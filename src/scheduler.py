"""
Scheduler para gestión automática de envíos de correos
Verifica periódicamente qué correos deben enviarse según el estado de las reservas
"""
import asyncio
from datetime import datetime, timedelta
from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from sqlalchemy.orm import Session

from config import settings
from database import (
    get_db,
    Reserva,
    EstadoOC,
    TipoCorreo,
    ConfiguracionCliente
)
from src.email_sender import email_sender


class OCScheduler:
    """Scheduler para envíos automáticos de correos de seguimiento de OC"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.logger = logger.bind(module="OCScheduler")

    def start(self):
        """Inicia el scheduler con todas las tareas programadas"""
        self.logger.info("🚀 Iniciando scheduler de seguimiento de OC...")

        # Tarea 1: Verificar y enviar correos pendientes (varias veces al día)
        interval_hours = 24 / settings.scheduler_checks_per_day
        self.scheduler.add_job(
            self.process_pending_emails,
            IntervalTrigger(hours=interval_hours),
            id='process_pending_emails',
            name='Procesar correos pendientes',
            replace_existing=True
        )

        # Tarea 2: Reintentar correos fallidos (cada 2 horas)
        self.scheduler.add_job(
            self.retry_failed_emails,
            IntervalTrigger(hours=2),
            id='retry_failed_emails',
            name='Reintentar correos fallidos',
            replace_existing=True
        )

        # Tarea 3: Limpieza de reservas expiradas (diario a las 2 AM)
        self.scheduler.add_job(
            self.cleanup_expired_reservations,
            CronTrigger(hour=2, minute=0),
            id='cleanup_expired',
            name='Limpiar reservas expiradas',
            replace_existing=True
        )

        # Tarea 4: Reporte diario de estado (diario a las 8 AM)
        self.scheduler.add_job(
            self.daily_status_report,
            CronTrigger(hour=8, minute=0),
            id='daily_report',
            name='Reporte diario',
            replace_existing=True
        )

        self.scheduler.start()
        self.logger.info("✅ Scheduler iniciado correctamente")

        # Ejecutar inmediatamente al iniciar
        asyncio.create_task(self.process_pending_emails())

    def shutdown(self):
        """Detiene el scheduler"""
        self.scheduler.shutdown()
        self.logger.info("⏹️ Scheduler detenido")

    async def process_pending_emails(self):
        """
        Procesa reservas pendientes y envía correos según corresponda
        """
        self.logger.info("🔄 Procesando correos pendientes...")

        db = next(get_db())

        try:
            # Obtener todas las reservas que requieren OC y están pendientes
            reservas_pendientes = db.query(Reserva).filter(
                Reserva.requiere_oc == True,
                Reserva.estado_oc == EstadoOC.PENDIENTE
            ).all()

            self.logger.info(f"Encontradas {len(reservas_pendientes)} reservas pendientes de OC")

            sent_count = 0

            for reserva in reservas_pendientes:
                # Obtener configuración del cliente
                config_cliente = db.query(ConfiguracionCliente).filter_by(
                    nombre_agencia=reserva.agencia,
                    activo=True
                ).first()

                if not config_cliente:
                    self.logger.warning(
                        f"Cliente {reserva.agencia} no tiene configuración activa"
                    )
                    continue

                # Determinar qué tipo de correo enviar
                correo_enviado = False

                # 1. Solicitud inicial (día 0)
                if reserva.necesita_solicitud_inicial:
                    self.logger.info(
                        f"📧 Enviando solicitud inicial: Reserva {reserva.id_reserva}"
                    )
                    success = email_sender.send_solicitud_inicial(
                        reserva=reserva,
                        db=db,
                        to_email=config_cliente.email_contacto
                    )
                    if success:
                        sent_count += 1
                        correo_enviado = True

                # 2. Recordatorio día 2
                elif reserva.necesita_recordatorio_dia2:
                    dias_config = config_cliente.dias_recordatorio_1 or settings.days_for_reminder_1
                    if reserva.dias_desde_creacion >= dias_config:
                        self.logger.info(
                            f"📧 Enviando recordatorio día {dias_config}: Reserva {reserva.id_reserva}"
                        )
                        success = email_sender.send_recordatorio_dia2(
                            reserva=reserva,
                            db=db,
                            to_email=config_cliente.email_contacto
                        )
                        if success:
                            sent_count += 1
                            correo_enviado = True

                # 3. Ultimátum día 4
                elif reserva.necesita_ultimatum_dia4:
                    dias_config = config_cliente.dias_recordatorio_2 or settings.days_for_reminder_2
                    if reserva.dias_desde_creacion >= dias_config:
                        self.logger.info(
                            f"🚨 Enviando ultimátum día {dias_config}: Reserva {reserva.id_reserva}"
                        )
                        success = email_sender.send_ultimatum_dia4(
                            reserva=reserva,
                            db=db,
                            to_email=config_cliente.email_contacto
                        )
                        if success:
                            sent_count += 1
                            correo_enviado = True

                # Si ya pasaron más de 5 días sin OC, marcar como expirada
                if reserva.dias_desde_creacion > 5 and not correo_enviado:
                    self.logger.warning(
                        f"⚠️ Reserva {reserva.id_reserva} marcada como EXPIRADA "
                        f"(sin OC después de {reserva.dias_desde_creacion} días)"
                    )
                    reserva.estado_oc = EstadoOC.EXPIRADA
                    db.commit()

            self.logger.info(f"✅ Procesamiento completado: {sent_count} correos enviados")

        except Exception as e:
            self.logger.error(f"❌ Error procesando correos pendientes: {e}")
            db.rollback()

        finally:
            db.close()

    async def retry_failed_emails(self):
        """Reintenta envío de correos que fallaron"""
        self.logger.info("🔄 Reintentando correos fallidos...")

        db = next(get_db())

        try:
            retried_count = email_sender.retry_failed_emails(db, max_retry=3)
            self.logger.info(f"✅ Reintentos completados: {retried_count} correos reenviados")

        except Exception as e:
            self.logger.error(f"❌ Error reintentando correos: {e}")

        finally:
            db.close()

    async def cleanup_expired_reservations(self):
        """
        Limpia reservas expiradas (check-in pasado, sin OC)
        """
        self.logger.info("🧹 Limpiando reservas expiradas...")

        db = next(get_db())

        try:
            now = datetime.utcnow()

            # Reservas con check-in pasado y OC pendiente
            expired = db.query(Reserva).filter(
                Reserva.fecha_checkin < now,
                Reserva.estado_oc == EstadoOC.PENDIENTE,
                Reserva.requiere_oc == True
            ).all()

            for reserva in expired:
                self.logger.warning(
                    f"⚠️ Reserva {reserva.id_reserva} expirada "
                    f"(check-in: {reserva.fecha_checkin}, sin OC)"
                )
                reserva.estado_oc = EstadoOC.EXPIRADA
                # TODO: Enviar notificación de expiración

            db.commit()
            self.logger.info(f"✅ Limpieza completada: {len(expired)} reservas expiradas")

        except Exception as e:
            self.logger.error(f"❌ Error en limpieza: {e}")
            db.rollback()

        finally:
            db.close()

    async def daily_status_report(self):
        """
        Genera un reporte diario del estado del sistema
        """
        self.logger.info("📊 Generando reporte diario...")

        db = next(get_db())

        try:
            # Estadísticas
            total_reservas = db.query(Reserva).filter_by(requiere_oc=True).count()
            pendientes = db.query(Reserva).filter_by(
                estado_oc=EstadoOC.PENDIENTE,
                requiere_oc=True
            ).count()
            recibidas = db.query(Reserva).filter_by(
                estado_oc=EstadoOC.RECIBIDA
            ).count()
            expiradas = db.query(Reserva).filter_by(
                estado_oc=EstadoOC.EXPIRADA
            ).count()

            # Reservas críticas (más de 4 días sin OC)
            criticas = db.query(Reserva).filter(
                Reserva.requiere_oc == True,
                Reserva.estado_oc == EstadoOC.PENDIENTE
            ).all()

            criticas_count = sum(1 for r in criticas if r.dias_desde_creacion >= 4)

            report = f"""
📊 REPORTE DIARIO - SEGUIMIENTO DE OC
{'=' * 50}
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}

📈 ESTADÍSTICAS GENERALES:
  • Total reservas con OC requerida: {total_reservas}
  • OC Pendientes: {pendientes}
  • OC Recibidas: {recibidas}
  • Reservas Expiradas: {expiradas}

🚨 ALERTAS:
  • Reservas críticas (>4 días sin OC): {criticas_count}

{'=' * 50}
            """

            self.logger.info(report)

            # TODO: Enviar reporte por email si está configurado
            if settings.system_notification_email:
                # Enviar reporte por correo
                pass

        except Exception as e:
            self.logger.error(f"❌ Error generando reporte: {e}")

        finally:
            db.close()

    def get_stats(self) -> dict:
        """
        Obtiene estadísticas actuales del sistema

        Returns:
            Diccionario con estadísticas
        """
        db = next(get_db())

        try:
            stats = {
                'total_reservas': db.query(Reserva).filter_by(requiere_oc=True).count(),
                'oc_pendientes': db.query(Reserva).filter_by(
                    estado_oc=EstadoOC.PENDIENTE
                ).count(),
                'oc_recibidas': db.query(Reserva).filter_by(
                    estado_oc=EstadoOC.RECIBIDA
                ).count(),
                'oc_expiradas': db.query(Reserva).filter_by(
                    estado_oc=EstadoOC.EXPIRADA
                ).count(),
            }

            # Calcular reservas críticas
            reservas_pendientes = db.query(Reserva).filter_by(
                estado_oc=EstadoOC.PENDIENTE,
                requiere_oc=True
            ).all()

            stats['criticas'] = sum(1 for r in reservas_pendientes if r.dias_desde_creacion >= 4)

            return stats

        finally:
            db.close()


# Instancia global
oc_scheduler = OCScheduler()


if __name__ == "__main__":
    # Test del scheduler
    from database import init_db

    init_db()

    # Iniciar scheduler
    scheduler = OCScheduler()
    scheduler.start()

    # Mantener ejecutando
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("\n👋 Scheduler detenido")

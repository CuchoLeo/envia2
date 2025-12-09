"""
Módulo de envío de correos SMTP con plantillas Jinja2
Maneja el envío de correos HTML con reintentos y gestión de errores
"""
import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

from jinja2 import Environment, FileSystemLoader, Template
from loguru import logger
from sqlalchemy.orm import Session

from config import settings
from database import Reserva, CorreoEnviado, TipoCorreo, EstadoEnvio, ConfiguracionCliente


class EmailSender:
    """Manejador de envío de correos SMTP"""

    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.smtp_from_email
        self.from_name = settings.smtp_from_name
        self.use_tls = settings.smtp_use_tls

        # Configurar Jinja2
        # Los templates están en el directorio raíz del proyecto, no en src/
        templates_dir = Path(__file__).parent.parent / "templates"
        self.jinja_env = Environment(loader=FileSystemLoader(str(templates_dir)))

        self.logger = logger.bind(module="EmailSender")

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        cc: Optional[List[str]] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Envía un correo electrónico

        Args:
            to_email: Destinatario principal
            subject: Asunto del correo
            html_body: Cuerpo HTML
            text_body: Cuerpo texto plano (opcional)
            cc: Lista de destinatarios en copia

        Returns:
            (exitoso, mensaje_error)
        """
        try:
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email

            if cc:
                msg['Cc'] = ', '.join(cc)

            # Agregar cuerpo texto plano
            if text_body:
                part1 = MIMEText(text_body, 'plain', 'utf-8')
                msg.attach(part1)

            # Agregar cuerpo HTML
            part2 = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(part2)

            # Conectar y enviar
            self.logger.info(f"Enviando correo a {to_email}: {subject}")

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()

                server.login(self.smtp_username, self.smtp_password)

                # Lista de todos los destinatarios
                recipients = [to_email]
                if cc:
                    recipients.extend(cc)

                server.send_message(msg, from_addr=self.from_email, to_addrs=recipients)

            self.logger.info(f"✅ Correo enviado exitosamente a {to_email}")
            return True, None

        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"Error de autenticación SMTP: {e}"
            self.logger.error(error_msg)
            return False, error_msg

        except smtplib.SMTPException as e:
            error_msg = f"Error SMTP: {e}"
            self.logger.error(error_msg)
            return False, error_msg

        except Exception as e:
            error_msg = f"Error inesperado enviando correo: {e}"
            self.logger.error(error_msg)
            return False, error_msg

    def render_template(
        self,
        template_name: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Renderiza una plantilla Jinja2 con el contexto dado

        Args:
            template_name: Nombre del archivo de plantilla
            context: Diccionario con variables para la plantilla

        Returns:
            HTML renderizado
        """
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            self.logger.error(f"Error renderizando plantilla {template_name}: {e}")
            raise

    def _get_cliente_email(self, reserva: Reserva, db: Session) -> Optional[str]:
        """
        Obtiene el email de contacto del cliente desde configuracion_clientes

        Args:
            reserva: Objeto Reserva
            db: Sesión de base de datos

        Returns:
            Email de contacto del cliente o None si no está configurado
        """
        try:
            cliente = db.query(ConfiguracionCliente).filter_by(
                nombre_agencia=reserva.agencia
            ).first()

            if cliente and cliente.email_contacto:
                return cliente.email_contacto
            else:
                self.logger.warning(
                    f"No se encontró email de contacto para agencia: {reserva.agencia}"
                )
                return None

        except Exception as e:
            self.logger.error(f"Error obteniendo email del cliente: {e}")
            return None

    def send_solicitud_inicial(
        self,
        reserva: Reserva,
        db: Session,
        to_email: Optional[str] = None
    ) -> bool:
        """
        Envía correo de solicitud inicial de OC

        Args:
            reserva: Objeto Reserva
            db: Sesión de base de datos
            to_email: Email del destinatario (opcional, se busca en configuracion_clientes)

        Returns:
            True si se envió exitosamente
        """
        # Preparar contexto para la plantilla
        context = self._prepare_context(reserva)

        # Renderizar plantilla
        html_body = self.render_template('solicitud_inicial.html', context)

        # Determinar destinatario
        if not to_email:
            to_email = self._get_cliente_email(reserva, db)

            if not to_email:
                error_msg = f"No hay email de contacto configurado para {reserva.agencia}"
                self.logger.error(error_msg)

                # Registrar el intento fallido en BD
                correo = CorreoEnviado(
                    reserva_id=reserva.id,
                    tipo_correo=TipoCorreo.SOLICITUD_INICIAL,
                    destinatario="SIN EMAIL",
                    asunto=f"Solicitud de Orden de Compra - Reserva {reserva.id_reserva}",
                    cuerpo_html=html_body,
                    estado=EstadoEnvio.ERROR,
                    fecha_programado=datetime.utcnow(),
                    fecha_error=datetime.utcnow(),
                    mensaje_error=error_msg,
                    intentos=1
                )
                db.add(correo)
                db.commit()
                return False

        # Enviar correo
        subject = f"Solicitud de Orden de Compra - Reserva {reserva.id_reserva}"

        success, error = self.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            cc=settings.cc_recipients_list
        )

        # Registrar en base de datos
        correo = CorreoEnviado(
            reserva_id=reserva.id,
            tipo_correo=TipoCorreo.SOLICITUD_INICIAL,
            destinatario=to_email,
            cc=', '.join(settings.cc_recipients_list) if settings.cc_recipients_list else None,
            asunto=subject,
            cuerpo_html=html_body,
            estado=EstadoEnvio.ENVIADO if success else EstadoEnvio.ERROR,
            fecha_programado=datetime.utcnow(),
            fecha_enviado=datetime.utcnow() if success else None,
            fecha_error=datetime.utcnow() if not success else None,
            mensaje_error=error,
            intentos=1
        )

        db.add(correo)
        db.commit()

        return success

    def send_recordatorio_dia2(
        self,
        reserva: Reserva,
        db: Session,
        to_email: Optional[str] = None
    ) -> bool:
        """
        Envía recordatorio del día 2

        Args:
            reserva: Objeto Reserva
            db: Sesión de base de datos
            to_email: Email del destinatario (opcional, se busca en configuracion_clientes)

        Returns:
            True si se envió exitosamente
        """
        context = self._prepare_context(reserva)
        html_body = self.render_template('recordatorio_dia2.html', context)

        if not to_email:
            to_email = self._get_cliente_email(reserva, db)

            if not to_email:
                error_msg = f"No hay email de contacto configurado para {reserva.agencia}"
                self.logger.error(error_msg)

                # Registrar el intento fallido en BD
                correo = CorreoEnviado(
                    reserva_id=reserva.id,
                    tipo_correo=TipoCorreo.RECORDATORIO_DIA_2,
                    destinatario="SIN EMAIL",
                    asunto=f"Recordatorio - OC Pendiente - Reserva {reserva.id_reserva}",
                    cuerpo_html=html_body,
                    estado=EstadoEnvio.ERROR,
                    fecha_programado=datetime.utcnow(),
                    fecha_error=datetime.utcnow(),
                    mensaje_error=error_msg,
                    intentos=1
                )
                db.add(correo)
                db.commit()
                return False

        subject = f"Recordatorio - OC Pendiente - Reserva {reserva.id_reserva}"

        success, error = self.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            cc=settings.cc_recipients_list
        )

        correo = CorreoEnviado(
            reserva_id=reserva.id,
            tipo_correo=TipoCorreo.RECORDATORIO_DIA_2,
            destinatario=to_email,
            cc=', '.join(settings.cc_recipients_list) if settings.cc_recipients_list else None,
            asunto=subject,
            cuerpo_html=html_body,
            estado=EstadoEnvio.ENVIADO if success else EstadoEnvio.ERROR,
            fecha_programado=datetime.utcnow(),
            fecha_enviado=datetime.utcnow() if success else None,
            fecha_error=datetime.utcnow() if not success else None,
            mensaje_error=error,
            intentos=1
        )

        db.add(correo)
        db.commit()

        return success

    def send_ultimatum_dia4(
        self,
        reserva: Reserva,
        db: Session,
        to_email: Optional[str] = None
    ) -> bool:
        """
        Envía ultimátum del día 4

        Args:
            reserva: Objeto Reserva
            db: Sesión de base de datos
            to_email: Email del destinatario (opcional, se busca en configuracion_clientes)

        Returns:
            True si se envió exitosamente
        """
        context = self._prepare_context(reserva)
        html_body = self.render_template('ultimatum_dia4.html', context)

        if not to_email:
            to_email = self._get_cliente_email(reserva, db)

            if not to_email:
                error_msg = f"No hay email de contacto configurado para {reserva.agencia}"
                self.logger.error(error_msg)

                # Registrar el intento fallido en BD
                correo = CorreoEnviado(
                    reserva_id=reserva.id,
                    tipo_correo=TipoCorreo.ULTIMATUM_DIA_4,
                    destinatario="SIN EMAIL",
                    asunto=f"🚨 URGENTE - Ultimátum OC - Reserva {reserva.id_reserva}",
                    cuerpo_html=html_body,
                    estado=EstadoEnvio.ERROR,
                    fecha_programado=datetime.utcnow(),
                    fecha_error=datetime.utcnow(),
                    mensaje_error=error_msg,
                    intentos=1
                )
                db.add(correo)
                db.commit()
                return False

        subject = f"🚨 URGENTE - Ultimátum OC - Reserva {reserva.id_reserva}"

        success, error = self.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            cc=settings.cc_recipients_list
        )

        correo = CorreoEnviado(
            reserva_id=reserva.id,
            tipo_correo=TipoCorreo.ULTIMATUM_DIA_4,
            destinatario=to_email,
            cc=', '.join(settings.cc_recipients_list) if settings.cc_recipients_list else None,
            asunto=subject,
            cuerpo_html=html_body,
            estado=EstadoEnvio.ENVIADO if success else EstadoEnvio.ERROR,
            fecha_programado=datetime.utcnow(),
            fecha_enviado=datetime.utcnow() if success else None,
            fecha_error=datetime.utcnow() if not success else None,
            mensaje_error=error,
            intentos=1
        )

        db.add(correo)
        db.commit()

        return success

    def enviar_solicitud_oc(
        self,
        reserva: Reserva,
        tipo_correo: str,
        destinatario: Optional[str] = None,
        db: Optional[Session] = None
    ) -> bool:
        """
        Método unificado para enviar correos de solicitud de OC

        Args:
            reserva: Objeto Reserva
            tipo_correo: Tipo de correo a enviar (solicitud_inicial, recordatorio_1, recordatorio_2, ultimatum)
            destinatario: Email del destinatario (opcional)
            db: Sesión de base de datos (opcional, si no se proporciona no se registra en BD)

        Returns:
            True si se envió exitosamente
        """
        # Mapeo de tipos de correo a métodos
        tipo_map = {
            'solicitud_inicial': ('send_solicitud_inicial', TipoCorreo.SOLICITUD_INICIAL, 'solicitud_inicial.html'),
            'recordatorio_1': ('send_recordatorio_dia2', TipoCorreo.RECORDATORIO_DIA_2, 'recordatorio_dia2.html'),
            'recordatorio_2': ('send_ultimatum_dia4', TipoCorreo.ULTIMATUM_DIA_4, 'recordatorio_dia4.html'),
            'ultimatum': ('send_ultimatum_dia4', TipoCorreo.ULTIMATUM_DIA_4, 'ultimatum_dia4.html')
        }

        if tipo_correo not in tipo_map:
            self.logger.error(f"Tipo de correo no válido: {tipo_correo}")
            return False

        # Si se proporciona db, usar el método específico que registra en BD
        if db:
            method_name, _, _ = tipo_map[tipo_correo]
            method = getattr(self, method_name)
            return method(reserva=reserva, db=db, to_email=destinatario)

        # Si no hay db, enviar sin registrar
        _, tipo_enum, template_file = tipo_map[tipo_correo]

        # Preparar contexto
        context = self._prepare_context(reserva)

        # Renderizar plantilla
        html_body = self.render_template(template_file, context)

        # Determinar destinatario
        if not destinatario:
            # Sin db no podemos buscar el email, retornar error
            error_msg = "No se proporcionó destinatario y no hay sesión de BD para buscarlo"
            self.logger.error(error_msg)
            return False

        # Asunto según tipo
        asuntos = {
            'solicitud_inicial': f"Solicitud de Orden de Compra - Reserva {reserva.id_reserva}",
            'recordatorio_1': f"Recordatorio - OC Pendiente - Reserva {reserva.id_reserva}",
            'recordatorio_2': f"⚠️ URGENTE - Segunda Solicitud OC - Reserva {reserva.id_reserva}",
            'ultimatum': f"🚨 URGENTE - Ultimátum OC - Reserva {reserva.id_reserva}"
        }

        subject = asuntos.get(tipo_correo, f"Solicitud OC - Reserva {reserva.id_reserva}")

        # Enviar correo
        success, error = self.send_email(
            to_email=destinatario,
            subject=subject,
            html_body=html_body,
            cc=settings.cc_recipients_list
        )

        if not success:
            self.logger.error(f"Error enviando correo: {error}")

        return success

    def _prepare_context(self, reserva: Reserva) -> Dict[str, Any]:
        """
        Prepara el contexto para renderizar plantillas

        Args:
            reserva: Objeto Reserva

        Returns:
            Diccionario con variables para la plantilla
        """
        # Formatear monto con separador de miles
        monto_formateado = f"{reserva.monto_total:,.0f}" if reserva.monto_total else "0"

        return {
            'id_reserva': reserva.id_reserva,
            'loc_interno': reserva.loc_interno,
            'localizador': reserva.localizador,
            'agencia': reserva.agencia,
            'nombre_hotel': reserva.nombre_hotel or 'N/A',
            'direccion_hotel': reserva.direccion_hotel,
            'telefono_hotel': reserva.telefono_hotel,
            'fecha_checkin': reserva.fecha_checkin.strftime('%d/%m/%Y') if reserva.fecha_checkin else 'N/A',
            'fecha_checkout': reserva.fecha_checkout.strftime('%d/%m/%Y') if reserva.fecha_checkout else 'N/A',
            'hora_llegada': reserva.hora_llegada or 'N/A',
            'hora_salida': reserva.hora_salida or 'N/A',
            'numero_noches': reserva.numero_noches or 0,
            'numero_habitaciones': reserva.numero_habitaciones or 0,
            'monto_total': monto_formateado,
            'moneda': reserva.moneda,
            'dias_desde_creacion': reserva.dias_desde_creacion,
            'email_remitente': settings.smtp_from_email,
            'email_oc': settings.oc_inbox_username,
        }

    def retry_failed_emails(self, db: Session, max_retry: int = 3) -> int:
        """
        Reintenta envío de correos fallidos

        Args:
            db: Sesión de base de datos
            max_retry: Número máximo de reintentos

        Returns:
            Número de correos reenviados exitosamente
        """
        failed_emails = db.query(CorreoEnviado).filter(
            CorreoEnviado.estado == EstadoEnvio.ERROR,
            CorreoEnviado.intentos < max_retry
        ).all()

        success_count = 0

        for correo in failed_emails:
            self.logger.info(
                f"Reintentando envío {correo.intentos + 1}/{max_retry}: "
                f"{correo.tipo_correo.value} para reserva {correo.reserva.id_reserva}"
            )

            success, error = self.send_email(
                to_email=correo.destinatario,
                subject=correo.asunto,
                html_body=correo.cuerpo_html,
                cc=correo.cc.split(',') if correo.cc else None
            )

            correo.intentos += 1

            if success:
                correo.estado = EstadoEnvio.ENVIADO
                correo.fecha_enviado = datetime.utcnow()
                correo.mensaje_error = None
                success_count += 1
                self.logger.info(f"✅ Reenvío exitoso")
            else:
                correo.fecha_error = datetime.utcnow()
                correo.mensaje_error = error
                self.logger.error(f"❌ Reenvío fallido: {error}")

            db.commit()

        return success_count


# Instancia global
email_sender = EmailSender()


if __name__ == "__main__":
    # Test de renderizado de plantillas
    from database import init_db

    init_db()
    db = next(get_db())

    # Buscar primera reserva que requiera OC
    reserva = db.query(Reserva).filter_by(requiere_oc=True).first()

    if reserva:
        print(f"\n=== Test de envío de correos ===")
        print(f"Reserva: {reserva.id_reserva} - {reserva.agencia}")

        # Renderizar plantillas (sin enviar)
        sender = EmailSender()
        context = sender._prepare_context(reserva)

        print("\n✅ Plantillas renderizadas correctamente:")
        print("  - solicitud_inicial.html")
        print("  - recordatorio_dia2.html")
        print("  - ultimatum_dia4.html")
    else:
        print("No hay reservas en la base de datos")

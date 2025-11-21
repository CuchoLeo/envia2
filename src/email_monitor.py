"""
Monitor de correos IMAP para detectar nuevas reservas y OC recibidas
Monitorea casillas de correo y procesa archivos adjuntos PDF
"""
import time
import email
from email.header import decode_header
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime, parseaddr
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path
import asyncio

from loguru import logger
from sqlalchemy.orm import Session

from config import settings
from database import Reserva, OrdenCompra, EstadoOC, get_db
from src.pdf_processor import pdf_processor
from src.imap_wrapper import SimpleIMAPClient


class EmailMonitor:
    """Monitor de correos IMAP"""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        mailbox: str = "INBOX",
        use_ssl: bool = True
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.mailbox = mailbox
        self.use_ssl = use_ssl
        self.logger = logger.bind(module="EmailMonitor", account=username)
        self.client: Optional[SimpleIMAPClient] = None
        self.processed_uids = set()

    def connect(self) -> bool:
        """Conecta al servidor IMAP"""
        try:
            self.logger.info(f"Conectando a {self.host}:{self.port}")

            # Usar wrapper simple compatible con Python 3.14+
            self.client = SimpleIMAPClient(
                host=self.host,
                port=self.port,
                use_ssl=self.use_ssl
            )

            if not self.client.connect(self.username, self.password):
                return False

            if not self.client.select_folder(self.mailbox):
                return False

            self.logger.info("✅ Conexión IMAP establecida")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error conectando a IMAP: {e}")
            import traceback
            self.logger.debug(traceback.format_exc())
            return False

    def disconnect(self):
        """Cierra la conexión IMAP"""
        if self.client:
            try:
                self.client.disconnect()
                self.logger.info("Desconectado de IMAP")
            except Exception as e:
                self.logger.error(f"Error al desconectar: {e}")

    def check_new_emails(self) -> List[Dict[str, Any]]:
        """
        Verifica si hay correos nuevos no procesados

        Returns:
            Lista de diccionarios con información de correos nuevos
        """
        if not self.client:
            if not self.connect():
                return []

        try:
            # Buscar correos no leídos
            messages = self.client.search_unseen()

            self.logger.info(f"Encontrados {len(messages)} correos no leídos")

            emails_data = []
            for uid in messages:
                if uid not in self.processed_uids:
                    email_data = self._fetch_email(uid)
                    if email_data:
                        emails_data.append(email_data)
                        self.processed_uids.add(uid)

            return emails_data

        except Exception as e:
            self.logger.error(f"Error verificando correos: {e}")
            return []

    def _fetch_email(self, uid: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene los datos completos de un correo

        Args:
            uid: UID del mensaje

        Returns:
            Diccionario con datos del correo y adjuntos
        """
        try:
            # Usar el wrapper simple
            email_data = self.client.fetch_message(uid)

            if not email_data:
                return None

            subject = email_data['subject']
            from_address = email_data['from']

            self.logger.info(f"Procesando correo: {subject} de {from_address}")

            # Filtrar solo adjuntos PDF
            pdf_attachments = []
            for att in email_data.get('attachments', []):
                if att['filename'].lower().endswith('.pdf'):
                    pdf_attachments.append(att)
                    self.logger.info(f"  📎 Adjunto PDF: {att['filename']} ({att['size']} bytes)")

            return {
                'uid': uid,
                'subject': subject,
                'from': from_address,
                'to': email_data.get('to', ''),
                'date': email_data.get('date'),
                'body_text': email_data.get('body_text', ''),
                'body_html': email_data.get('body_html', ''),
                'attachments': pdf_attachments
            }

        except Exception as e:
            self.logger.error(f"Error obteniendo correo UID {uid}: {e}")
            return None

    def mark_as_read(self, uid: int):
        """Marca un correo como leído"""
        try:
            self.client.mark_as_read(uid)
        except Exception as e:
            self.logger.error(f"Error marcando correo {uid} como leído: {e}")


class ReservaMonitor(EmailMonitor):
    """Monitor especializado para correos de confirmación de reservas"""

    def __init__(self):
        super().__init__(
            host=settings.imap_host,
            port=settings.imap_port,
            username=settings.imap_username,
            password=settings.imap_password,
            mailbox=settings.imap_mailbox,
            use_ssl=settings.imap_use_ssl
        )
        self.logger = logger.bind(module="ReservaMonitor")

    def process_new_reservations(self, db: Session) -> int:
        """
        Procesa correos nuevos buscando confirmaciones de reservas

        Returns:
            Número de reservas procesadas
        """
        emails = self.check_new_emails()
        processed_count = 0

        for email_data in emails:
            # Filtrar solo correos de confirmación de reserva
            subject = email_data['subject'].lower()
            if 'confirmación' not in subject and 'confirmacion' not in subject and 'confirmation' not in subject:
                self.logger.debug(f"Correo no es confirmación de reserva: {email_data['subject']}")
                continue

            # Validar que el remitente esté autorizado
            # Extraer solo el email del campo From (ignorando el nombre)
            from_name, from_email = parseaddr(email_data['from'])
            if not settings.is_sender_allowed(from_email):
                self.logger.warning(
                    f"Remitente NO autorizado: {from_email} ({email_data['from']}). "
                    f"Correo ignorado: {email_data['subject']}"
                )
                continue

            # Verificar que tenga adjuntos PDF
            if not email_data['attachments']:
                self.logger.debug(f"Correo sin adjuntos PDF: {email_data['subject']}")
                continue

            # Procesar cada adjunto PDF
            for attachment in email_data['attachments']:
                try:
                    # Extraer datos del PDF
                    pdf_data = pdf_processor.extract_from_bytes(
                        attachment['content'],
                        attachment['filename']
                    )

                    if not pdf_data:
                        self.logger.warning(f"No se pudieron extraer datos de {attachment['filename']}")
                        continue

                    # Validar datos
                    is_valid, errors = pdf_processor.validate_data(pdf_data)
                    if not is_valid:
                        self.logger.error(f"Datos inválidos en {attachment['filename']}: {errors}")
                        continue

                    # Verificar si la agencia requiere seguimiento de OC
                    agencia = pdf_data.get('agencia', '')
                    # requiere_oc = settings.requires_oc(agencia)  # Comentado: Todas las reservas requieren OC
                    requiere_oc = True  # TODAS las reservas requieren OC

                    # Verificar si ya existe la reserva
                    id_reserva = pdf_data.get('id_reserva')
                    existing = db.query(Reserva).filter_by(id_reserva=id_reserva).first()

                    if existing:
                        self.logger.warning(f"Reserva {id_reserva} ya existe en la base de datos")
                        continue

                    # Crear nueva reserva
                    reserva = Reserva(
                        id_reserva=pdf_data.get('id_reserva'),
                        loc_interno=pdf_data.get('loc_interno'),
                        localizador=pdf_data.get('localizador'),
                        agencia=agencia,
                        nombre_hotel=pdf_data.get('nombre_hotel'),
                        direccion_hotel=pdf_data.get('direccion_hotel'),
                        telefono_hotel=pdf_data.get('telefono_hotel'),
                        fecha_checkin=pdf_data.get('fecha_checkin'),
                        fecha_checkout=pdf_data.get('fecha_checkout'),
                        hora_llegada=pdf_data.get('hora_llegada'),
                        hora_salida=pdf_data.get('hora_salida'),
                        numero_noches=pdf_data.get('numero_noches'),
                        numero_habitaciones=pdf_data.get('numero_habitaciones'),
                        monto_total=pdf_data.get('monto_total'),
                        moneda=pdf_data.get('moneda', 'CLP'),
                        detalles_habitaciones=pdf_data.get('detalles_habitaciones'),
                        fecha_limite_cancelacion=pdf_data.get('fecha_limite_cancelacion'),
                        observaciones_hotel=pdf_data.get('observaciones_hotel'),
                        notas_asesor=pdf_data.get('notas_asesor'),
                        fecha_emision=pdf_data.get('fecha_emision'),
                        estado_oc=EstadoOC.PENDIENTE if requiere_oc else EstadoOC.NO_REQUIERE_OC,
                        requiere_oc=requiere_oc,
                        email_origen_id=str(email_data['uid']),
                        email_origen_fecha=parsedate_to_datetime(email_data['date']) if email_data.get('date') else datetime.now(),
                        pdf_filename=attachment['filename']
                    )

                    db.add(reserva)
                    db.commit()

                    self.logger.info(
                        f"✅ Reserva creada: {id_reserva} - {agencia} - "
                        f"Requiere OC: {'Sí' if requiere_oc else 'No'}"
                    )

                    processed_count += 1

                    # Marcar correo como leído
                    self.mark_as_read(email_data['uid'])

                except Exception as e:
                    self.logger.error(f"Error procesando adjunto {attachment['filename']}: {e}")
                    db.rollback()

        return processed_count

    async def monitor_loop(self):
        """Loop de monitoreo continuo"""
        self.logger.info("🔄 Iniciando monitoreo de reservas...")

        # Conectar inicialmente
        if not self.connect():
            self.logger.error("❌ No se pudo conectar inicialmente, reintentando en 60s...")
            await asyncio.sleep(60)

        while True:
            try:
                # Verificar conexión antes de procesar
                if not self.client:
                    self.logger.warning("⚠️ Cliente no conectado, reconectando...")
                    if not self.connect():
                        self.logger.error("❌ Reconexión fallida, esperando 60s...")
                        await asyncio.sleep(60)
                        continue

                db = next(get_db())
                count = self.process_new_reservations(db)

                if count > 0:
                    self.logger.info(f"✅ Procesadas {count} reservas nuevas")

                # Esperar antes del próximo check
                await asyncio.sleep(settings.imap_check_interval)

            except Exception as e:
                self.logger.error(f"Error en loop de monitoreo: {e}")
                # Desconectar para forzar reconexión en el siguiente ciclo
                self.disconnect()
                await asyncio.sleep(60)  # Esperar 1 minuto en caso de error


class OCMonitor(EmailMonitor):
    """Monitor especializado para correos con órdenes de compra"""

    def __init__(self):
        super().__init__(
            host=settings.oc_inbox_host,
            port=settings.oc_inbox_port,
            username=settings.oc_inbox_username,
            password=settings.oc_inbox_password,
            mailbox=settings.oc_inbox_mailbox,
            use_ssl=settings.oc_inbox_use_ssl
        )
        self.logger = logger.bind(module="OCMonitor")

    def process_oc_emails(self, db: Session) -> int:
        """
        Procesa correos nuevos buscando órdenes de compra

        Returns:
            Número de OC procesadas
        """
        emails = self.check_new_emails()
        processed_count = 0

        for email_data in emails:
            # Filtrar solo correos de órdenes de compra
            subject = email_data['subject'].lower()
            if not any(keyword in subject for keyword in ['orden de compra', 'oc', 'purchase order', 'orden compra']):
                self.logger.debug(f"Correo no es orden de compra: {email_data['subject']}")
                continue

            # Verificar que tenga adjuntos PDF
            if not email_data['attachments']:
                continue

            # Intentar asociar con reserva existente
            reserva = self._find_reserva_from_email(email_data, db)

            if not reserva:
                self.logger.warning(
                    f"No se pudo asociar correo con reserva: {email_data['subject']}"
                )
                continue

            # Verificar que no tenga ya una OC
            if reserva.orden_compra:
                self.logger.warning(f"Reserva {reserva.id_reserva} ya tiene una OC registrada")
                continue

            # Procesar adjuntos
            for attachment in email_data['attachments']:
                try:
                    # Crear registro de OC
                    oc = OrdenCompra(
                        reserva_id=reserva.id,
                        email_remitente=email_data['from'],
                        email_asunto=email_data['subject'],
                        email_fecha=parsedate_to_datetime(email_data['date']) if email_data.get('date') else datetime.now(),
                        email_id=str(email_data['uid']),
                        archivo_nombre=attachment['filename'],
                        archivo_tamano=attachment['size'],
                        # TODO: Guardar archivo en disco o GCS
                        archivo_ruta=f"./oc_files/{reserva.id_reserva}_{attachment['filename']}"
                    )

                    db.add(oc)

                    # Actualizar estado de reserva
                    reserva.estado_oc = EstadoOC.RECIBIDA

                    db.commit()

                    self.logger.info(
                        f"✅ OC recibida para reserva {reserva.id_reserva} - {reserva.agencia}"
                    )

                    processed_count += 1

                    # Marcar correo como leído
                    self.mark_as_read(email_data['uid'])

                    break  # Solo procesar el primer PDF

                except Exception as e:
                    self.logger.error(f"Error procesando OC: {e}")
                    db.rollback()

        return processed_count

    def _find_reserva_from_email(self, email_data: Dict[str, Any], db: Session) -> Optional[Reserva]:
        """
        Intenta encontrar la reserva asociada al correo de OC

        Busca por localizadores o ID en el asunto o cuerpo del correo
        """
        text = f"{email_data['subject']} {email_data['body_text']}"

        # Buscar patrones comunes
        import re

        # Buscar ID de reserva
        id_match = re.search(r'ID[:\s]*(\d+)', text, re.IGNORECASE)
        if id_match:
            reserva = db.query(Reserva).filter_by(
                id_reserva=id_match.group(1),
                estado_oc=EstadoOC.PENDIENTE
            ).first()
            if reserva:
                return reserva

        # Buscar LOC Interno
        loc_match = re.search(r'LOC[:\s]+([A-Z0-9]+)', text, re.IGNORECASE)
        if loc_match:
            reserva = db.query(Reserva).filter_by(
                loc_interno=loc_match.group(1),
                estado_oc=EstadoOC.PENDIENTE
            ).first()
            if reserva:
                return reserva

        # Buscar por "Reserva CODIGO" en el asunto
        reserva_match = re.search(r'Reserva[:\s]+([A-Z0-9]+)', text, re.IGNORECASE)
        if reserva_match:
            codigo = reserva_match.group(1)
            # Buscar por id_reserva o loc_interno
            reserva = db.query(Reserva).filter(
                (Reserva.id_reserva == codigo) | (Reserva.loc_interno == codigo)
            ).filter_by(estado_oc=EstadoOC.PENDIENTE).first()
            if reserva:
                return reserva

        # Buscar por "Orden de Compra CODIGO" o "OC CODIGO"
        oc_match = re.search(r'(?:orden\s+de\s+compra|OC)[:\s]+([A-Z0-9]+)', text, re.IGNORECASE)
        if oc_match:
            codigo = oc_match.group(1)
            # Buscar por id_reserva o loc_interno
            reserva = db.query(Reserva).filter(
                (Reserva.id_reserva == codigo) | (Reserva.loc_interno == codigo)
            ).filter_by(estado_oc=EstadoOC.PENDIENTE).first()
            if reserva:
                return reserva

        # Buscar por agencia en el remitente
        from_email = email_data['from']
        reservas_pendientes = db.query(Reserva).filter_by(
            estado_oc=EstadoOC.PENDIENTE
        ).all()

        # Buscar coincidencia por dominio de correo
        for reserva in reservas_pendientes:
            # Simplificado: buscar nombre de agencia en el correo
            if reserva.agencia.lower() in from_email.lower():
                return reserva

        return None

    async def monitor_loop(self):
        """Loop de monitoreo continuo de OC"""
        self.logger.info("🔄 Iniciando monitoreo de órdenes de compra...")

        # Conectar inicialmente
        if not self.connect():
            self.logger.error("❌ No se pudo conectar inicialmente, reintentando en 60s...")
            await asyncio.sleep(60)

        while True:
            try:
                # Verificar conexión antes de procesar
                if not self.client:
                    self.logger.warning("⚠️ Cliente no conectado, reconectando...")
                    if not self.connect():
                        self.logger.error("❌ Reconexión fallida, esperando 60s...")
                        await asyncio.sleep(60)
                        continue

                db = next(get_db())
                count = self.process_oc_emails(db)

                if count > 0:
                    self.logger.info(f"✅ Procesadas {count} órdenes de compra")

                # Esperar antes del próximo check
                await asyncio.sleep(settings.oc_check_interval)

            except Exception as e:
                self.logger.error(f"Error en loop de monitoreo OC: {e}")
                # Desconectar para forzar reconexión
                self.disconnect()
                await asyncio.sleep(60)


if __name__ == "__main__":
    # Test de monitoreo
    from database import init_db

    init_db()

    monitor = ReservaMonitor()
    if monitor.connect():
        db = next(get_db())
        count = monitor.process_new_reservations(db)
        print(f"Procesadas {count} reservas")
        monitor.disconnect()

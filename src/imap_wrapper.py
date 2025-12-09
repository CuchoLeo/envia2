"""
Wrapper alternativo para IMAP usando biblioteca estándar de Python
Compatible con Python 3.14+
"""
import imaplib
import email
from email.parser import BytesParser
from email import policy
from typing import List, Optional, Dict, Any
from loguru import logger


class SimpleIMAPClient:
    """Cliente IMAP simple usando biblioteca estándar de Python"""

    def __init__(self, host: str, port: int = 993, use_ssl: bool = True):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.client: Optional[imaplib.IMAP4_SSL] = None
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.current_folder: str = "INBOX"
        self.logger = logger.bind(module="SimpleIMAPClient")

    def connect(self, username: str, password: str) -> bool:
        """Conecta y autentica con el servidor IMAP"""
        try:
            # Guardar credenciales para reconexión
            self.username = username
            self.password = password

            self.logger.info(f"Conectando a {self.host}:{self.port}")

            if self.use_ssl:
                self.client = imaplib.IMAP4_SSL(self.host, self.port)
            else:
                self.client = imaplib.IMAP4(self.host, self.port)

            # Login
            self.client.login(username, password)
            self.logger.info("✅ Conexión y autenticación exitosa")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error conectando: {e}")
            return False

    def _ensure_connected(self) -> bool:
        """Verifica la conexión y reconecta si es necesario"""
        try:
            # Intentar hacer un NOOP (no operation) para verificar conexión
            if self.client:
                self.client.noop()
                return True
            else:
                # Cliente no existe, necesita conectarse
                self.logger.warning("⚠️ Cliente no inicializado, conectando...")
                if self.username and self.password:
                    if self.connect(self.username, self.password):
                        # Re-seleccionar la carpeta que estaba activa
                        return self.select_folder(self.current_folder)
                return False
        except:
            # Conexión perdida, intentar reconectar
            self.logger.warning("⚠️ Conexión perdida, reconectando...")
            # Limpiar cliente actual
            self.client = None
            if self.username and self.password:
                if self.connect(self.username, self.password):
                    # Re-seleccionar la carpeta que estaba activa
                    return self.select_folder(self.current_folder)
            return False

    def disconnect(self):
        """Cierra la conexión"""
        if self.client:
            try:
                self.client.logout()
            except:
                pass

    def select_folder(self, folder: str = "INBOX") -> bool:
        """Selecciona una carpeta"""
        try:
            if not self.client:
                self.logger.error("Cliente no conectado")
                return False

            status, response = self.client.select(folder)

            if status == 'OK':
                self.current_folder = folder
                self.logger.debug(f"Carpeta '{folder}' seleccionada")
                return True
            else:
                self.logger.error(f"Error seleccionando carpeta {folder}: {response}")
                return False

        except Exception as e:
            self.logger.error(f"Error seleccionando carpeta {folder}: {e}")
            return False

    def search_unseen(self) -> List[int]:
        """Busca mensajes no leídos"""
        try:
            # Asegurar que estamos conectados
            if not self._ensure_connected():
                self.logger.error("No se pudo establecer conexión para búsqueda")
                return []

            # Verificar que tengamos una carpeta seleccionada
            if not self.current_folder or self.current_folder == "":
                self.logger.debug("No hay carpeta seleccionada, seleccionando INBOX")
                if not self.select_folder("INBOX"):
                    self.logger.error("No se pudo seleccionar INBOX")
                    return []

            status, messages = self.client.search(None, 'UNSEEN')

            if status == 'OK':
                message_ids = messages[0].split()
                count = len(message_ids)
                self.logger.debug(f"Búsqueda UNSEEN exitosa: {count} mensajes")
                return [int(mid) for mid in message_ids]
            else:
                self.logger.warning(f"SEARCH retornó estado no-OK: {status}")
                return []

        except imaplib.IMAP4.abort as e:
            # Conexión abortada, intentar reconectar una vez
            self.logger.warning(f"Conexión abortada durante búsqueda: {e}")
            self.client = None  # Forzar reconexión

            if self._ensure_connected():
                self.logger.info("Reconexión exitosa, reintentando búsqueda...")
                try:
                    status, messages = self.client.search(None, 'UNSEEN')
                    if status == 'OK':
                        message_ids = messages[0].split()
                        return [int(mid) for mid in message_ids]
                    else:
                        self.logger.error(f"Búsqueda falló después de reconectar: {status}")
                except Exception as retry_error:
                    self.logger.error(f"Error en reintento de búsqueda: {retry_error}")
            else:
                self.logger.error("No se pudo reconectar después de abort")

            return []

        except Exception as e:
            self.logger.error(f"Error buscando mensajes: {e}")
            import traceback
            self.logger.debug(f"Stack trace: {traceback.format_exc()}")
            return []

    def fetch_message(self, message_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un mensaje completo"""
        try:
            # Asegurar conexión
            if not self._ensure_connected():
                return None

            # Fetch del mensaje (usando PEEK para no marcarlo como leído)
            status, data = self.client.fetch(str(message_id), '(BODY.PEEK[])')

            if status != 'OK':
                self.logger.warning(f"FETCH retornó estado {status}")
                return None

            # Validar que data tiene el formato esperado
            if not data or len(data) == 0:
                self.logger.warning(f"FETCH retornó data vacío para mensaje {message_id}")
                return None

            # Verificar que data[0] es una tupla
            if not isinstance(data[0], tuple) or len(data[0]) < 2:
                self.logger.warning(f"FETCH retornó formato inesperado para mensaje {message_id}: {type(data[0])}")
                return None

            # Extraer el contenido del mensaje
            raw_email = data[0][1]

            # Validar que raw_email es bytes
            if not isinstance(raw_email, bytes):
                self.logger.error(f"FETCH retornó tipo inesperado para mensaje {message_id}: {type(raw_email)}")
                return None

            # Parsear el mensaje
            msg = BytesParser(policy=policy.default).parsebytes(raw_email)

            # Extraer información básica
            result = {
                'id': message_id,
                'subject': str(msg.get('Subject', '')),
                'from': str(msg.get('From', '')),
                'to': str(msg.get('To', '')),
                'date': msg.get('Date'),
                'body_text': '',
                'body_html': '',
                'attachments': []
            }

            # Extraer cuerpo y adjuntos
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition', ''))

                    # Texto plano
                    if content_type == 'text/plain' and 'attachment' not in content_disposition:
                        try:
                            result['body_text'] = part.get_content()
                        except:
                            pass

                    # HTML
                    elif content_type == 'text/html' and 'attachment' not in content_disposition:
                        try:
                            result['body_html'] = part.get_content()
                        except:
                            pass

                    # Adjuntos
                    elif 'attachment' in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            try:
                                content = part.get_payload(decode=True)
                                result['attachments'].append({
                                    'filename': filename,
                                    'content': content,
                                    'size': len(content) if content else 0
                                })
                            except:
                                pass
            else:
                # Mensaje simple (no multipart)
                content_type = msg.get_content_type()
                if content_type == 'text/plain':
                    result['body_text'] = msg.get_content()
                elif content_type == 'text/html':
                    result['body_html'] = msg.get_content()

            return result

        except Exception as e:
            self.logger.error(f"Error obteniendo mensaje {message_id}: {e}")
            import traceback
            self.logger.debug(f"Stack trace: {traceback.format_exc()}")
            return None

    def mark_as_read(self, message_id: int):
        """Marca un mensaje como leído"""
        try:
            if self._ensure_connected():
                self.client.store(str(message_id), '+FLAGS', '\\Seen')
        except Exception as e:
            self.logger.error(f"Error marcando mensaje {message_id} como leído: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

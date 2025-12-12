"""
Cliente de Microsoft Graph API para acceso a correos de Office 365
Reemplaza IMAP para lectura de correos con autenticación moderna OAuth 2.0
"""
import base64
from datetime import datetime
from typing import List, Optional, Dict, Any
from email import message_from_bytes
from email.header import decode_header

from msal import ConfidentialClientApplication
from msgraph_core import GraphClient
from azure.identity import ClientSecretCredential
from loguru import logger


class GraphEmailClient:
    """
    Cliente para acceder a correos de Office 365 usando Microsoft Graph API

    Ventajas vs IMAP:
    - OAuth 2.0 (más seguro que contraseñas)
    - No requiere habilitar IMAP en Office 365
    - Permisos granulares
    - API moderna de Microsoft
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        mailbox_email: str
    ):
        """
        Inicializa el cliente de Graph API

        Args:
            client_id: Application (client) ID de Azure AD
            client_secret: Client secret value de Azure AD
            tenant_id: Directory (tenant) ID de Azure AD
            mailbox_email: Email del mailbox a acceder (ej: recordatorio.oc@hotelsales.cl)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.mailbox_email = mailbox_email

        self.logger = logger.bind(module="GraphEmailClient")
        self._graph_client: Optional[GraphClient] = None
        self._credential: Optional[ClientSecretCredential] = None

    def connect(self):
        """Establece conexión con Microsoft Graph API usando OAuth 2.0"""
        try:
            self.logger.info(f"Conectando a Microsoft Graph API para {self.mailbox_email}...")

            # Crear credencial OAuth
            self._credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )

            # Crear cliente de Graph
            self._graph_client = GraphClient(credential=self._credential)

            # Verificar acceso obteniendo el mailbox
            self._test_connection()

            self.logger.info("✅ Conexión exitosa a Microsoft Graph API")

        except Exception as e:
            self.logger.error(f"❌ Error conectando a Graph API: {e}")
            raise

    def _test_connection(self):
        """Verifica que la conexión funcione obteniendo info del mailbox"""
        try:
            # Intentar obtener información del usuario
            endpoint = f"/users/{self.mailbox_email}"
            response = self._graph_client.get(endpoint)

            if response and response.status_code == 200:
                user_data = response.json()
                self.logger.debug(f"Mailbox verificado: {user_data.get('displayName', 'N/A')}")
            else:
                raise Exception(f"No se pudo verificar acceso al mailbox: {response.status_code}")

        except Exception as e:
            raise Exception(f"Error verificando conexión: {e}")

    def get_unread_messages(
        self,
        folder: str = "inbox",
        top: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Obtiene mensajes no leídos del mailbox

        Args:
            folder: Carpeta a consultar (inbox, sent, etc)
            top: Número máximo de mensajes a obtener

        Returns:
            Lista de mensajes no leídos con metadata
        """
        try:
            self.logger.info(f"Buscando mensajes no leídos en {folder}...")

            # Endpoint para mensajes no leídos
            endpoint = f"/users/{self.mailbox_email}/mailFolders/{folder}/messages"
            params = {
                "$filter": "isRead eq false",
                "$top": top,
                "$orderby": "receivedDateTime desc",
                "$select": "id,subject,from,receivedDateTime,hasAttachments,internetMessageId"
            }

            response = self._graph_client.get(endpoint, params=params)

            if response.status_code == 200:
                data = response.json()
                messages = data.get('value', [])
                self.logger.info(f"Encontrados {len(messages)} mensajes no leídos")
                return messages
            else:
                self.logger.error(f"Error obteniendo mensajes: {response.status_code}")
                return []

        except Exception as e:
            self.logger.error(f"Error obteniendo mensajes no leídos: {e}")
            return []

    def get_message_content(self, message_id: str) -> Optional[bytes]:
        """
        Obtiene el contenido completo (MIME) del mensaje

        Args:
            message_id: ID del mensaje en Graph API

        Returns:
            Contenido MIME del mensaje en bytes, o None si falla
        """
        try:
            # Obtener contenido MIME del mensaje
            endpoint = f"/users/{self.mailbox_email}/messages/{message_id}/$value"
            response = self._graph_client.get(endpoint)

            if response.status_code == 200:
                return response.content
            else:
                self.logger.error(f"Error obteniendo contenido del mensaje: {response.status_code}")
                return None

        except Exception as e:
            self.logger.error(f"Error obteniendo contenido MIME: {e}")
            return None

    def get_message_attachments(self, message_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene los adjuntos de un mensaje

        Args:
            message_id: ID del mensaje

        Returns:
            Lista de adjuntos con metadata y contenido
        """
        try:
            endpoint = f"/users/{self.mailbox_email}/messages/{message_id}/attachments"
            response = self._graph_client.get(endpoint)

            if response.status_code == 200:
                data = response.json()
                return data.get('value', [])
            else:
                self.logger.error(f"Error obteniendo adjuntos: {response.status_code}")
                return []

        except Exception as e:
            self.logger.error(f"Error obteniendo adjuntos: {e}")
            return []

    def mark_as_read(self, message_id: str) -> bool:
        """
        Marca un mensaje como leído

        Args:
            message_id: ID del mensaje

        Returns:
            True si se marcó correctamente, False en caso contrario
        """
        try:
            endpoint = f"/users/{self.mailbox_email}/messages/{message_id}"
            body = {"isRead": True}

            response = self._graph_client.patch(endpoint, json=body)

            if response.status_code in [200, 204]:
                self.logger.debug(f"Mensaje {message_id} marcado como leído")
                return True
            else:
                self.logger.error(f"Error marcando mensaje como leído: {response.status_code}")
                return False

        except Exception as e:
            self.logger.error(f"Error marcando mensaje como leído: {e}")
            return False

    def parse_mime_message(self, mime_content: bytes) -> Any:
        """
        Parsea contenido MIME a objeto email.message.Message

        Args:
            mime_content: Contenido MIME en bytes

        Returns:
            Objeto email.message.Message parseado
        """
        return message_from_bytes(mime_content)

    def get_message_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene detalles completos de un mensaje (metadata + contenido)

        Args:
            message_id: ID del mensaje

        Returns:
            Diccionario con toda la información del mensaje
        """
        try:
            endpoint = f"/users/{self.mailbox_email}/messages/{message_id}"
            params = {
                "$expand": "attachments"
            }

            response = self._graph_client.get(endpoint, params=params)

            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Error obteniendo detalles del mensaje: {response.status_code}")
                return None

        except Exception as e:
            self.logger.error(f"Error obteniendo detalles: {e}")
            return None

    def disconnect(self):
        """Cierra la conexión (no es necesario con Graph API, pero mantenemos la interfaz)"""
        self.logger.debug("Desconectando de Graph API (no requiere acción)")
        self._graph_client = None
        self._credential = None

    @staticmethod
    def decode_attachment_content(content_bytes: str) -> bytes:
        """
        Decodifica el contenido de un adjunto de base64

        Args:
            content_bytes: Contenido en base64 string

        Returns:
            Contenido decodificado en bytes
        """
        return base64.b64decode(content_bytes)

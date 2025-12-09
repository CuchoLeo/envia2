"""
Configuración central del sistema de seguimiento de OC
Carga variables de entorno y proporciona configuración validada
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import EmailStr, Field, validator
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Settings(BaseSettings):
    """Configuración general del sistema"""

    # General
    app_name: str = Field(default="Sistema de Seguimiento OC", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Base de datos
    database_url: str = Field(
        default="sqlite:///./data/oc_seguimiento.db",
        env="DATABASE_URL"
    )

    # IMAP - Monitoreo de confirmaciones
    imap_host: str = Field(env="IMAP_HOST")
    imap_port: int = Field(default=993, env="IMAP_PORT")
    imap_username: str = Field(env="IMAP_USERNAME")
    imap_password: str = Field(env="IMAP_PASSWORD")
    imap_mailbox: str = Field(default="INBOX", env="IMAP_MAILBOX")
    imap_use_ssl: bool = Field(default=True, env="IMAP_USE_SSL")
    imap_check_interval: int = Field(default=300, env="IMAP_CHECK_INTERVAL")

    # SMTP - Envío de correos
    smtp_host: str = Field(env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: str = Field(env="SMTP_USERNAME")
    smtp_password: str = Field(env="SMTP_PASSWORD")
    smtp_from_email: EmailStr = Field(env="SMTP_FROM_EMAIL")
    smtp_from_name: str = Field(
        default="Kontrol Travel - Administración",
        env="SMTP_FROM_NAME"
    )
    smtp_use_tls: bool = Field(default=True, env="SMTP_USE_TLS")

    # IMAP - Recepción de OC
    oc_inbox_host: str = Field(env="OC_INBOX_HOST")
    oc_inbox_port: int = Field(default=993, env="OC_INBOX_PORT")
    oc_inbox_username: str = Field(env="OC_INBOX_USERNAME")
    oc_inbox_password: str = Field(env="OC_INBOX_PASSWORD")
    oc_inbox_mailbox: str = Field(default="INBOX", env="OC_INBOX_MAILBOX")
    oc_inbox_use_ssl: bool = Field(default=True, env="OC_INBOX_USE_SSL")
    oc_check_interval: int = Field(default=300, env="OC_CHECK_INTERVAL")

    # Scheduler
    scheduler_check_hour: int = Field(default=9, env="SCHEDULER_CHECK_HOUR")
    scheduler_check_minute: int = Field(default=0, env="SCHEDULER_CHECK_MINUTE")
    scheduler_checks_per_day: int = Field(default=4, env="SCHEDULER_CHECKS_PER_DAY")

    # Web
    web_host: str = Field(default="0.0.0.0", env="WEB_HOST")
    web_port: int = Field(default=8001, env="WEB_PORT")
    web_reload: bool = Field(default=True, env="WEB_RELOAD")

    # Admin
    admin_username: str = Field(default="admin", env="ADMIN_USERNAME")
    admin_password: str = Field(default="changeme123", env="ADMIN_PASSWORD")

    # Configuración de correos
    email_cc_recipients: str = Field(
        default="administracion@ideasfractal.com",
        env="EMAIL_CC_RECIPIENTS"
    )
    days_for_reminder_1: int = Field(default=2, env="DAYS_FOR_REMINDER_1")
    days_for_reminder_2: int = Field(default=4, env="DAYS_FOR_REMINDER_2")

    # Remitentes autorizados para confirmaciones
    allowed_confirmation_senders: str = Field(
        default="reservasonline@hotelsales.cl",
        env="ALLOWED_CONFIRMATION_SENDERS"
    )

    # Clientes que requieren OC
    agencies_requiring_oc: str = Field(
        default="WALVIS S.A.",
        env="AGENCIES_REQUIRING_OC"
    )

    # Google Cloud (opcional)
    gcp_project_id: str = Field(default="", env="GCP_PROJECT_ID")
    gcp_bucket_name: str = Field(default="", env="GCP_BUCKET_NAME")
    google_application_credentials: str = Field(
        default="",
        env="GOOGLE_APPLICATION_CREDENTIALS"
    )

    # Notificaciones (opcional)
    slack_webhook_url: str = Field(default="", env="SLACK_WEBHOOK_URL")
    system_notification_email: str = Field(
        default="",
        env="SYSTEM_NOTIFICATION_EMAIL"
    )

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cc_recipients_list(self) -> List[str]:
        """Retorna lista de destinatarios CC"""
        return [
            email.strip()
            for email in self.email_cc_recipients.split(",")
            if email.strip()
        ]

    @property
    def agencies_list(self) -> List[str]:
        """Retorna lista de agencias que requieren OC"""
        return [
            agency.strip()
            for agency in self.agencies_requiring_oc.split(",")
            if agency.strip()
        ]

    @property
    def allowed_senders_list(self) -> List[str]:
        """Retorna lista de remitentes autorizados para confirmaciones"""
        return [
            sender.strip().lower()
            for sender in self.allowed_confirmation_senders.split(",")
            if sender.strip()
        ]

    def requires_oc(self, agency_name: str) -> bool:
        """Verifica si una agencia requiere seguimiento de OC"""
        return agency_name.strip() in self.agencies_list

    def is_sender_allowed(self, sender_email: str) -> bool:
        """Verifica si un remitente está autorizado para enviar confirmaciones"""
        return sender_email.strip().lower() in self.allowed_senders_list


# Instancia global de configuración
settings = Settings()


# Validaciones adicionales
def validate_config():
    """Valida que la configuración sea correcta"""
    errors = []

    # Validar configuración IMAP
    if not settings.imap_host or not settings.imap_username:
        errors.append("Configuración IMAP incompleta")

    # Validar configuración SMTP
    if not settings.smtp_host or not settings.smtp_username:
        errors.append("Configuración SMTP incompleta")

    # Validar que haya al menos una agencia configurada
    if not settings.agencies_list:
        errors.append("No hay agencias configuradas que requieran OC")

    if errors:
        raise ValueError(f"Errores de configuración: {', '.join(errors)}")

    return True


if __name__ == "__main__":
    # Test de configuración
    print("=== Configuración del Sistema ===")
    print(f"Aplicación: {settings.app_name} v{settings.app_version}")
    print(f"Entorno: {settings.environment}")
    print(f"Base de datos: {settings.database_url}")
    print(f"IMAP Monitor: {settings.imap_host}:{settings.imap_port}")
    print(f"SMTP Envío: {settings.smtp_host}:{settings.smtp_port}")
    print(f"Agencias con OC: {', '.join(settings.agencies_list)}")

    try:
        validate_config()
        print("\n✅ Configuración válida")
    except ValueError as e:
        print(f"\n❌ {e}")

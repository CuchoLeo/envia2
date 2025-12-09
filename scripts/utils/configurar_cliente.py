#!/usr/bin/env python3
"""
Script de configuración interactiva para nuevo cliente
Genera el archivo .env con la información del cliente
"""
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import init_db, get_db, ConfiguracionCliente

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Imprime el encabezado"""
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.CYAN}🔧 CONFIGURACIÓN DE CLIENTE - SISTEMA DE SEGUIMIENTO OC{Colors.RESET}")
    print("="*70)
    print(f"{Colors.YELLOW}Este script te guiará para configurar el sistema para un nuevo cliente{Colors.RESET}\n")

def input_required(prompt, default=None):
    """Input que no acepta valores vacíos"""
    while True:
        if default:
            value = input(f"{Colors.BOLD}{prompt} [{default}]: {Colors.RESET}").strip()
            if not value:
                return default
            return value
        else:
            value = input(f"{Colors.BOLD}{prompt}: {Colors.RESET}").strip()
            if value:
                return value
            print(f"{Colors.RED}⚠️  Este campo es obligatorio{Colors.RESET}")

def input_yes_no(prompt, default=True):
    """Input si/no"""
    default_str = "S/n" if default else "s/N"
    value = input(f"{Colors.BOLD}{prompt} [{default_str}]: {Colors.RESET}").strip().lower()
    if not value:
        return default
    return value in ['s', 'si', 'sí', 'y', 'yes']

def configurar_correos():
    """Configura las cuentas de correo"""
    print(f"\n{Colors.CYAN}📧 CONFIGURACIÓN DE CORREOS{Colors.RESET}\n")

    una_cuenta = input_yes_no("¿Usar una sola cuenta para todo?", True)

    if una_cuenta:
        print(f"\n{Colors.BLUE}Usando una cuenta para IMAP y SMTP{Colors.RESET}")
        email = input_required("Email de Gmail (ej: admin.tuempresa@gmail.com)")
        password = input_required("Contraseña de aplicación de Gmail (16 caracteres)")

        return {
            'imap_host': 'imap.gmail.com',
            'imap_port': 993,
            'imap_username': email,
            'imap_password': password,
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_username': email,
            'smtp_password': password,
            'smtp_from_email': email,
            'oc_inbox_username': email,
            'oc_inbox_password': password,
        }
    else:
        print(f"\n{Colors.BLUE}Configuración separada de cuentas{Colors.RESET}")

        print("\n📥 Cuenta Gmail para RECIBIR confirmaciones:")
        imap_email = input_required("Email de Gmail")
        imap_password = input_required("Contraseña de aplicación (16 caracteres)")

        print("\n📤 Cuenta Gmail para ENVIAR solicitudes:")
        smtp_email = input_required("Email de Gmail")
        smtp_password = input_required("Contraseña de aplicación (16 caracteres)")

        usar_misma_oc = input_yes_no("¿Usar la misma cuenta SMTP para recibir OC?", True)

        if usar_misma_oc:
            oc_email = smtp_email
            oc_password = smtp_password
        else:
            print("\n📬 Cuenta Gmail para RECIBIR OC:")
            oc_email = input_required("Email de Gmail")
            oc_password = input_required("Contraseña de aplicación (16 caracteres)")

        return {
            'imap_host': 'imap.gmail.com',
            'imap_port': 993,
            'imap_username': imap_email,
            'imap_password': imap_password,
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_username': smtp_email,
            'smtp_password': smtp_password,
            'smtp_from_email': smtp_email,
            'oc_inbox_username': oc_email,
            'oc_inbox_password': oc_password,
        }

def configurar_empresa():
    """Configura información de la empresa"""
    print(f"\n{Colors.CYAN}🏢 INFORMACIÓN DE LA EMPRESA{Colors.RESET}\n")

    nombre = input_required("Nombre de la empresa", "Kontrol Travel")
    nombre_firma = input_required("Nombre para firma de emails", f"{nombre} - Administración")

    return {
        'app_name': nombre,
        'smtp_from_name': nombre_firma,
    }

def configurar_recordatorios():
    """Configura días de recordatorios"""
    print(f"\n{Colors.CYAN}⏰ CONFIGURACIÓN DE RECORDATORIOS{Colors.RESET}\n")

    dias_rec1 = input_required("Días para 1er recordatorio", "2")
    dias_rec2 = input_required("Días para 2do recordatorio", "4")

    return {
        'days_for_reminder_1': int(dias_rec1),
        'days_for_reminder_2': int(dias_rec2),
    }

def configurar_cc():
    """Configura emails en copia"""
    print(f"\n{Colors.CYAN}📬 EMAILS EN COPIA (CC){Colors.RESET}\n")

    emails_cc = []

    while True:
        email = input(f"{Colors.BOLD}Email para CC (Enter para terminar): {Colors.RESET}").strip()
        if not email:
            break
        emails_cc.append(email)
        print(f"  ✅ {email}")

    return {
        'email_cc_recipients': ','.join(emails_cc) if emails_cc else '',
    }

def configurar_agencias():
    """Configura las agencias que requieren OC"""
    print(f"\n{Colors.CYAN}🏢 AGENCIAS QUE REQUIEREN OC{Colors.RESET}\n")
    print(f"{Colors.YELLOW}Las agencias se configurarán después en la base de datos{Colors.RESET}")
    print(f"{Colors.YELLOW}Por ahora, lista los nombres separados por comas:{Colors.RESET}\n")

    agencias_str = input_required(
        "Nombres de agencias (separadas por comas)",
        "WALVIS S.A.,EMPRESA CORPORATIVA LTDA"
    )

    return {
        'agencies_requiring_oc': agencias_str,
    }

def generar_env(config):
    """Genera el archivo .env"""
    env_content = f"""# Configuración del Cliente - Generado automáticamente
# Fecha: {Path(__file__).stat().st_mtime}

# ============================================================================
# GENERAL
# ============================================================================
APP_NAME="{config['app_name']}"
APP_VERSION="1.0.0"
ENVIRONMENT="production"
DEBUG=false
LOG_LEVEL="INFO"

# ============================================================================
# BASE DE DATOS
# ============================================================================
DATABASE_URL="sqlite:///./data/oc_seguimiento.db"

# ============================================================================
# IMAP - Monitoreo de Confirmaciones de Reserva
# ============================================================================
IMAP_HOST="{config['imap_host']}"
IMAP_PORT={config['imap_port']}
IMAP_USERNAME="{config['imap_username']}"
IMAP_PASSWORD="{config['imap_password']}"
IMAP_MAILBOX="INBOX"
IMAP_USE_SSL=true
IMAP_CHECK_INTERVAL=300

# ============================================================================
# SMTP - Envío de Correos
# ============================================================================
SMTP_HOST="{config['smtp_host']}"
SMTP_PORT={config['smtp_port']}
SMTP_USERNAME="{config['smtp_username']}"
SMTP_PASSWORD="{config['smtp_password']}"
SMTP_FROM_EMAIL="{config['smtp_from_email']}"
SMTP_FROM_NAME="{config['smtp_from_name']}"
SMTP_USE_TLS=true

# ============================================================================
# IMAP - Recepción de Órdenes de Compra
# ============================================================================
OC_INBOX_HOST="{config['imap_host']}"
OC_INBOX_PORT={config['imap_port']}
OC_INBOX_USERNAME="{config['oc_inbox_username']}"
OC_INBOX_PASSWORD="{config['oc_inbox_password']}"
OC_INBOX_MAILBOX="INBOX"
OC_INBOX_USE_SSL=true
OC_CHECK_INTERVAL=300

# ============================================================================
# SCHEDULER
# ============================================================================
SCHEDULER_CHECK_HOUR=9
SCHEDULER_CHECK_MINUTE=0
SCHEDULER_CHECKS_PER_DAY=4

# ============================================================================
# WEB SERVER
# ============================================================================
WEB_HOST="0.0.0.0"
WEB_PORT=8001
WEB_RELOAD=false

# ============================================================================
# ADMINISTRACIÓN
# ============================================================================
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="changeme123"

# ============================================================================
# CONFIGURACIÓN DE CORREOS
# ============================================================================
EMAIL_CC_RECIPIENTS="{config.get('email_cc_recipients', '')}"
DAYS_FOR_REMINDER_1={config['days_for_reminder_1']}
DAYS_FOR_REMINDER_2={config['days_for_reminder_2']}

# ============================================================================
# CLIENTES QUE REQUIEREN OC (separados por comas)
# ============================================================================
AGENCIES_REQUIRING_OC="{config['agencies_requiring_oc']}"

# ============================================================================
# GOOGLE CLOUD (Opcional)
# ============================================================================
GCP_PROJECT_ID=""
GCP_BUCKET_NAME=""
GOOGLE_APPLICATION_CREDENTIALS=""

# ============================================================================
# NOTIFICACIONES (Opcional)
# ============================================================================
SLACK_WEBHOOK_URL=""
SYSTEM_NOTIFICATION_EMAIL=""
"""
    return env_content

def crear_agencias_bd(agencias_str):
    """Crea las agencias en la base de datos"""
    print(f"\n{Colors.CYAN}💾 CREANDO AGENCIAS EN BASE DE DATOS{Colors.RESET}\n")

    init_db()
    db = next(get_db())

    agencias = [a.strip() for a in agencias_str.split(',')]

    try:
        for nombre_agencia in agencias:
            # Verificar si ya existe
            existe = db.query(ConfiguracionCliente).filter_by(
                nombre_agencia=nombre_agencia
            ).first()

            if existe:
                print(f"  ⚠️  {nombre_agencia} ya existe, saltando...")
                continue

            # Crear configuración
            config = ConfiguracionCliente(
                nombre_agencia=nombre_agencia,
                email_contacto=None,  # Se configurará después
                requiere_oc=True,
                activo=True,
                dias_recordatorio_1=2,
                dias_recordatorio_2=4,
            )

            db.add(config)
            print(f"  ✅ {nombre_agencia}")

        db.commit()
        print(f"\n{Colors.GREEN}✅ Agencias creadas exitosamente{Colors.RESET}")

    except Exception as e:
        db.rollback()
        print(f"\n{Colors.RED}❌ Error creando agencias: {e}{Colors.RESET}")
    finally:
        db.close()

def main():
    """Función principal"""
    print_header()

    # Recopilar configuración
    config = {}

    # 1. Correos
    config.update(configurar_correos())

    # 2. Empresa
    config.update(configurar_empresa())

    # 3. Recordatorios
    config.update(configurar_recordatorios())

    # 4. CC
    config.update(configurar_cc())

    # 5. Agencias
    config.update(configurar_agencias())

    # Resumen
    print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}📋 RESUMEN DE CONFIGURACIÓN{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

    print(f"Empresa: {config['app_name']}")
    print(f"Email IMAP: {config['imap_username']}")
    print(f"Email SMTP: {config['smtp_username']}")
    print(f"Email OC: {config['oc_inbox_username']}")
    print(f"Recordatorio 1: {config['days_for_reminder_1']} días")
    print(f"Recordatorio 2: {config['days_for_reminder_2']} días")
    print(f"CC: {config.get('email_cc_recipients', 'Ninguno')}")
    print(f"Agencias: {config['agencies_requiring_oc']}")

    # Confirmar
    print()
    if not input_yes_no("¿Confirmas la configuración?", True):
        print(f"\n{Colors.YELLOW}❌ Configuración cancelada{Colors.RESET}\n")
        sys.exit(0)

    # Generar .env
    print(f"\n{Colors.CYAN}💾 GENERANDO ARCHIVO .env{Colors.RESET}\n")

    env_path = Path(__file__).parent.parent / '.env'

    # Backup si existe
    if env_path.exists():
        backup_path = env_path.with_suffix('.env.backup')
        env_path.rename(backup_path)
        print(f"  ✅ Backup creado: .env.backup")

    # Escribir nuevo .env
    env_content = generar_env(config)
    env_path.write_text(env_content)
    print(f"  ✅ Archivo .env creado")

    # Crear agencias en BD
    crear_agencias_bd(config['agencies_requiring_oc'])

    # Mensaje final
    print(f"\n{Colors.GREEN}{'='*70}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}✅ CONFIGURACIÓN COMPLETADA{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*70}{Colors.RESET}\n")

    print(f"{Colors.BLUE}📋 Próximos pasos:{Colors.RESET}")
    print("  1. Revisar y editar .env si es necesario")
    print("  2. Configurar emails de contacto de agencias:")
    print(f"     {Colors.YELLOW}python3 scripts/configurar_agencias_contactos.py{Colors.RESET}")
    print("  3. Probar conexión IMAP/SMTP:")
    print(f"     {Colors.YELLOW}python3 scripts/test_conexion.py{Colors.RESET}")
    print("  4. Iniciar el servidor:")
    print(f"     {Colors.YELLOW}python3 app.py{Colors.RESET}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}❌ Configuración cancelada{Colors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error inesperado: {e}{Colors.RESET}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

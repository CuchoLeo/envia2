#!/usr/bin/env python3
"""
Script para verificar que todas las conexiones funcionan correctamente
antes de pasar a pruebas con el cliente
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.imap_wrapper import SimpleIMAPClient
from config import settings
import smtplib

# Colores
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def test_imap_confirmaciones():
    """Test conexión IMAP para confirmaciones"""
    print(f"\n{Colors.CYAN}📥 TEST 1: IMAP - Recepción de Confirmaciones{Colors.RESET}")
    print(f"   Host: {settings.imap_host}:{settings.imap_port}")
    print(f"   Usuario: {settings.imap_username}")

    try:
        client = SimpleIMAPClient(
            host=settings.imap_host,
            port=settings.imap_port,
            username=settings.imap_username,
            password=settings.imap_password,
            use_ssl=settings.imap_use_ssl
        )
        client.connect()

        # Contar emails
        emails = client.get_unread_message_ids()
        client.disconnect()

        print(f"   {Colors.GREEN}✅ Conexión exitosa{Colors.RESET}")
        print(f"   📧 {len(emails)} correos no leídos")
        return True

    except Exception as e:
        print(f"   {Colors.RED}❌ Error: {e}{Colors.RESET}")
        return False

def test_imap_oc():
    """Test conexión IMAP para OC"""
    print(f"\n{Colors.CYAN}📬 TEST 2: IMAP - Recepción de Órdenes de Compra{Colors.RESET}")
    print(f"   Host: {settings.oc_inbox_host}:{settings.oc_inbox_port}")
    print(f"   Usuario: {settings.oc_inbox_username}")

    try:
        client = SimpleIMAPClient(
            host=settings.oc_inbox_host,
            port=settings.oc_inbox_port,
            username=settings.oc_inbox_username,
            password=settings.oc_inbox_password,
            use_ssl=settings.oc_inbox_use_ssl
        )
        client.connect()

        emails = client.get_unread_message_ids()
        client.disconnect()

        print(f"   {Colors.GREEN}✅ Conexión exitosa{Colors.RESET}")
        print(f"   📧 {len(emails)} correos no leídos")
        return True

    except Exception as e:
        print(f"   {Colors.RED}❌ Error: {e}{Colors.RESET}")
        return False

def test_smtp():
    """Test conexión SMTP"""
    print(f"\n{Colors.CYAN}📤 TEST 3: SMTP - Envío de Correos{Colors.RESET}")
    print(f"   Host: {settings.smtp_host}:{settings.smtp_port}")
    print(f"   Usuario: {settings.smtp_username}")

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            if settings.smtp_use_tls:
                server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)

        print(f"   {Colors.GREEN}✅ Conexión y autenticación exitosa{Colors.RESET}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"   {Colors.RED}❌ Error de autenticación: {e}{Colors.RESET}")
        print(f"   {Colors.YELLOW}💡 Verifica que la contraseña de aplicación sea correcta{Colors.RESET}")
        return False
    except Exception as e:
        print(f"   {Colors.RED}❌ Error: {e}{Colors.RESET}")
        return False

def test_database():
    """Test base de datos"""
    print(f"\n{Colors.CYAN}💾 TEST 4: Base de Datos{Colors.RESET}")

    try:
        from database import init_db, get_db, Reserva, ConfiguracionCliente

        init_db()
        print(f"   {Colors.GREEN}✅ Base de datos inicializada{Colors.RESET}")

        db = next(get_db())
        try:
            # Contar registros
            total_reservas = db.query(Reserva).count()
            total_clientes = db.query(ConfiguracionCliente).count()

            print(f"   📊 {total_reservas} reservas en BD")
            print(f"   🏢 {total_clientes} clientes configurados")

            # Listar clientes
            if total_clientes > 0:
                print(f"\n   {Colors.BLUE}Clientes configurados:{Colors.RESET}")
                clientes = db.query(ConfiguracionCliente).all()
                for c in clientes:
                    email_info = c.email_contacto if c.email_contacto else "sin email"
                    print(f"     • {c.nombre_agencia} ({email_info})")

            return True
        finally:
            db.close()

    except Exception as e:
        print(f"   {Colors.RED}❌ Error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        return False

def test_templates():
    """Test templates de email"""
    print(f"\n{Colors.CYAN}📄 TEST 5: Templates de Email{Colors.RESET}")

    try:
        from src.email_sender import EmailSender

        sender = EmailSender()

        # Verificar que los templates existan
        templates = [
            'solicitud_inicial.html',
            'recordatorio_dia2.html',
            'ultimatum_dia4.html'
        ]

        all_ok = True
        for template in templates:
            try:
                sender.jinja_env.get_template(template)
                print(f"   {Colors.GREEN}✅{Colors.RESET} {template}")
            except Exception as e:
                print(f"   {Colors.RED}❌{Colors.RESET} {template} - {e}")
                all_ok = False

        return all_ok

    except Exception as e:
        print(f"   {Colors.RED}❌ Error: {e}{Colors.RESET}")
        return False

def test_config():
    """Test configuración general"""
    print(f"\n{Colors.CYAN}⚙️  TEST 6: Configuración General{Colors.RESET}")

    try:
        print(f"   App: {settings.app_name}")
        print(f"   Env: {settings.environment}")
        print(f"   Debug: {settings.debug}")
        print(f"   Web: {settings.web_host}:{settings.web_port}")
        print(f"   CC: {settings.email_cc_recipients if settings.email_cc_recipients else 'Ninguno'}")
        print(f"   Recordatorio 1: {settings.days_for_reminder_1} días")
        print(f"   Recordatorio 2: {settings.days_for_reminder_2} días")

        print(f"\n   {Colors.BLUE}Agencias que requieren OC:{Colors.RESET}")
        for agencia in settings.agencies_requiring_oc:
            print(f"     • {agencia}")

        print(f"   {Colors.GREEN}✅ Configuración cargada{Colors.RESET}")
        return True

    except Exception as e:
        print(f"   {Colors.RED}❌ Error: {e}{Colors.RESET}")
        return False

def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.CYAN}🧪 TEST DE CONEXIONES - SISTEMA OC{Colors.RESET}")
    print("="*70)

    # Cargar .env
    load_dotenv()

    # Ejecutar tests
    results = {
        'IMAP Confirmaciones': test_imap_confirmaciones(),
        'IMAP OC': test_imap_oc(),
        'SMTP': test_smtp(),
        'Base de Datos': test_database(),
        'Templates': test_templates(),
        'Configuración': test_config(),
    }

    # Resumen
    print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}📊 RESUMEN{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if result else f"{Colors.RED}❌ FAIL{Colors.RESET}"
        print(f"  {status}  {test_name}")

    print()
    print(f"  Total: {passed}/{total} tests pasados")

    # Resultado final
    if passed == total:
        print(f"\n{Colors.GREEN}{'='*70}{Colors.RESET}")
        print(f"{Colors.GREEN}{Colors.BOLD}✅ TODOS LOS TESTS PASARON - SISTEMA LISTO{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*70}{Colors.RESET}\n")
        print(f"{Colors.BLUE}Próximo paso:{Colors.RESET}")
        print(f"  python3 app.py  {Colors.YELLOW}# Iniciar el servidor{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{'='*70}{Colors.RESET}")
        print(f"{Colors.RED}{Colors.BOLD}❌ ALGUNOS TESTS FALLARON{Colors.RESET}")
        print(f"{Colors.RED}{'='*70}{Colors.RESET}\n")
        print(f"{Colors.YELLOW}Por favor, corrige los errores antes de continuar{Colors.RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}❌ Tests cancelados{Colors.RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error inesperado: {e}{Colors.RESET}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

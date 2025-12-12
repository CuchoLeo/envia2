#!/usr/bin/env python3
"""
Script de prueba para verificar conexión a Microsoft Graph API
Reemplazo de IMAP para acceso a correos de Office 365
"""
import sys
import smtplib
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from src.graph_email_client import GraphEmailClient

def test_graph_api_connection():
    """Prueba conexión a Microsoft Graph API"""
    print("\n" + "="*60)
    print("PRUEBA DE CONEXIÓN MICROSOFT GRAPH API")
    print("="*60)
    print(f"Tenant ID: {settings.azure_tenant_id[:8]}...")
    print(f"Client ID: {settings.azure_client_id[:8]}...")
    print(f"Mailbox: {settings.graph_mailbox_email}")
    print()

    try:
        # Verificar que las credenciales estén configuradas
        if not settings.azure_client_id or not settings.azure_client_secret or not settings.azure_tenant_id:
            print("❌ ERROR: Faltan credenciales de Azure AD en .env")
            print()
            print("Debes configurar:")
            print("  AZURE_CLIENT_ID=...")
            print("  AZURE_CLIENT_SECRET=...")
            print("  AZURE_TENANT_ID=...")
            print("  GRAPH_MAILBOX_EMAIL=...")
            print()
            print("Consulta: docs/CONFIGURAR_AZURE_AD_GRAPH_API.md")
            return False

        # Crear cliente de Graph
        client = GraphEmailClient(
            client_id=settings.azure_client_id,
            client_secret=settings.azure_client_secret,
            tenant_id=settings.azure_tenant_id,
            mailbox_email=settings.graph_mailbox_email
        )

        # Conectar
        print("Conectando a Microsoft Graph API...")
        client.connect()
        print("✅ Autenticación OAuth 2.0 exitosa")
        print()

        # Obtener mensajes no leídos
        print("Probando lectura de correos no leídos...")
        messages = client.get_unread_messages(top=5)
        print(f"✅ Lectura exitosa: {len(messages)} mensajes no leídos encontrados")
        print()

        # Mostrar algunos mensajes
        if messages:
            print("Últimos 5 mensajes no leídos:")
            for idx, msg in enumerate(messages[:5], 1):
                from_addr = msg.get('from', {}).get('emailAddress', {})
                from_name = from_addr.get('name', 'N/A')
                from_email = from_addr.get('address', 'N/A')
                subject = msg.get('subject', 'Sin asunto')
                date = msg.get('receivedDateTime', 'N/A')

                print(f"\n{idx}. {subject}")
                print(f"   De: {from_name} <{from_email}>")
                print(f"   Fecha: {date}")
                print(f"   Adjuntos: {'Sí' if msg.get('hasAttachments') else 'No'}")
        print()

        # Desconectar
        client.disconnect()

        return True

    except Exception as e:
        print(f"\n❌ Error en conexión Graph API: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("Pasos para resolver:")
        print("1. Verifica que la aplicación esté registrada en Azure AD")
        print("2. Verifica que los permisos estén otorgados (Grant admin consent)")
        print("3. Verifica que la Application Access Policy esté configurada")
        print()
        print("Consulta: docs/CONFIGURAR_AZURE_AD_GRAPH_API.md")
        return False


def test_smtp_connection():
    """Prueba conexión SMTP a Office 365 (sigue usando SMTP para envío)"""
    print("\n" + "="*60)
    print("PRUEBA DE CONEXIÓN SMTP (Office 365)")
    print("="*60)
    print(f"Host: {settings.smtp_host}")
    print(f"Puerto: {settings.smtp_port}")
    print(f"Usuario: {settings.smtp_username}")
    print(f"TLS: {settings.smtp_use_tls}")
    print()

    try:
        # Conectar con TLS
        server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
        server.set_debuglevel(0)
        server.ehlo()

        if settings.smtp_use_tls:
            server.starttls()
            server.ehlo()

        # Autenticar
        server.login(settings.smtp_username, settings.smtp_password)
        print("✅ Autenticación SMTP exitosa")
        print()

        server.quit()
        return True

    except Exception as e:
        print(f"❌ Error en conexión SMTP: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🔍 PRUEBA DE CONEXIÓN A MICROSOFT 365 CON GRAPH API")
    print("="*60)
    print()
    print("Este script verifica:")
    print("  1. Autenticación OAuth 2.0 con Azure AD")
    print("  2. Acceso al mailbox via Microsoft Graph API")
    print("  3. Lectura de correos no leídos")
    print("  4. Envío de correos via SMTP (Office 365)")
    print()

    graph_ok = test_graph_api_connection()
    smtp_ok = test_smtp_connection()

    print("="*60)
    print("RESUMEN")
    print("="*60)
    print(f"Microsoft Graph API: {'✅ OK' if graph_ok else '❌ FALLÓ'}")
    print(f"SMTP: {'✅ OK' if smtp_ok else '❌ FALLÓ'}")
    print()

    if graph_ok and smtp_ok:
        print("✅ Todas las conexiones funcionan correctamente")
        print()
        print("Próximos pasos:")
        print("  1. El sistema está listo para usar Graph API")
        print("  2. Ejecuta: python app.py")
        print()
        sys.exit(0)
    else:
        print("❌ Algunas conexiones fallaron")
        print()
        print("Por favor:")
        print("  1. Revisa la configuración en .env")
        print("  2. Consulta: docs/CONFIGURAR_AZURE_AD_GRAPH_API.md")
        print("  3. Verifica permisos en Azure AD")
        print()
        sys.exit(1)

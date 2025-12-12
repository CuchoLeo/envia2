#!/usr/bin/env python3
"""
Script de prueba para verificar conexión a Office 365
"""
import sys
import imaplib
import smtplib
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from config import settings

def test_imap_connection():
    """Prueba conexión IMAP a Office 365"""
    print("\n" + "="*60)
    print("PRUEBA DE CONEXIÓN IMAP (Office 365)")
    print("="*60)
    print(f"Host: {settings.imap_host}")
    print(f"Puerto: {settings.imap_port}")
    print(f"Usuario: {settings.imap_username}")
    print(f"SSL: {settings.imap_use_ssl}")

    try:
        # Conectar con SSL
        mail = imaplib.IMAP4_SSL(settings.imap_host, settings.imap_port)

        # Autenticar
        mail.login(settings.imap_username, settings.imap_password)
        print("\n✅ Autenticación IMAP exitosa")

        # Seleccionar INBOX
        status, messages = mail.select(settings.imap_mailbox)
        if status == 'OK':
            print(f"✅ Mailbox '{settings.imap_mailbox}' seleccionado correctamente")
            print(f"   Total de mensajes: {messages[0].decode()}")

        mail.logout()
        return True

    except Exception as e:
        print(f"\n❌ Error en conexión IMAP: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_smtp_connection():
    """Prueba conexión SMTP a Office 365"""
    print("\n" + "="*60)
    print("PRUEBA DE CONEXIÓN SMTP (Office 365)")
    print("="*60)
    print(f"Host: {settings.smtp_host}")
    print(f"Puerto: {settings.smtp_port}")
    print(f"Usuario: {settings.smtp_username}")
    print(f"TLS: {settings.smtp_use_tls}")

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
        print("\n✅ Autenticación SMTP exitosa")

        server.quit()
        return True

    except Exception as e:
        print(f"\n❌ Error en conexión SMTP: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🔍 PRUEBA DE CONEXIÓN A OFFICE 365")
    print("="*60)

    imap_ok = test_imap_connection()
    smtp_ok = test_smtp_connection()

    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    print(f"IMAP: {'✅ OK' if imap_ok else '❌ FALLÓ'}")
    print(f"SMTP: {'✅ OK' if smtp_ok else '❌ FALLÓ'}")

    if imap_ok and smtp_ok:
        print("\n✅ Todas las conexiones funcionan correctamente")
        sys.exit(0)
    else:
        print("\n❌ Algunas conexiones fallaron")
        sys.exit(1)

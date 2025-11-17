#!/usr/bin/env python3
"""
Script de prueba para conexión IMAP
Verifica que las credenciales y conexión IMAP funcionen correctamente
"""
import sys
import ssl
from dotenv import load_dotenv
import os

print("=" * 60)
print("🧪 Test de Conexión IMAP")
print("=" * 60)
print()

# Cargar configuración
load_dotenv()

imap_host = os.getenv('IMAP_HOST', 'imap.gmail.com')
imap_port = int(os.getenv('IMAP_PORT', '993'))
imap_user = os.getenv('IMAP_USERNAME')
imap_pass = os.getenv('IMAP_PASSWORD')

if not imap_user or not imap_pass:
    print("❌ Error: Credenciales IMAP no configuradas en .env")
    print("💡 Edita el archivo .env con IMAP_USERNAME e IMAP_PASSWORD")
    sys.exit(1)

print(f"Host: {imap_host}:{imap_port}")
print(f"Usuario: {imap_user}")
print(f"Password: {'*' * (len(imap_pass) - 4) + imap_pass[-4:]}")
print()

# Test 1: Importar IMAPClient
print("📦 Test 1: Importando IMAPClient...")
try:
    from imapclient import IMAPClient
    print("✅ IMAPClient importado correctamente")
except ImportError as e:
    print(f"❌ Error importando IMAPClient: {e}")
    print("💡 Ejecuta: pip install --upgrade imapclient")
    sys.exit(1)

print()

# Test 2: Conectar con IMAPClient
print("🔌 Test 2: Conectando con IMAPClient...")
try:
    # Crear contexto SSL
    ssl_context = ssl.create_default_context()

    # Intentar conexión
    client = IMAPClient(
        imap_host,
        port=imap_port,
        ssl=True,
        ssl_context=ssl_context
    )

    print("✅ Socket SSL creado")

    # Intentar login
    print("🔐 Autenticando...")
    client.login(imap_user, imap_pass)
    print("✅ Autenticación exitosa")

    # Seleccionar carpeta
    print("📂 Seleccionando INBOX...")
    client.select_folder('INBOX')
    print("✅ INBOX seleccionado")

    # Contar mensajes
    print("📊 Obteniendo información...")
    messages = client.search(['ALL'])
    print(f"✅ Total de mensajes en INBOX: {len(messages)}")

    # Buscar mensajes no leídos
    unread = client.search(['UNSEEN'])
    print(f"✅ Mensajes no leídos: {len(unread)}")

    # Cerrar conexión
    client.logout()
    print("✅ Conexión cerrada correctamente")

    print()
    print("=" * 60)
    print("🎉 ¡Conexión IMAP funcionando perfectamente!")
    print("=" * 60)
    print()
    print("📝 Próximo paso: Ejecuta python app.py")

    sys.exit(0)

except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("=" * 60)
    print("🔍 Diagnóstico de Errores Comunes:")
    print("=" * 60)
    print()

    error_str = str(e).lower()

    if 'authentication' in error_str or 'invalid credentials' in error_str:
        print("❌ Error de Autenticación")
        print()
        print("Soluciones:")
        print("1. Verifica que uses CONTRASEÑA DE APLICACIÓN, no tu contraseña normal")
        print("2. Genera una nueva contraseña de aplicación:")
        print("   https://myaccount.google.com/apppasswords")
        print("3. Verifica que la contraseña NO tenga espacios en .env")
        print("4. Copia y pega la contraseña directamente")

    elif 'ssl' in error_str or 'certificate' in error_str:
        print("❌ Error de SSL/Certificado")
        print()
        print("Soluciones:")
        print("1. Actualiza IMAPClient: pip install --upgrade imapclient")
        print("2. Verifica conexión a internet")
        print("3. Intenta desactivar antivirus/firewall temporalmente")

    elif 'timeout' in error_str or 'timed out' in error_str:
        print("❌ Error de Timeout")
        print()
        print("Soluciones:")
        print("1. Verifica tu conexión a internet")
        print("2. Verifica que el puerto 993 no esté bloqueado")
        print("3. Intenta con un puerto diferente (ej: 143)")

    elif 'connection refused' in error_str:
        print("❌ Conexión Rechazada")
        print()
        print("Soluciones:")
        print("1. Verifica que IMAP esté habilitado en Gmail:")
        print("   https://mail.google.com/mail/u/0/#settings/fwdandpop")
        print("2. Habilita 'Acceso IMAP'")

    else:
        print("❌ Error Desconocido")
        print()
        print(f"Detalles: {e}")
        print()
        print("Soluciones generales:")
        print("1. Verifica credenciales en .env")
        print("2. Genera nueva contraseña de aplicación")
        print("3. Habilita IMAP en configuración de Gmail")
        print("4. Actualiza IMAPClient: pip install --upgrade imapclient")

    print()
    import traceback
    print("📋 Stack trace completo:")
    traceback.print_exc()

    sys.exit(1)

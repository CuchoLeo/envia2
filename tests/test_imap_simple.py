#!/usr/bin/env python3
"""
Script de prueba para conexión IMAP usando wrapper simple
Compatible con Python 3.14+
"""
import sys
from dotenv import load_dotenv
import os

print("=" * 60)
print("🧪 Test de Conexión IMAP (Wrapper Simple)")
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
print(f"Python: {sys.version}")
print()

# Test: Usar wrapper simple
print("📦 Test: Importando wrapper simple...")
try:
    from imap_wrapper import SimpleIMAPClient
    print("✅ SimpleIMAPClient importado correctamente")
except ImportError as e:
    print(f"❌ Error importando SimpleIMAPClient: {e}")
    sys.exit(1)

print()

# Test: Conectar
print("🔌 Test: Conectando con SimpleIMAPClient...")
try:
    client = SimpleIMAPClient(
        host=imap_host,
        port=imap_port,
        use_ssl=True
    )

    print("✅ Cliente creado")

    # Conectar y autenticar
    print("🔐 Autenticando...")
    if not client.connect(imap_user, imap_pass):
        print("❌ Error en autenticación")
        sys.exit(1)

    print("✅ Autenticación exitosa")

    # Seleccionar carpeta
    print("📂 Seleccionando INBOX...")
    if not client.select_folder('INBOX'):
        print("❌ Error seleccionando INBOX")
        sys.exit(1)

    print("✅ INBOX seleccionado")

    # Buscar mensajes no leídos
    print("📊 Buscando mensajes...")
    unread = client.search_unseen()
    print(f"✅ Mensajes no leídos: {len(unread)}")

    if len(unread) > 0:
        print(f"\n📧 Probando lectura del primer mensaje...")
        first_msg = client.fetch_message(unread[0])

        if first_msg:
            print(f"✅ Mensaje leído correctamente:")
            print(f"   Asunto: {first_msg['subject'][:50]}...")
            print(f"   De: {first_msg['from'][:50]}...")
            print(f"   Adjuntos: {len(first_msg['attachments'])}")

    # Cerrar conexión
    client.disconnect()
    print("\n✅ Conexión cerrada correctamente")

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

    import traceback
    print("📋 Stack trace:")
    traceback.print_exc()

    print()
    print("=" * 60)
    print("💡 Soluciones:")
    print("=" * 60)
    print()

    error_str = str(e).lower()

    if 'authentication' in error_str or 'login' in error_str:
        print("❌ Error de Autenticación")
        print()
        print("1. Usa CONTRASEÑA DE APLICACIÓN de Gmail")
        print("2. Genera una aquí: https://myaccount.google.com/apppasswords")
        print("3. Verifica que NO tenga espacios en .env")

    elif 'connection' in error_str or 'refused' in error_str:
        print("❌ Error de Conexión")
        print()
        print("1. Habilita IMAP en Gmail:")
        print("   https://mail.google.com/mail/u/0/#settings/fwdandpop")
        print("2. Verifica tu conexión a internet")
        print("3. Verifica que el puerto 993 no esté bloqueado")

    else:
        print("❌ Error Desconocido")
        print()
        print("1. Verifica credenciales en .env")
        print("2. Lee la guía: TROUBLESHOOTING.md")

    sys.exit(1)

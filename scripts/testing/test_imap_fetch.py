#!/usr/bin/env python3
"""
Script para probar el fetch de mensajes IMAP
Útil para diagnosticar problemas con mensajes específicos
"""
import sys
import os

# Agregar raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

from src.imap_wrapper import SimpleIMAPClient
from config import settings
from loguru import logger

def test_imap_fetch():
    """Prueba el fetch de mensajes IMAP"""

    print("\n" + "="*60)
    print("  🧪 TEST DE FETCH IMAP")
    print("="*60 + "\n")

    # Conectar al servidor IMAP
    print(f"📡 Conectando a {settings.imap_host}...")

    client = SimpleIMAPClient(
        host=settings.imap_host,
        port=settings.imap_port,
        use_ssl=settings.imap_use_ssl
    )

    if not client.connect(settings.imap_username, settings.imap_password):
        print("❌ Error conectando al servidor IMAP")
        return False

    print("✅ Conectado exitosamente\n")

    # Seleccionar inbox
    if not client.select_folder(settings.imap_mailbox):
        print("❌ Error seleccionando mailbox")
        return False

    print(f"✅ Mailbox '{settings.imap_mailbox}' seleccionado\n")

    # Buscar mensajes no leídos
    print("🔍 Buscando mensajes no leídos...")
    message_ids = client.search_unseen()

    if not message_ids:
        print("⚠️  No hay mensajes no leídos")
        return True

    print(f"✅ Encontrados {len(message_ids)} mensajes no leídos\n")

    # Probar fetch de cada mensaje
    print("📥 Probando fetch de mensajes...\n")

    exitosos = 0
    errores = 0

    for msg_id in message_ids[:5]:  # Solo los primeros 5 para no saturar
        print(f"   Mensaje {msg_id}...", end=" ")

        mensaje = client.fetch_message(msg_id)

        if mensaje:
            print(f"✅ OK")
            print(f"      Asunto: {mensaje['subject'][:50]}...")
            print(f"      De: {mensaje['from'][:50]}...")
            print(f"      Adjuntos: {len(mensaje['attachments'])}")
            exitosos += 1
        else:
            print(f"❌ ERROR")
            errores += 1

        print()

    # Resumen
    print("\n" + "="*60)
    print("  📊 RESUMEN")
    print("="*60)
    print(f"  Total mensajes no leídos: {len(message_ids)}")
    print(f"  Mensajes probados: {min(len(message_ids), 5)}")
    print(f"  ✅ Exitosos: {exitosos}")
    print(f"  ❌ Errores: {errores}")
    print("="*60 + "\n")

    client.disconnect()

    return errores == 0


if __name__ == "__main__":
    try:
        success = test_imap_fetch()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario\n")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)

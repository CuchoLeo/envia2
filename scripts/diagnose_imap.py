#!/usr/bin/env python3
"""
Script de diagnóstico completo de IMAP
Ayuda a identificar problemas de conexión y detección de correos
"""
import sys
from dotenv import load_dotenv
import os
from imap_wrapper import SimpleIMAPClient

print("=" * 70)
print("🔍 DIAGNÓSTICO COMPLETO DE IMAP")
print("=" * 70)

# Cargar configuración
load_dotenv()

imap_host = os.getenv('IMAP_HOST', 'imap.gmail.com')
imap_port = int(os.getenv('IMAP_PORT', 993))
imap_user = os.getenv('IMAP_USERNAME')
imap_pass = os.getenv('IMAP_PASSWORD')

if not imap_user or not imap_pass:
    print("❌ ERROR: IMAP_USERNAME o IMAP_PASSWORD no configurados en .env")
    sys.exit(1)

print(f"\n📧 Cuenta: {imap_user}")
print(f"🌐 Servidor: {imap_host}:{imap_port}")
print("-" * 70)

# Crear cliente
client = SimpleIMAPClient(host=imap_host, port=imap_port, use_ssl=True)

# Test 1: Conexión
print("\n1️⃣  Test de conexión...")
if not client.connect(imap_user, imap_pass):
    print("❌ No se pudo conectar al servidor IMAP")
    print("\n💡 Verificaciones:")
    print("  1. ¿IMAP está habilitado en Gmail?")
    print("  2. ¿Usas contraseña de aplicación (no tu contraseña normal)?")
    print("  3. ¿La verificación en 2 pasos está habilitada?")
    sys.exit(1)

print("✅ Conexión exitosa")

# Test 2: Listar todas las carpetas
print("\n2️⃣  Listando carpetas disponibles...")
try:
    status, folders = client.client.list()
    if status == 'OK':
        print(f"✅ Encontradas {len(folders)} carpetas:")
        for folder in folders:
            folder_str = folder.decode() if isinstance(folder, bytes) else str(folder)
            print(f"   📁 {folder_str}")
    else:
        print(f"⚠️  No se pudieron listar carpetas: {status}")
except Exception as e:
    print(f"❌ Error listando carpetas: {e}")

# Test 3: Seleccionar INBOX y obtener estadísticas
print("\n3️⃣  Estadísticas de INBOX...")
try:
    if client.select_folder("INBOX"):
        # Obtener número total de mensajes
        status, total = client.client.search(None, 'ALL')
        total_count = len(total[0].split()) if status == 'OK' else 0

        # Obtener mensajes no leídos
        status, unseen = client.client.search(None, 'UNSEEN')
        unseen_count = len(unseen[0].split()) if status == 'OK' else 0

        # Obtener mensajes leídos
        status, seen = client.client.search(None, 'SEEN')
        seen_count = len(seen[0].split()) if status == 'OK' else 0

        print(f"✅ INBOX seleccionado correctamente")
        print(f"   📊 Total de mensajes: {total_count}")
        print(f"   👁️  Mensajes leídos: {seen_count}")
        print(f"   ✉️  Mensajes NO leídos: {unseen_count}")

        if unseen_count == 0:
            print("\n⚠️  NO HAY MENSAJES NO LEÍDOS")
            print("   💡 Posibles causas:")
            print("   1. Todos los correos están marcados como leídos")
            print("   2. Los correos están en otra carpeta (Promociones, Social, etc.)")
            print("   3. No hay correos en la cuenta")

    else:
        print("❌ No se pudo seleccionar INBOX")
except Exception as e:
    print(f"❌ Error obteniendo estadísticas: {e}")
    import traceback
    print(traceback.format_exc())

# Test 4: Listar últimos 5 mensajes (leídos o no)
print("\n4️⃣  Últimos 5 mensajes en INBOX (leídos o no)...")
try:
    status, all_messages = client.client.search(None, 'ALL')

    if status == 'OK' and all_messages[0]:
        message_ids = all_messages[0].split()
        last_5 = message_ids[-5:] if len(message_ids) >= 5 else message_ids

        if last_5:
            print(f"✅ Mostrando últimos {len(last_5)} mensajes:")
            for msg_id in reversed(last_5):  # Mostrar del más reciente al más antiguo
                email_data = client.fetch_message(int(msg_id))
                if email_data:
                    subject = email_data.get('subject', '(sin asunto)')
                    from_addr = email_data.get('from', '(desconocido)')
                    date = email_data.get('date', '(sin fecha)')
                    attachments = len(email_data.get('attachments', []))

                    print(f"\n   📧 ID: {msg_id.decode()}")
                    print(f"      De: {from_addr}")
                    print(f"      Asunto: {subject[:60]}{'...' if len(subject) > 60 else ''}")
                    print(f"      Fecha: {date}")
                    print(f"      Adjuntos: {attachments}")
        else:
            print("⚠️  No hay mensajes en INBOX")
    else:
        print(f"⚠️  No se pudieron buscar mensajes: {status}")

except Exception as e:
    print(f"❌ Error listando mensajes: {e}")
    import traceback
    print(traceback.format_exc())

# Test 5: Buscar específicamente mensajes no leídos usando el método del wrapper
print("\n5️⃣  Test de búsqueda de no leídos (método del sistema)...")
try:
    unseen_messages = client.search_unseen()
    print(f"✅ Resultado: {len(unseen_messages)} mensajes no leídos encontrados")

    if unseen_messages:
        print("   IDs de mensajes no leídos:")
        for uid in unseen_messages[:10]:  # Mostrar máximo 10
            print(f"      - {uid}")
    else:
        print("   ⚠️  El sistema no detectó mensajes no leídos")

except Exception as e:
    print(f"❌ Error en búsqueda de no leídos: {e}")
    import traceback
    print(traceback.format_exc())

# Test 6: Verificar conexión después de todas las operaciones
print("\n6️⃣  Verificando conexión después de operaciones...")
try:
    if client._ensure_connected():
        print("✅ Conexión sigue activa")
    else:
        print("❌ Conexión perdida")
except Exception as e:
    print(f"❌ Error verificando conexión: {e}")

# Cerrar conexión
print("\n7️⃣  Cerrando conexión...")
client.disconnect()
print("✅ Desconectado correctamente")

print("\n" + "=" * 70)
print("📋 RESUMEN DEL DIAGNÓSTICO")
print("=" * 70)
print("\n✅ PRÓXIMOS PASOS:")
print("\n1. Si NO hay mensajes no leídos:")
print("   - Envía un correo de prueba con: python enviar_prueba.py")
print("   - Verifica que llegue a INBOX (no a Promociones/Social)")
print("   - Asegúrate de que esté marcado como NO LEÍDO")
print("\n2. Si hay mensajes pero el sistema no los detecta:")
print("   - Revisa los logs del sistema: tail -f logs/oc_seguimiento_*.log")
print("   - Verifica que el intervalo de chequeo no sea muy largo")
print("\n3. Si ves errores de conexión:")
print("   - Verifica IMAP_HOST, IMAP_PORT en .env")
print("   - Regenera la contraseña de aplicación en Gmail")
print("   - Asegúrate de que IMAP esté habilitado en Gmail")
print("\n" + "=" * 70)

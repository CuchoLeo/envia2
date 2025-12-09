"""
Script para marcar correos como no leídos para reprocesamiento
"""
import sys
import os

# Agregar raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

import imaplib
import email
from email.header import decode_header
from config import settings

def marcar_correos_no_leidos(subject_filter: str = None, sender_filter: str = None):
    """
    Marca correos como no leídos para que sean reprocesados

    Args:
        subject_filter: Filtro por asunto (ej: "servicio reserva")
        sender_filter: Filtro por remitente (ej: "v.rodriguezy@gmail.com")
    """
    print("🔓 Conectando a IMAP...")

    # Conectar a IMAP
    mail = imaplib.IMAP4_SSL(settings.imap_host, settings.imap_port)
    mail.login(settings.imap_username, settings.imap_password)
    mail.select(settings.imap_mailbox)

    print("✅ Conectado exitosamente\n")

    # Buscar correos leídos
    status, messages = mail.search(None, 'SEEN')

    if status != 'OK':
        print("❌ Error al buscar correos")
        return

    email_ids = messages[0].split()
    print(f"📧 Encontrados {len(email_ids)} correos leídos\n")

    marked_count = 0

    for email_id in email_ids[-20:]:  # Procesar últimos 20 correos
        try:
            # Obtener el correo
            status, msg_data = mail.fetch(email_id, '(RFC822)')

            if status != 'OK':
                continue

            # Parse del mensaje
            msg = email.message_from_bytes(msg_data[0][1])

            # Decodificar asunto
            subject = ""
            if msg["Subject"]:
                subject_parts = decode_header(msg["Subject"])
                subject = ""
                for content, encoding in subject_parts:
                    if isinstance(content, bytes):
                        subject += content.decode(encoding or 'utf-8', errors='ignore')
                    else:
                        subject += str(content)

            # Obtener remitente
            from_addr = msg.get("From", "")

            # Aplicar filtros
            should_mark = True

            if subject_filter and subject_filter.lower() not in subject.lower():
                should_mark = False

            if sender_filter and sender_filter.lower() not in from_addr.lower():
                should_mark = False

            if should_mark:
                # Marcar como no leído
                mail.store(email_id, '-FLAGS', '\\Seen')
                print(f"✅ Marcado como no leído:")
                print(f"   Asunto: {subject[:60]}")
                print(f"   De: {from_addr}")
                print()
                marked_count += 1

        except Exception as e:
            print(f"⚠️  Error procesando correo {email_id}: {e}")
            continue

    mail.close()
    mail.logout()

    print(f"\n{'='*60}")
    print(f"✅ Proceso completado: {marked_count} correos marcados como no leídos")
    print(f"{'='*60}")
    print("\n💡 Los correos serán reprocesados en el próximo ciclo del monitor")


if __name__ == "__main__":
    import sys

    print("="*60)
    print("  MARCAR CORREOS COMO NO LEÍDOS PARA REPROCESAMIENTO")
    print("="*60)
    print()

    # Permitir filtros desde línea de comandos
    subject_filter = None
    sender_filter = None

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Uso:")
            print("  python marcar_correos_no_leidos.py                    # Marcar todos")
            print("  python marcar_correos_no_leidos.py --subject 'texto' # Filtrar por asunto")
            print("  python marcar_correos_no_leidos.py --sender 'email'  # Filtrar por remitente")
            print()
            sys.exit(0)

        if "--subject" in sys.argv:
            idx = sys.argv.index("--subject")
            if idx + 1 < len(sys.argv):
                subject_filter = sys.argv[idx + 1]
                print(f"🔍 Filtrando por asunto: '{subject_filter}'")

        if "--sender" in sys.argv:
            idx = sys.argv.index("--sender")
            if idx + 1 < len(sys.argv):
                sender_filter = sys.argv[idx + 1]
                print(f"🔍 Filtrando por remitente: '{sender_filter}'")
    else:
        # Valores por defecto
        sender_filter = "v.rodriguezy@gmail.com"
        print(f"🔍 Filtrando por remitente por defecto: '{sender_filter}'")

    print()
    marcar_correos_no_leidos(subject_filter, sender_filter)

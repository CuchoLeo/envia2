"""
Script temporal para marcar un email como no leído
"""
import sys
import os

# Agregar raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

from src.imap_wrapper import SimpleIMAPClient
from config import settings

def marcar_como_no_leido(subject_contains: str):
    """
    Busca un email por asunto y lo marca como no leído
    """
    client = SimpleIMAPClient(
        host=settings.imap_host,
        port=settings.imap_port,
        use_ssl=settings.imap_use_ssl
    )

    if not client.connect(settings.imap_username, settings.imap_password):
        print("❌ No se pudo conectar al servidor IMAP")
        return False

    if not client.select_folder(settings.imap_mailbox):
        print("❌ No se pudo seleccionar la carpeta")
        return False

    try:
        # Buscar TODOS los emails (leídos y no leídos)
        status, messages = client.client.search(None, 'ALL')

        if status != 'OK':
            print(f"❌ Error en búsqueda: {status}")
            return False

        message_ids = messages[0].split()
        print(f"📧 Encontrados {len(message_ids)} emails totales")

        # Buscar el email que contenga el texto en el asunto
        for mid in reversed(message_ids):  # Empezar por los más recientes
            email_data = client.fetch_message(int(mid))

            if email_data and subject_contains.lower() in email_data['subject'].lower():
                print(f"\n✅ Email encontrado:")
                print(f"   UID: {mid.decode()}")
                print(f"   Asunto: {email_data['subject']}")
                print(f"   De: {email_data['from']}")

                # Marcar como NO LEÍDO (remover flag \Seen)
                client.client.store(mid, '-FLAGS', '\\Seen')
                print(f"✅ Email marcado como NO LEÍDO")
                return True

        print(f"❌ No se encontró email con asunto que contenga: '{subject_contains}'")
        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        client.disconnect()

if __name__ == "__main__":
    # Buscar el email de OC que enviamos
    marcar_como_no_leido("Orden de Compra - Reserva ID 45215412")

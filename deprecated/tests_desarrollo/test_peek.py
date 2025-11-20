"""Test para verificar el formato de BODY.PEEK[]"""
from imap_wrapper import SimpleIMAPClient
from config import settings

client = SimpleIMAPClient(
    host=settings.imap_host,
    port=settings.imap_port,
    use_ssl=settings.imap_use_ssl
)

if client.connect(settings.imap_username, settings.imap_password):
    if client.select_folder(settings.imap_mailbox):
        # Buscar emails no leídos
        unseen_ids = client.search_unseen()
        print(f"📧 Emails no leídos: {len(unseen_ids)}")

        if unseen_ids:
            uid = unseen_ids[0]
            print(f"\n🔍 Probando fetch con UID {uid}...")

            try:
                email_data = client.fetch_message(uid)

                if email_data:
                    print(f"✅ Fetch exitoso!")
                    print(f"   Asunto: {email_data['subject']}")
                    print(f"   De: {email_data['from']}")
                    print(f"   Adjuntos: {len(email_data.get('attachments', []))}")
                else:
                    print("❌ fetch_message devolvió None")

            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()

    client.disconnect()

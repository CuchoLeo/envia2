"""
Script para verificar emails no leídos manualmente
"""
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

        for uid in unseen_ids:
            email_data = client.fetch_message(uid)
            if email_data:
                print(f"\n{'='*60}")
                print(f"UID: {uid}")
                print(f"Asunto: {email_data['subject']}")
                print(f"De: {email_data['from']}")
                print(f"Adjuntos: {len(email_data.get('attachments', []))}")

                # Verificar filtro de OC
                subject = email_data['subject'].lower()
                keywords = ['orden de compra', 'oc', 'purchase order', 'orden compra']
                matches = [kw for kw in keywords if kw in subject]
                if matches:
                    print(f"✅ Coincide con filtro OC: {matches}")
                else:
                    print(f"❌ NO coincide con filtro OC")

                # Verificar filtro de confirmación
                conf_keywords = ['confirmación', 'confirmacion', 'confirmation']
                conf_matches = [kw for kw in conf_keywords if kw in subject]
                if conf_matches:
                    print(f"⚠️ Coincide con filtro CONFIRMACIÓN: {conf_matches}")

    client.disconnect()

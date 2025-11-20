#!/usr/bin/env python3
"""
Script para marcar el correo de OC como no leído
"""
import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))
IMAP_USERNAME = os.getenv("IMAP_USERNAME")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")

print(f"🔍 Conectando a {IMAP_USERNAME}...")

# Conectar
mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
mail.login(IMAP_USERNAME, IMAP_PASSWORD)
mail.select("INBOX")

# Buscar el correo con asunto "Orden de Compra"
status, messages = mail.search(None, 'SUBJECT "Orden de Compra"')

if status == "OK" and messages[0]:
    email_ids = messages[0].split()
    print(f"📧 Encontrados {len(email_ids)} correos con asunto 'Orden de Compra'")

    for email_id in email_ids:
        # Marcar como no leído
        mail.store(email_id, '-FLAGS', '\\Seen')
        print(f"✅ Correo {email_id.decode()} marcado como NO LEÍDO")
else:
    print("❌ No se encontraron correos")

mail.close()
mail.logout()
print("✅ Completado")

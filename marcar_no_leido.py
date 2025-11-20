#!/usr/bin/env python3
"""
Script para marcar el correo de v.rodriguezy@gmail.com como no leído
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

# Buscar el correo de v.rodriguezy@gmail.com
status, messages = mail.search(None, 'FROM "v.rodriguezy@gmail.com"')

if status == "OK" and messages[0]:
    email_ids = messages[0].split()
    print(f"📧 Encontrados {len(email_ids)} correos de v.rodriguezy@gmail.com")

    for email_id in email_ids[-1:]:  # Solo el más reciente
        # Marcar como no leído
        mail.store(email_id, '-FLAGS', '\\Seen')
        print(f"✅ Correo {email_id.decode()} marcado como NO LEÍDO")
else:
    print("❌ No se encontraron correos")

mail.close()
mail.logout()
print("✅ Completado")

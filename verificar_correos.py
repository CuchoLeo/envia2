#!/usr/bin/env python3
"""
Script para verificar correos en seguimientoocx@gmail.com
"""
import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993
IMAP_USERNAME = "seguimientoocx@gmail.com"
IMAP_PASSWORD = "sormbjwiasjazllo"

print(f"🔍 Conectando a {IMAP_USERNAME}...")

# Conectar
mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
mail.login(IMAP_USERNAME, IMAP_PASSWORD)
mail.select("INBOX")

# Buscar TODOS los correos (leídos y no leídos)
status, messages = mail.search(None, 'ALL')

if status == "OK" and messages[0]:
    email_ids = messages[0].split()
    print(f"📧 Total de correos: {len(email_ids)}")

    # Mostrar últimos 10 correos
    print(f"\n📋 Últimos 10 correos:")
    for email_id in email_ids[-10:]:
        status, msg_data = mail.fetch(email_id, '(BODY[HEADER.FIELDS (FROM SUBJECT DATE)] FLAGS)')
        if status == "OK":
            header = msg_data[0][1].decode('utf-8', errors='ignore')
            flags = str(msg_data[1])

            # Extraer subject
            subject_start = header.find('Subject: ')
            if subject_start != -1:
                subject_end = header.find('\r\n', subject_start)
                subject = header[subject_start+9:subject_end]

                # Extraer from
                from_start = header.find('From: ')
                if from_start != -1:
                    from_end = header.find('\r\n', from_start)
                    from_addr = header[from_start+6:from_end]

                    # Verificar si está leído
                    is_seen = '\\Seen' in flags
                    status_icon = "✅" if is_seen else "📬"

                    print(f"  {status_icon} ID: {email_id.decode():5} | {subject[:50]:50} | De: {from_addr[:30]}")

mail.close()
mail.logout()
print("\n✅ Completado")

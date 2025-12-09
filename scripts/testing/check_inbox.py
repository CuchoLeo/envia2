#!/usr/bin/env python3
"""
Script de diagnóstico para revisar correos en seguimientoocx@gmail.com
"""
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración desde .env
IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))
IMAP_USERNAME = os.getenv("IMAP_USERNAME")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")

print(f"🔍 Conectando a {IMAP_USERNAME} en {IMAP_HOST}:{IMAP_PORT}")
print("=" * 80)

try:
    # Conectar a Gmail
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(IMAP_USERNAME, IMAP_PASSWORD)
    mail.select("INBOX")

    # Buscar TODOS los correos no leídos (sin importar el asunto)
    status, messages = mail.search(None, "UNSEEN")

    if status != "OK":
        print("❌ Error al buscar correos")
        exit(1)

    email_ids = messages[0].split()
    print(f"📧 Total de correos NO LEÍDOS: {len(email_ids)}")
    print("=" * 80)

    if not email_ids:
        print("✅ No hay correos sin leer en este momento")
        print("\n💡 Verifica que:")
        print("   1. El correo fue enviado a seguimientoocx@gmail.com")
        print("   2. El correo no fue marcado como leído")
        print("   3. El correo no está en spam")
        exit(0)

    # Revisar cada correo
    for i, email_id in enumerate(email_ids[:20], 1):  # Máximo 20 correos
        status, msg_data = mail.fetch(email_id, "(RFC822)")

        if status != "OK":
            continue

        # Parsear el mensaje
        msg = email.message_from_bytes(msg_data[0][1])

        # Extraer información
        subject_header = msg.get("Subject", "")
        subject = ""
        if subject_header:
            decoded = decode_header(subject_header)
            for content, encoding in decoded:
                if isinstance(content, bytes):
                    subject += content.decode(encoding or "utf-8", errors="ignore")
                else:
                    subject += str(content)

        from_header = msg.get("From", "")
        from_email = email.utils.parseaddr(from_header)[1].lower()

        date = msg.get("Date", "")

        # Verificar si tiene adjuntos PDF
        has_pdf = False
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append(filename)
                        if filename.lower().endswith('.pdf'):
                            has_pdf = True

        # Verificar criterios
        subject_lower = subject.lower()
        has_confirmation_keyword = (
            'confirmación' in subject_lower or
            'confirmacion' in subject_lower or
            'confirmation' in subject_lower
        )

        # Remitentes autorizados
        allowed_senders = ['kontroltravel@ideasfractal.com', 'v.rodriguezy@gmail.com']
        is_authorized = from_email in allowed_senders

        # Mostrar información
        print(f"\n📨 Correo #{i}")
        print(f"   De: {from_email}")
        print(f"   Asunto: {subject}")
        print(f"   Fecha: {date}")
        print(f"   Adjuntos: {len(attachments)} - {', '.join(attachments) if attachments else 'Ninguno'}")
        print(f"   Tiene PDF: {'✅ SÍ' if has_pdf else '❌ NO'}")
        print(f"   Remitente autorizado: {'✅ SÍ' if is_authorized else '❌ NO'}")
        print(f"   Tiene palabra clave confirmación: {'✅ SÍ' if has_confirmation_keyword else '❌ NO'}")

        # Evaluación
        if is_authorized and has_confirmation_keyword and has_pdf:
            print(f"   ✅ ✅ ✅ ESTE CORREO DEBERÍA PROCESARSE")
        else:
            reasons = []
            if not is_authorized:
                reasons.append(f"remitente no autorizado ({from_email})")
            if not has_confirmation_keyword:
                reasons.append("falta palabra 'confirmación' en asunto")
            if not has_pdf:
                reasons.append("no tiene PDF adjunto")
            print(f"   ❌ NO SE PROCESA: {', '.join(reasons)}")

        print("   " + "-" * 76)

    print("\n" + "=" * 80)
    print("📋 REMITENTES AUTORIZADOS CONFIGURADOS:")
    print("   - kontroltravel@ideasfractal.com")
    print("   - v.rodriguezy@gmail.com")
    print("\n💡 Para que un correo se procese debe cumplir TODO:")
    print("   1. Remitente autorizado")
    print("   2. Asunto con 'confirmación', 'confirmacion' o 'confirmation'")
    print("   3. Tener archivo PDF adjunto")

    mail.close()
    mail.logout()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

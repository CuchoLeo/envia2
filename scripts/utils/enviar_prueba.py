#!/usr/bin/env python3
"""
Script de prueba para enviar correos simulados
Simula el envío de un correo con PDF de confirmación de reserva
"""
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

from dotenv import load_dotenv
import os

# Cargar configuración
load_dotenv()

def enviar_correo_con_pdf(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_pass: str,
    desde: str,
    para: str,
    asunto: str,
    cuerpo: str,
    pdf_path: str
):
    """Envía un correo con adjunto PDF"""

    print("=" * 60)
    print("📧 Enviando correo de prueba...")
    print("=" * 60)
    print(f"Desde: {desde}")
    print(f"Para: {para}")
    print(f"Asunto: {asunto}")
    print(f"PDF: {pdf_path}")
    print()

    # Verificar que existe el PDF
    if not Path(pdf_path).exists():
        print(f"❌ Error: No se encuentra el archivo {pdf_path}")
        return False

    try:
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = desde
        msg['To'] = para
        msg['Subject'] = asunto

        # Agregar cuerpo
        msg.attach(MIMEText(cuerpo, 'plain'))

        # Agregar PDF
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
            pdf_attachment = MIMEApplication(pdf_data, _subtype='pdf')
            pdf_attachment.add_header(
                'Content-Disposition',
                'attachment',
                filename=Path(pdf_path).name
            )
            msg.attach(pdf_attachment)

        # Conectar y enviar
        print("🔄 Conectando al servidor SMTP...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()

        print("🔐 Autenticando...")
        server.login(smtp_user, smtp_pass)

        print("📤 Enviando correo...")
        server.send_message(msg)
        server.quit()

        print()
        print("=" * 60)
        print("✅ Correo enviado exitosamente!")
        print("=" * 60)
        print()
        print("🔍 El sistema debería detectar este correo en ~60 segundos")
        print("📊 Verifica el dashboard: http://localhost:8001")
        print()

        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación SMTP")
        print("💡 Verifica tus credenciales en .env")
        print("💡 Asegúrate de usar una contraseña de aplicación de Gmail")
        return False

    except Exception as e:
        print(f"❌ Error enviando correo: {e}")
        return False


def main():
    """Función principal"""

    print()
    print("🧪 HERRAMIENTA DE PRUEBA - Envío de Correo con PDF")
    print()

    # Obtener configuración del .env
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USERNAME')
    smtp_pass = os.getenv('SMTP_PASSWORD')

    # Destinatario (casilla de monitoreo)
    imap_user = os.getenv('IMAP_USERNAME')

    if not smtp_user or not smtp_pass:
        print("❌ Error: No se encontró configuración SMTP en .env")
        print("💡 Edita el archivo .env con tus credenciales")
        sys.exit(1)

    if not imap_user:
        print("❌ Error: No se encontró configuración IMAP en .env")
        sys.exit(1)

    # Archivo PDF (por defecto el de ejemplo en data/)
    pdf_path = Path(__file__).parent.parent / "data" / "resumen del servicio.pdf"
    if len(sys.argv) > 1:
        pdf_path = Path(sys.argv[1])

    # Menú de opciones
    print("Selecciona el tipo de correo a enviar:")
    print()
    print("1. 📋 Confirmación de Reserva (con PDF)")
    print("2. 📄 Orden de Compra (simular respuesta del cliente)")
    print("3. 🛑 Salir")
    print()

    opcion = input("Opción (1-3): ").strip()

    if opcion == "1":
        # Simular confirmación de reserva
        print()
        print("📋 Enviando confirmación de reserva...")

        asunto = "Confirmación de Reserva Hotel - ID 45215412"
        cuerpo = """
Estimado Cliente,

Adjunto encontrará la confirmación de su reserva hotelera.

Detalles:
- ID: 45215412
- LOC Interno: AAFTTAT
- Hotel: Hampton by Hilton Santiago Las Condes
- Check-in: 27/11/2025
- Monto: CLP 528,701.00

Saludos cordiales,
Kontrol Travel
        """.strip()

        success = enviar_correo_con_pdf(
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_pass=smtp_pass,
            desde=smtp_user,
            para=imap_user,
            asunto=asunto,
            cuerpo=cuerpo,
            pdf_path=pdf_path
        )

        if success:
            print("✅ Correo de confirmación enviado")
            print("🔄 El sistema lo procesará automáticamente")

    elif opcion == "2":
        # Simular envío de OC
        print()
        print("📄 Enviando orden de compra...")

        # Solicitar datos de la reserva
        id_reserva = input("ID de Reserva (o Enter para 45215412): ").strip()
        if not id_reserva:
            id_reserva = "45215412"

        loc_interno = input("LOC Interno (o Enter para AAFTTAT): ").strip()
        if not loc_interno:
            loc_interno = "AAFTTAT"

        asunto = f"Orden de Compra - Reserva ID {id_reserva} - LOC {loc_interno}"
        cuerpo = f"""
Estimados,

Adjunto la Orden de Compra correspondiente a:

- Reserva ID: {id_reserva}
- LOC Interno: {loc_interno}
- Número OC: OC-{id_reserva}

Saludos,
Cliente Corporativo
        """.strip()

        # Para OC, enviamos a la casilla de recepción de OC
        oc_inbox = os.getenv('OC_INBOX_USERNAME', imap_user)

        success = enviar_correo_con_pdf(
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_pass=smtp_pass,
            desde=smtp_user,
            para=oc_inbox,
            asunto=asunto,
            cuerpo=cuerpo,
            pdf_path=pdf_path
        )

        if success:
            print("✅ Orden de Compra enviada")
            print("🔄 El sistema debería detectarla y asociarla con la reserva")

    elif opcion == "3":
        print("👋 Saliendo...")
        sys.exit(0)

    else:
        print("❌ Opción inválida")
        sys.exit(1)


if __name__ == "__main__":
    main()

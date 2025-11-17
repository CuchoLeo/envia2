#!/usr/bin/env python3
"""
🧪 Script de Prueba del Flujo Completo
Automatiza todo el ciclo: Confirmación → Solicitud OC → Respuesta OC → Cierre
"""
import smtplib
import sys
import time
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

# Cargar configuración
load_dotenv()

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_step(step_num, total, message):
    """Imprime paso del proceso"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}[{step_num}/{total}] {message}{Colors.RESET}")
    print("=" * 70)

def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

def print_error(message):
    """Imprime mensaje de error"""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")

def print_info(message):
    """Imprime mensaje informativo"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")

def print_waiting(message):
    """Imprime mensaje de espera"""
    print(f"{Colors.YELLOW}⏳ {message}{Colors.RESET}")

def enviar_correo_con_pdf(smtp_host, smtp_port, smtp_user, smtp_pass, desde, para, asunto, cuerpo, pdf_path):
    """Envía un correo con adjunto PDF"""
    try:
        # Verificar que existe el PDF
        if not Path(pdf_path).exists():
            print_error(f"No se encuentra el archivo {pdf_path}")
            return False

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
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print_error(f"Error enviando correo: {e}")
        return False

def verificar_api():
    """Verifica que la API esté disponible"""
    try:
        response = requests.get('http://localhost:8001/api/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def obtener_stats():
    """Obtiene estadísticas del sistema"""
    try:
        response = requests.get('http://localhost:8001/api/stats', timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def obtener_reservas():
    """Obtiene lista de reservas"""
    try:
        response = requests.get('http://localhost:8001/api/reservas', timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def esperar_con_progress(segundos, mensaje):
    """Espera mostrando progreso"""
    print(f"\n{mensaje}")
    for i in range(segundos, 0, -1):
        print(f"   {i} segundos... ", end='\r')
        time.sleep(1)
    print("   ✓ Listo!          ")

def main():
    """Función principal de prueba"""

    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}{Colors.CYAN}🧪 PRUEBA COMPLETA DEL FLUJO DE SEGUIMIENTO DE OC{Colors.RESET}")
    print("=" * 70)
    print(f"{Colors.YELLOW}Este script automatiza todo el ciclo de vida de una reserva:{Colors.RESET}")
    print("  1. Envío de confirmación de reserva")
    print("  2. Detección y procesamiento automático")
    print("  3. Envío de solicitud de OC")
    print("  4. Envío de OC por parte del cliente")
    print("  5. Detección y cierre del ciclo")
    print("=" * 70)

    # Obtener configuración
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USERNAME')
    smtp_pass = os.getenv('SMTP_PASSWORD')
    imap_user = os.getenv('IMAP_USERNAME')
    oc_inbox = os.getenv('OC_INBOX_USERNAME', imap_user)

    if not all([smtp_user, smtp_pass, imap_user]):
        print_error("Falta configuración en .env")
        sys.exit(1)

    # Buscar PDF en la carpeta data/
    pdf_path = Path(__file__).parent.parent / "data" / "resumen del servicio.pdf"
    if not pdf_path.exists():
        print_error(f"No se encuentra el archivo {pdf_path}")
        print_info("Asegúrate de que existe: data/resumen del servicio.pdf")
        sys.exit(1)

    # Verificar que la API está corriendo
    print_step(0, 7, "Verificando que el sistema está corriendo")
    if not verificar_api():
        print_error("El sistema no está corriendo en http://localhost:8001")
        print_info("Ejecuta: python app.py")
        sys.exit(1)
    print_success("Sistema está corriendo y respondiendo")

    # Obtener estado inicial
    stats_inicial = obtener_stats()
    if stats_inicial:
        print_info(f"Estado inicial:")
        print(f"  - Total reservas: {stats_inicial.get('total_reservas', 0)}")
        print(f"  - Pendientes OC: {stats_inicial.get('pendientes_oc', 0)}")

    # Paso 1: Enviar confirmación de reserva
    print_step(1, 7, "Enviando confirmación de reserva (simula hotel)")

    id_reserva = f"TEST{int(time.time())}"  # ID único para esta prueba
    loc_interno = "TESTLOC"

    asunto_confirmacion = f"Confirmación de Reserva Hotel - ID {id_reserva}"
    cuerpo_confirmacion = f"""
Estimado Cliente,

Adjunto encontrará la confirmación de su reserva hotelera.

Detalles:
- ID: {id_reserva}
- LOC Interno: {loc_interno}
- Hotel: Hampton by Hilton Santiago Las Condes
- Check-in: 27/11/2025
- Monto: CLP 528,701.00

Saludos cordiales,
Kontrol Travel
    """.strip()

    print_info(f"De: {smtp_user}")
    print_info(f"Para: {imap_user}")
    print_info(f"Asunto: {asunto_confirmacion}")

    if not enviar_correo_con_pdf(smtp_host, smtp_port, smtp_user, smtp_pass,
                                  smtp_user, imap_user, asunto_confirmacion,
                                  cuerpo_confirmacion, pdf_path):
        print_error("Fallo al enviar confirmación")
        sys.exit(1)

    print_success("Confirmación enviada")

    # Paso 2: Esperar detección del sistema
    print_step(2, 7, "Esperando que el sistema detecte y procese el correo")

    # El intervalo de chequeo está en .env (IMAP_CHECK_INTERVAL)
    intervalo = int(os.getenv('IMAP_CHECK_INTERVAL', '300'))
    tiempo_espera = min(intervalo + 10, 70)  # Esperar intervalo + margen, max 70 seg

    esperar_con_progress(tiempo_espera, f"⏳ Esperando {tiempo_espera} segundos para que el monitor IMAP detecte el correo...")

    # Verificar que se creó la reserva
    print_info("Verificando que se creó la reserva en la base de datos...")
    reservas_data = obtener_reservas()

    reserva_encontrada = False
    if reservas_data and 'reservas' in reservas_data:
        for reserva in reservas_data['reservas']:
            if loc_interno in str(reserva.get('loc_interno', '')):
                reserva_encontrada = True
                print_success(f"Reserva creada: ID {reserva.get('id')}, Estado OC: {reserva.get('estado_oc')}")
                break

    if not reserva_encontrada:
        print_error("No se encontró la reserva creada")
        print_info("Revisa los logs: tail -f logs/oc_seguimiento_*.log")
        print_info("El sistema podría necesitar más tiempo, verifica el dashboard")
    else:
        print_success("Reserva detectada y procesada correctamente")

    # Paso 3: Verificar envío de solicitud de OC
    print_step(3, 7, "Verificando que se envió solicitud de OC automáticamente")

    # En un sistema real, aquí verificaríamos la bandeja del cliente
    # Por ahora verificamos el contador de correos enviados
    stats_actual = obtener_stats()
    if stats_actual:
        correos_enviados = stats_actual.get('correos_enviados', 0)
        if correos_enviados > 0:
            print_success(f"Sistema ha enviado {correos_enviados} correos")
        else:
            print_info("No se detectaron correos enviados aún (puede tomar unos minutos)")

    # Paso 4: Solicitar confirmación del usuario
    print_step(4, 7, "Revisión manual")
    print_info("Abre el dashboard: http://localhost:8001")
    print_info("Verifica que:")
    print("  1. La reserva aparece en la lista")
    print("  2. El estado es 'PENDIENTE' o 'SOLICITADA'")
    print("  3. Se envió el correo de solicitud de OC")

    input(f"\n{Colors.YELLOW}Presiona Enter cuando hayas verificado el dashboard...{Colors.RESET}")

    # Paso 5: Enviar OC de respuesta
    print_step(5, 7, "Enviando Orden de Compra (simula respuesta del cliente)")

    asunto_oc = f"Orden de Compra - Reserva ID {id_reserva} - LOC {loc_interno}"
    cuerpo_oc = f"""
Estimados,

Adjunto la Orden de Compra correspondiente a:

- Reserva ID: {id_reserva}
- LOC Interno: {loc_interno}
- Número OC: OC-{id_reserva}

Saludos,
WALVIS S.A.
    """.strip()

    print_info(f"De: {smtp_user}")
    print_info(f"Para: {oc_inbox}")
    print_info(f"Asunto: {asunto_oc}")

    if not enviar_correo_con_pdf(smtp_host, smtp_port, smtp_user, smtp_pass,
                                  smtp_user, oc_inbox, asunto_oc,
                                  cuerpo_oc, pdf_path):
        print_error("Fallo al enviar OC")
        sys.exit(1)

    print_success("OC enviada")

    # Paso 6: Esperar detección de la OC
    print_step(6, 7, "Esperando que el sistema detecte la OC")

    intervalo_oc = int(os.getenv('OC_CHECK_INTERVAL', '300'))
    tiempo_espera_oc = min(intervalo_oc + 10, 70)

    esperar_con_progress(tiempo_espera_oc, f"⏳ Esperando {tiempo_espera_oc} segundos para que el monitor de OC detecte el correo...")

    # Verificar que se actualizó la reserva
    print_info("Verificando que se actualizó el estado de la reserva...")
    reservas_data = obtener_reservas()

    oc_detectada = False
    if reservas_data and 'reservas' in reservas_data:
        for reserva in reservas_data['reservas']:
            if loc_interno in str(reserva.get('loc_interno', '')):
                estado = reserva.get('estado_oc', '')
                print_info(f"Estado actual: {estado}")
                if estado == 'RECIBIDA':
                    oc_detectada = True
                    print_success("OC detectada y procesada - Ciclo completado!")
                break

    if not oc_detectada:
        print_info("La OC podría necesitar más tiempo para ser detectada")
        print_info("Verifica el dashboard en unos minutos")

    # Paso 7: Resumen final
    print_step(7, 7, "Resumen del test")

    stats_final = obtener_stats()
    if stats_final:
        print(f"\n{Colors.BOLD}Estadísticas Finales:{Colors.RESET}")
        print(f"  Total reservas: {stats_final.get('total_reservas', 0)}")
        print(f"  Pendientes OC: {stats_final.get('pendientes_oc', 0)}")
        print(f"  OC Recibidas: {stats_final.get('oc_recibidas', 0)}")
        print(f"  Correos enviados: {stats_final.get('correos_enviados', 0)}")

    print(f"\n{Colors.BOLD}{Colors.GREEN}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}✅ PRUEBA COMPLETADA{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'=' * 70}{Colors.RESET}")

    print(f"\n{Colors.CYAN}📊 Próximos pasos:{Colors.RESET}")
    print("  1. Revisa el dashboard: http://localhost:8001")
    print("  2. Revisa los logs: tail -f logs/oc_seguimiento_*.log")
    print("  3. Verifica tu bandeja de correo para ver la solicitud de OC enviada")
    print(f"\n{Colors.YELLOW}💡 Datos de la prueba:{Colors.RESET}")
    print(f"  ID Reserva: {id_reserva}")
    print(f"  LOC Interno: {loc_interno}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Prueba interrumpida por el usuario{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error inesperado: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

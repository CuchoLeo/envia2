#!/usr/bin/env python3
"""
Script para enviar manualmente correos de solicitud de OC
Permite probar todos los tipos de correos que el sistema envía automáticamente
"""
import sys
import os
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.email_sender import email_sender
from database import get_db, Reserva, init_db
from datetime import datetime

# Cargar configuración
load_dotenv()

# Inicializar base de datos
init_db()

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Imprime el encabezado del script"""
    print("\n" + "="*70)
    print(f"{Colors.BOLD}{Colors.CYAN}📧 ENVÍO MANUAL DE SOLICITUDES DE OC{Colors.RESET}")
    print("="*70)
    print(f"{Colors.YELLOW}Este script permite enviar manualmente los correos de solicitud de OC")
    print("para probar los diferentes templates y estados.{Colors.RESET}\n")

def listar_reservas():
    """Lista las reservas disponibles"""
    db = next(get_db())
    try:
        reservas = db.query(Reserva).filter_by(requiere_oc=True).all()

        if not reservas:
            print(f"{Colors.RED}❌ No hay reservas que requieran OC en la base de datos{Colors.RESET}")
            return None

        print(f"{Colors.BOLD}📋 RESERVAS DISPONIBLES:{Colors.RESET}\n")
        print(f"{'ID':<5} {'ID Reserva':<12} {'LOC':<10} {'Agencia':<25} {'Estado OC':<12}")
        print("-" * 70)

        for reserva in reservas:
            print(f"{reserva.id:<5} {reserva.id_reserva:<12} {reserva.loc_interno:<10} "
                  f"{reserva.agencia:<25} {reserva.estado_oc:<12}")

        print()
        return reservas
    finally:
        db.close()

def obtener_reserva(reserva_id: int):
    """Obtiene una reserva por ID"""
    db = next(get_db())
    try:
        reserva = db.query(Reserva).filter_by(id=reserva_id).first()
        return reserva
    finally:
        db.close()

def mostrar_menu_tipos():
    """Muestra el menú de tipos de correo"""
    print(f"{Colors.BOLD}📨 TIPOS DE CORREO DISPONIBLES:{Colors.RESET}\n")
    print("1. 📧 Solicitud Inicial - Primera solicitud de OC al cliente")
    print("2. 🔔 Recordatorio 1 - Primer recordatorio (generalmente día 3)")
    print("3. ⚠️  Recordatorio 2 - Segundo recordatorio (generalmente día 5)")
    print("4. 🚨 Ultimátum - Correo de urgencia final")
    print("5. ❌ Cancelar")
    print()

def enviar_correo(reserva, tipo_correo: str):
    """Envía el correo de solicitud de OC"""
    print(f"\n{Colors.CYAN}📤 Enviando correo...{Colors.RESET}")
    print(f"  Tipo: {tipo_correo}")
    print(f"  Reserva: {reserva.id_reserva}")
    print(f"  Agencia: {reserva.agencia}")
    print()

    try:
        # Obtener email del cliente
        from database import ConfiguracionCliente
        db = next(get_db())
        try:
            cliente = db.query(ConfiguracionCliente).filter_by(
                nombre_agencia=reserva.agencia
            ).first()

            if not cliente:
                print(f"{Colors.RED}❌ No se encontró configuración para la agencia {reserva.agencia}{Colors.RESET}")
                print(f"{Colors.YELLOW}💡 Usando email de prueba: contacto@agencia.com{Colors.RESET}")
                email_destino = "contacto@agencia.com"
            else:
                email_destino = cliente.email_contacto
        finally:
            db.close()

        print(f"  Destinatario: {email_destino}")
        print()

        # Enviar correo usando el email_sender
        result = email_sender.enviar_solicitud_oc(
            reserva=reserva,
            tipo_correo=tipo_correo,
            destinatario=email_destino
        )

        if result:
            print(f"{Colors.GREEN}✅ Correo enviado exitosamente!{Colors.RESET}\n")
            print(f"{Colors.BLUE}📊 Detalles:{Colors.RESET}")
            print(f"  - Para: {email_destino}")
            print(f"  - Tipo: {tipo_correo}")
            print(f"  - Reserva ID: {reserva.id_reserva}")
            print(f"  - LOC: {reserva.loc_interno}")
            print(f"  - Monto: {reserva.moneda} {reserva.monto_total:,.0f}")
            return True
        else:
            print(f"{Colors.RED}❌ Error al enviar el correo{Colors.RESET}")
            return False

    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print_header()

    # Listar reservas disponibles
    reservas = listar_reservas()
    if not reservas:
        sys.exit(1)

    # Seleccionar reserva
    try:
        reserva_id = input(f"{Colors.BOLD}Ingresa el ID de la reserva (o Enter para cancelar): {Colors.RESET}").strip()

        if not reserva_id:
            print(f"\n{Colors.YELLOW}❌ Cancelado por el usuario{Colors.RESET}\n")
            sys.exit(0)

        reserva_id = int(reserva_id)
        reserva = obtener_reserva(reserva_id)

        if not reserva:
            print(f"\n{Colors.RED}❌ Reserva no encontrada con ID: {reserva_id}{Colors.RESET}\n")
            sys.exit(1)

        if not reserva.requiere_oc:
            print(f"\n{Colors.RED}❌ Esta reserva no requiere OC{Colors.RESET}\n")
            sys.exit(1)

        print(f"\n{Colors.GREEN}✅ Reserva seleccionada:{Colors.RESET}")
        print(f"  ID: {reserva.id_reserva}")
        print(f"  LOC: {reserva.loc_interno}")
        print(f"  Agencia: {reserva.agencia}")
        print(f"  Hotel: {reserva.nombre_hotel}")
        print(f"  Check-in: {reserva.fecha_checkin}")
        print(f"  Monto: {reserva.moneda} {reserva.monto_total:,.0f}")
        print(f"  Estado OC: {reserva.estado_oc}")
        print()

    except ValueError:
        print(f"\n{Colors.RED}❌ ID inválido{Colors.RESET}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}❌ Cancelado por el usuario{Colors.RESET}\n")
        sys.exit(0)

    # Mostrar menú de tipos de correo
    mostrar_menu_tipos()

    # Seleccionar tipo de correo
    try:
        opcion = input(f"{Colors.BOLD}Selecciona el tipo de correo (1-5): {Colors.RESET}").strip()

        tipos_correo = {
            "1": "solicitud_inicial",
            "2": "recordatorio_1",
            "3": "recordatorio_2",
            "4": "ultimatum"
        }

        if opcion == "5" or opcion == "":
            print(f"\n{Colors.YELLOW}❌ Cancelado por el usuario{Colors.RESET}\n")
            sys.exit(0)

        if opcion not in tipos_correo:
            print(f"\n{Colors.RED}❌ Opción inválida{Colors.RESET}\n")
            sys.exit(1)

        tipo_correo = tipos_correo[opcion]

        # Confirmar envío
        print(f"\n{Colors.YELLOW}⚠️  ¿Confirmas el envío del correo?{Colors.RESET}")
        print(f"  Tipo: {tipo_correo}")
        print(f"  Reserva: {reserva.id_reserva} - {reserva.agencia}")
        confirmar = input(f"\n{Colors.BOLD}Enviar correo? (s/N): {Colors.RESET}").strip().lower()

        if confirmar != 's' and confirmar != 'si' and confirmar != 'sí':
            print(f"\n{Colors.YELLOW}❌ Envío cancelado{Colors.RESET}\n")
            sys.exit(0)

        # Enviar correo
        success = enviar_correo(reserva, tipo_correo)

        if success:
            print(f"\n{Colors.GREEN}{'='*70}{Colors.RESET}")
            print(f"{Colors.GREEN}{Colors.BOLD}✅ CORREO ENVIADO EXITOSAMENTE{Colors.RESET}")
            print(f"{Colors.GREEN}{'='*70}{Colors.RESET}\n")

            print(f"{Colors.BLUE}💡 Próximos pasos:{Colors.RESET}")
            print(f"  1. Revisa tu bandeja de entrada")
            print(f"  2. Verifica que el correo se vea correctamente")
            print(f"  3. Responde con un email de OC para completar el ciclo")
            print()
        else:
            print(f"\n{Colors.RED}{'='*70}{Colors.RESET}")
            print(f"{Colors.RED}{Colors.BOLD}❌ ERROR AL ENVIAR CORREO{Colors.RESET}")
            print(f"{Colors.RED}{'='*70}{Colors.RESET}\n")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}❌ Cancelado por el usuario{Colors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error inesperado: {e}{Colors.RESET}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

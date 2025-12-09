#!/usr/bin/env python3
"""
Script para actualizar emails de contacto de clientes
Permite actualizar el campo email_contacto en configuracion_clientes
"""
import sys
import os

# Agregar raíz del proyecto al path Y cambiar directorio de trabajo
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

from database import init_db, get_db, ConfiguracionCliente
from loguru import logger


def listar_clientes_sin_email(db):
    """Lista clientes que no tienen email configurado"""
    clientes = db.query(ConfiguracionCliente).filter(
        (ConfiguracionCliente.email_contacto == None) |
        (ConfiguracionCliente.email_contacto == '')
    ).all()

    return clientes


def actualizar_email(db, nombre_agencia: str, email: str) -> bool:
    """
    Actualiza el email de contacto de un cliente

    Args:
        db: Sesión de base de datos
        nombre_agencia: Nombre de la agencia a actualizar
        email: Nuevo email de contacto

    Returns:
        True si se actualizó exitosamente
    """
    try:
        cliente = db.query(ConfiguracionCliente).filter_by(
            nombre_agencia=nombre_agencia
        ).first()

        if not cliente:
            print(f"❌ No se encontró cliente: {nombre_agencia}")
            return False

        cliente.email_contacto = email
        db.commit()

        print(f"✅ Actualizado: {nombre_agencia} -> {email}")
        return True

    except Exception as e:
        logger.error(f"Error actualizando {nombre_agencia}: {e}")
        db.rollback()
        return False


def menu_interactivo():
    """Menú interactivo para actualizar emails"""

    print("\n" + "="*70)
    print("  📧 ACTUALIZACIÓN DE EMAILS DE CONTACTO")
    print("="*70 + "\n")

    init_db()
    db = next(get_db())

    while True:
        print("\nOpciones:")
        print("  1. Ver clientes sin email")
        print("  2. Ver todos los clientes con sus emails")
        print("  3. Actualizar email de un cliente")
        print("  4. Actualizar emails en lote (desde archivo)")
        print("  0. Salir")

        opcion = input("\n  Selecciona una opción: ").strip()

        if opcion == "0":
            print("\n✅ Saliendo...\n")
            break

        elif opcion == "1":
            clientes = listar_clientes_sin_email(db)

            print(f"\n📋 Clientes SIN email configurado: {len(clientes)}\n")
            print("-" * 70)

            for cliente in clientes:
                requiere = "SÍ requiere OC" if cliente.requiere_oc else "NO requiere OC"
                print(f"  • {cliente.nombre_agencia:<50} | {requiere}")

            print("-" * 70)

        elif opcion == "2":
            clientes = db.query(ConfiguracionCliente).order_by(
                ConfiguracionCliente.nombre_agencia
            ).all()

            print(f"\n📋 Todos los clientes ({len(clientes)}):\n")
            print("-" * 90)
            print(f"{'AGENCIA':<50} | {'EMAIL':<30} | OC")
            print("-" * 90)

            for cliente in clientes:
                email = cliente.email_contacto or "(sin email)"
                requiere = "SÍ" if cliente.requiere_oc else "NO"
                print(f"{cliente.nombre_agencia:<50} | {email:<30} | {requiere}")

            print("-" * 90)

        elif opcion == "3":
            print("\n📝 Actualizar email de cliente\n")

            nombre = input("  Nombre de la agencia: ").strip()

            if not nombre:
                print("  ❌ Nombre vacío, cancelando...")
                continue

            # Buscar cliente
            cliente = db.query(ConfiguracionCliente).filter_by(
                nombre_agencia=nombre
            ).first()

            if not cliente:
                print(f"\n  ❌ No se encontró cliente: {nombre}")
                print("\n  💡 Tip: El nombre debe coincidir exactamente (mayúsculas, espacios, etc.)")
                continue

            print(f"\n  Cliente encontrado:")
            print(f"    Agencia: {cliente.nombre_agencia}")
            print(f"    Email actual: {cliente.email_contacto or '(vacío)'}")
            print(f"    Requiere OC: {'SÍ' if cliente.requiere_oc else 'NO'}")

            email = input("\n  Nuevo email de contacto: ").strip()

            if not email:
                print("  ❌ Email vacío, cancelando...")
                continue

            # Validación básica de email
            if '@' not in email or '.' not in email.split('@')[1]:
                print("  ⚠️  El email no parece válido, pero se guardará de todas formas")

            confirmacion = input(f"\n  ¿Confirmar actualización? (S/n): ").strip().lower()

            if confirmacion in ['s', 'si', 'sí', 'yes', 'y', '']:
                if actualizar_email(db, nombre, email):
                    print(f"\n  ✅ Email actualizado correctamente\n")
                else:
                    print(f"\n  ❌ Error al actualizar\n")
            else:
                print("\n  ❌ Cancelado\n")

        elif opcion == "4":
            print("\n📁 Actualización en lote desde archivo\n")
            print("  Formato del archivo (CSV):")
            print("  NOMBRE_AGENCIA,email@example.com")
            print("  OTRA_AGENCIA,contacto@otra.com")
            print()

            archivo = input("  Ruta del archivo CSV: ").strip()

            if not archivo or not os.path.exists(archivo):
                print("  ❌ Archivo no encontrado\n")
                continue

            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    lineas = f.readlines()

                print(f"\n  📄 Archivo leído: {len(lineas)} líneas\n")

                exitosos = 0
                errores = 0

                for linea in lineas:
                    linea = linea.strip()
                    if not linea or linea.startswith('#'):
                        continue

                    partes = linea.split(',')
                    if len(partes) != 2:
                        print(f"  ⚠️  Línea inválida: {linea}")
                        continue

                    nombre, email = partes[0].strip(), partes[1].strip()

                    if actualizar_email(db, nombre, email):
                        exitosos += 1
                    else:
                        errores += 1

                print(f"\n  📊 Resumen:")
                print(f"    ✅ Actualizados: {exitosos}")
                print(f"    ❌ Errores: {errores}")
                print()

            except Exception as e:
                print(f"  ❌ Error leyendo archivo: {e}\n")

        else:
            print("\n  ❌ Opción no válida\n")


def actualizar_desde_dict(emails_dict: dict):
    """
    Actualiza emails desde un diccionario

    Args:
        emails_dict: Diccionario {nombre_agencia: email}
    """
    print("\n" + "="*70)
    print("  📧 ACTUALIZACIÓN MASIVA DE EMAILS")
    print("="*70 + "\n")

    init_db()
    db = next(get_db())

    exitosos = 0
    errores = 0
    no_encontrados = 0

    for nombre, email in emails_dict.items():
        try:
            cliente = db.query(ConfiguracionCliente).filter_by(
                nombre_agencia=nombre
            ).first()

            if not cliente:
                print(f"⚠️  No encontrado: {nombre}")
                no_encontrados += 1
                continue

            cliente.email_contacto = email
            exitosos += 1
            print(f"✅ {nombre:<50} -> {email}")

        except Exception as e:
            print(f"❌ Error en {nombre}: {e}")
            errores += 1

    try:
        db.commit()
        print("\n" + "="*70)
        print("  ✅ CAMBIOS GUARDADOS")
        print("="*70)
        print(f"\n  📊 Resumen:")
        print(f"    ✅ Actualizados: {exitosos}")
        print(f"    ⚠️  No encontrados: {no_encontrados}")
        print(f"    ❌ Errores: {errores}")
        print()
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error guardando cambios: {e}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Actualizar emails de contacto de clientes')
    parser.add_argument('--sin-email', action='store_true', help='Listar clientes sin email')
    parser.add_argument('--todos', action='store_true', help='Listar todos los clientes con emails')
    parser.add_argument('--cliente', type=str, help='Nombre de cliente a actualizar')
    parser.add_argument('--email', type=str, help='Nuevo email')
    parser.add_argument('--archivo', type=str, help='Archivo CSV con actualizaciones')

    args = parser.parse_args()

    init_db()
    db = next(get_db())

    if args.sin_email:
        clientes = listar_clientes_sin_email(db)
        print(f"\n📋 Clientes SIN email: {len(clientes)}\n")
        for cliente in clientes:
            print(f"  • {cliente.nombre_agencia}")
        print()

    elif args.todos:
        clientes = db.query(ConfiguracionCliente).order_by(
            ConfiguracionCliente.nombre_agencia
        ).all()
        print(f"\n📋 Todos los clientes:\n")
        for cliente in clientes:
            email = cliente.email_contacto or "(sin email)"
            print(f"  {cliente.nombre_agencia:<50} | {email}")
        print()

    elif args.cliente and args.email:
        actualizar_email(db, args.cliente, args.email)

    elif args.archivo:
        if not os.path.exists(args.archivo):
            print(f"❌ Archivo no encontrado: {args.archivo}")
        else:
            try:
                with open(args.archivo, 'r', encoding='utf-8') as f:
                    lineas = f.readlines()

                exitosos = 0
                errores = 0

                for linea in lineas:
                    linea = linea.strip()
                    if not linea or linea.startswith('#'):
                        continue

                    partes = linea.split(',')
                    if len(partes) == 2:
                        nombre, email = partes[0].strip(), partes[1].strip()
                        if actualizar_email(db, nombre, email):
                            exitosos += 1
                        else:
                            errores += 1

                print(f"\n✅ Actualizados: {exitosos}")
                print(f"❌ Errores: {errores}\n")

            except Exception as e:
                print(f"❌ Error: {e}")
    else:
        # Modo interactivo
        menu_interactivo()

"""
Script para limpiar registros de la base de datos
Permite eliminar reservas, correos enviados y órdenes de compra
"""
import sys
import os

# Agregar raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

from database import init_db, get_db, Reserva, CorreoEnviado, OrdenCompra, ConfiguracionCliente, EstadoOC
from sqlalchemy import func

def mostrar_estadisticas(db):
    """Muestra estadísticas actuales de la base de datos"""
    total_reservas = db.query(Reserva).count()
    total_correos = db.query(CorreoEnviado).count()
    total_oc = db.query(OrdenCompra).count()
    total_clientes = db.query(ConfiguracionCliente).count()

    print("\n" + "="*60)
    print("  📊 ESTADÍSTICAS ACTUALES DE LA BASE DE DATOS")
    print("="*60)
    print(f"  📋 Reservas:              {total_reservas}")
    print(f"  📧 Correos enviados:       {total_correos}")
    print(f"  ✅ Órdenes de compra:      {total_oc}")
    print(f"  👥 Clientes configurados:  {total_clientes}")
    print("="*60 + "\n")

    return total_reservas, total_correos, total_oc, total_clientes


def listar_reservas(db):
    """Lista todas las reservas"""
    reservas = db.query(Reserva).order_by(Reserva.fecha_creacion.desc()).all()

    if not reservas:
        print("❌ No hay reservas en la base de datos\n")
        return []

    print("\n" + "="*80)
    print("  📋 LISTADO DE RESERVAS")
    print("="*80)

    for i, r in enumerate(reservas, 1):
        print(f"\n  {i}. ID: {r.id_reserva}")
        print(f"     Agencia: {r.agencia}")
        print(f"     Monto: {r.moneda} {r.monto_total:,.0f}")
        print(f"     Estado OC: {r.estado_oc.value}")
        print(f"     Requiere OC: {'Sí' if r.requiere_oc else 'No'}")
        print(f"     Fecha creación: {r.fecha_creacion}")
        print(f"     Correos enviados: {len(r.correos_enviados)}")
        print(f"     OC recibida: {'Sí' if r.orden_compra else 'No'}")

    print("\n" + "="*80 + "\n")
    return reservas


def eliminar_ordenes_compra(db):
    """Elimina TODAS las órdenes de compra"""
    total_oc = db.query(OrdenCompra).count()

    if total_oc == 0:
        print("\n❌ No hay órdenes de compra en la base de datos\n")
        return False

    print(f"\n⚠️  ¡ADVERTENCIA! Esta acción eliminará {total_oc} órdenes de compra\n")
    print("   Las reservas NO se eliminarán, solo las OC recibidas")
    print()

    confirmacion = input("   ¿Estás seguro? Escribe 'SI' para confirmar: ")

    if confirmacion.upper() != 'SI':
        print("\n❌ Operación cancelada\n")
        return False

    try:
        count_oc = db.query(OrdenCompra).count()

        # Eliminar todas las órdenes de compra
        db.query(OrdenCompra).delete()

        # Actualizar estado de reservas que tenían OC
        reservas_con_oc = db.query(Reserva).filter(Reserva.estado_oc == EstadoOC.RECIBIDA).all()
        for reserva in reservas_con_oc:
            reserva.estado_oc = EstadoOC.PENDIENTE

        db.commit()

        print("\n" + "="*60)
        print("  ✅ ÓRDENES DE COMPRA ELIMINADAS")
        print("="*60)
        print(f"  ✅ OC eliminadas: {count_oc}")
        print(f"  🔄 Reservas actualizadas a PENDIENTE: {len(reservas_con_oc)}")
        print("="*60 + "\n")

        return True

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error al eliminar órdenes de compra: {e}\n")
        return False


def eliminar_todas_reservas(db):
    """Elimina TODAS las reservas y datos relacionados"""
    print("\n⚠️  ¡ADVERTENCIA! Esta acción eliminará TODAS las reservas\n")
    print("   Esto incluye:")
    print("   • Todas las reservas")
    print("   • Todos los correos enviados asociados")
    print("   • Todas las órdenes de compra recibidas")
    print()

    confirmacion = input("   ¿Estás seguro? Escribe 'SI' para confirmar: ")

    if confirmacion.upper() != 'SI':
        print("\n❌ Operación cancelada\n")
        return False

    try:
        # Contar antes de eliminar
        count_reservas = db.query(Reserva).count()
        count_correos = db.query(CorreoEnviado).count()
        count_oc = db.query(OrdenCompra).count()

        # Eliminar en orden (las relaciones cascade se encargan del resto)
        db.query(Reserva).delete()
        db.commit()

        print("\n" + "="*60)
        print("  ✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
        print("="*60)
        print(f"  📋 Reservas eliminadas:        {count_reservas}")
        print(f"  📧 Correos eliminados:         {count_correos}")
        print(f"  ✅ Órdenes de compra eliminadas: {count_oc}")
        print("="*60 + "\n")

        return True

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error al eliminar registros: {e}\n")
        return False


def eliminar_reserva_por_id(db, id_reserva):
    """Elimina una reserva específica por su ID"""
    reserva = db.query(Reserva).filter_by(id_reserva=id_reserva).first()

    if not reserva:
        print(f"\n❌ No se encontró la reserva con ID: {id_reserva}\n")
        return False

    print(f"\n📋 Reserva encontrada:")
    print(f"   ID: {reserva.id_reserva}")
    print(f"   Agencia: {reserva.agencia}")
    print(f"   Monto: {reserva.moneda} {reserva.monto_total:,.0f}")
    print(f"   Correos enviados: {len(reserva.correos_enviados)}")
    print(f"   OC recibida: {'Sí' if reserva.orden_compra else 'No'}")
    print()

    confirmacion = input("   ¿Eliminar esta reserva? Escribe 'SI' para confirmar: ")

    if confirmacion.upper() != 'SI':
        print("\n❌ Operación cancelada\n")
        return False

    try:
        db.delete(reserva)
        db.commit()
        print(f"\n✅ Reserva {id_reserva} eliminada exitosamente\n")
        return True

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error al eliminar reserva: {e}\n")
        return False


def eliminar_reservas_test(db):
    """Elimina solo las reservas de prueba (que empiecen con TEST)"""
    reservas_test = db.query(Reserva).filter(
        Reserva.id_reserva.like('TEST%')
    ).all()

    if not reservas_test:
        print("\n❌ No hay reservas de prueba (TEST*) en la base de datos\n")
        return False

    print(f"\n📋 Se encontraron {len(reservas_test)} reservas de prueba:")
    for r in reservas_test:
        print(f"   • {r.id_reserva} - {r.agencia}")
    print()

    confirmacion = input("   ¿Eliminar todas estas reservas de prueba? Escribe 'SI': ")

    if confirmacion.upper() != 'SI':
        print("\n❌ Operación cancelada\n")
        return False

    try:
        count = 0
        for reserva in reservas_test:
            db.delete(reserva)
            count += 1

        db.commit()
        print(f"\n✅ {count} reservas de prueba eliminadas exitosamente\n")
        return True

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error al eliminar reservas: {e}\n")
        return False


def menu_interactivo():
    """Menú interactivo para gestionar la limpieza de datos"""
    init_db()
    db = next(get_db())

    while True:
        print("\n" + "="*60)
        print("  🗑️  LIMPIEZA DE BASE DE DATOS - SISTEMA OC")
        print("="*60)
        print("\n  Opciones:")
        print("  1. Ver estadísticas actuales")
        print("  2. Listar todas las reservas")
        print("  3. Eliminar reserva específica (por ID)")
        print("  4. Eliminar reservas de prueba (TEST*)")
        print("  5. Eliminar TODAS las órdenes de compra 🗑️")
        print("  6. Eliminar TODAS las reservas ⚠️")
        print("  0. Salir")
        print()

        opcion = input("  Selecciona una opción: ").strip()

        if opcion == "1":
            mostrar_estadisticas(db)

        elif opcion == "2":
            listar_reservas(db)

        elif opcion == "3":
            id_reserva = input("\n  Ingresa el ID de la reserva a eliminar: ").strip()
            if id_reserva:
                eliminar_reserva_por_id(db, id_reserva)

        elif opcion == "4":
            eliminar_reservas_test(db)

        elif opcion == "5":
            eliminar_ordenes_compra(db)

        elif opcion == "6":
            eliminado = eliminar_todas_reservas(db)
            if eliminado:
                break  # Salir después de eliminar todo

        elif opcion == "0":
            print("\n👋 Saliendo...\n")
            break

        else:
            print("\n❌ Opción no válida\n")

    db.close()


if __name__ == "__main__":
    import sys

    # Permitir ejecución directa con argumentos
    if len(sys.argv) > 1:
        init_db()
        db = next(get_db())

        if sys.argv[1] == "--all":
            print("\n🗑️  Modo: Eliminar TODAS las reservas\n")
            eliminar_todas_reservas(db)

        elif sys.argv[1] == "--test":
            print("\n🗑️  Modo: Eliminar reservas de prueba (TEST*)\n")
            eliminar_reservas_test(db)

        elif sys.argv[1] == "--stats":
            mostrar_estadisticas(db)

        elif sys.argv[1] == "--list":
            listar_reservas(db)

        elif sys.argv[1] == "--id" and len(sys.argv) > 2:
            eliminar_reserva_por_id(db, sys.argv[2])

        elif sys.argv[1] == "--oc":
            print("\n🗑️  Modo: Eliminar TODAS las órdenes de compra\n")
            eliminar_ordenes_compra(db)

        elif sys.argv[1] == "--help":
            print("\nUso:")
            print("  python limpiar_base_datos.py              # Modo interactivo")
            print("  python limpiar_base_datos.py --all        # Eliminar TODAS las reservas")
            print("  python limpiar_base_datos.py --test       # Eliminar reservas TEST*")
            print("  python limpiar_base_datos.py --oc         # Eliminar TODAS las órdenes de compra")
            print("  python limpiar_base_datos.py --stats      # Ver estadísticas")
            print("  python limpiar_base_datos.py --list       # Listar reservas")
            print("  python limpiar_base_datos.py --id XXXX    # Eliminar reserva específica")
            print()

        else:
            print("\n❌ Argumento no válido. Usa --help para ver opciones\n")

        db.close()

    else:
        # Modo interactivo
        menu_interactivo()

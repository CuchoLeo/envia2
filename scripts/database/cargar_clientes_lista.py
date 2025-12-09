#!/usr/bin/env python3
"""
Script para cargar clientes desde lista proporcionada
Actualiza o crea registros en configuracion_clientes
"""
import sys
import os

# Agregar raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

from database import init_db, get_db, ConfiguracionCliente
from loguru import logger

# Lista de clientes con configuración de OC
CLIENTES_DATA = [
    ("FUNDACION COANIL", False),
    ("TRICOLOR", False),
    ("HTM", False),
    ("MUNDO PACIFICO", False),
    ("HOLDCO SPA", False),
    ("SAVAL", True),
    ("SPARTA", True),
    ("FLEXCO", False),
    ("SOLTEX CHILE S A", False),
    ("SOL SERVICIOS", False),
    ("BRITT CHILE", False),
    ("TECNIGEN S.A", True),
    ("SKY AIRLINE S.A", True),
    ("IFOP", True),
    ("ESSBIO", True),
    ("LUCANO RENT A CAR S.A", True),
    ("ACCIONA AIRPORT SERVICES CHILE SPA (AAS)", True),
    ("CESKAT SYSTEMS SA", False),
    ("PODIUM", False),
    ("FEDRIGONI (RITRAMA)", False),
    ("NUEVOSUR SA", True),
    ("ESVAL", False),
    ("AGUAS DEL VALLE", False),
    ("ACCIONA AIRPORT AMERICAS SPA (AAA)", True),
    ("AIRPORT MAINTENANCE SERVICES SPA", True),
    ("ITA GROUP", False),
    ("BATERIAS TUBULAR S.A.", False),
    ("ULTRACCION", False),
    ("COANIL CAPACITACION LIMITADA", False),
    ("CAPACITACIÓN DHUMANLAB SPA", False),
    ("DINÁMICAS HUMANAS SPA", False),
    ("CASA IDEAS", True),
    ("ELECNOR", False),
    ("COSEMAR SPA", False),
    ("LAB. PASTEUR", True),
    ("CORCHERA", False),
    ("VELTIS SPA (FERROVIAL SERVICIOS)", False),
    ("BERLIAM SPA (FERROVIAL SERVICIOS)", False),
    ("STEEL INGENIERIA SA (FERROVIAL SERVICIOS)", False),
    ("SISDEF", True),
    ("IST", True),
    ("COAGRA", False),
    ("BANAGRO S.A.", False),
    ("MORKEN", True),
    ("CLP INSUMOS", True),
    ("BCI SEGUROS GENERALES S.A.", False),
    ("EXELTIS CHILE SPA", True),
    ("SANTA ROSA CHILE ALIMENTOS LTDA.", False),
    ("TECNORED S.A.", False),
    ("MULTIACEROS S.A.", False),
    ("SOPROLE S.A.", False),
    ("LA CASA DE LAS CARCASAS CHILE SPA", True),
    ("FARMACIAS DOCTOR SIMI", True),
    ("GRUPO MEDICAL", True),
    ("WORKMED", True),
    ("SERVIPAG", True),
    ("KIA-INDUMOTORA", True),
    ("HYUNDAI", True),
    ("AUTOMOTORA DEL PACÍFICO", True),
    ("INDUMOTORA ONE", True),
    ("COSEMAR SERVICIOS INDUSTRIALES SPA", False),
    ("PRESERVA SPA", False),
    ("CEMARC", False),
    ("UNICON", True),
    ("UNACEM", True),
    ("WALVIS S.A.", False),
    ("PRODUCTOS FERNANDEZ S.A.", True),
    ("LABORATORIO ELEA", True),
    ("EVERLLENCE (EX MAN ENERGY SOLUTIONS)", False),
    ("COMERCIAL SANTA ELENA S.A.", False),
    ("SAN JOSE FARMS SPA", True),
    ("EXPORTADORA BAIKA S.A.", True),
    ("GESTACCION CONSULTOREES S.A.", True),
    ("LA CEIBA LTDA.", True),
    ("WILA SPA", True),
    ("BIOTEC", True),
]


def cargar_clientes():
    """Carga o actualiza clientes en la base de datos"""

    print("\n" + "="*70)
    print("  📋 CARGA DE CLIENTES - CONFIGURACIÓN OC")
    print("="*70 + "\n")

    # Inicializar BD
    init_db()
    db = next(get_db())

    print(f"✅ Conexión a base de datos establecida\n")
    print(f"📊 Total de clientes a procesar: {len(CLIENTES_DATA)}\n")

    # Contadores
    creados = 0
    actualizados = 0
    sin_cambios = 0
    errores = 0

    # Procesar cada cliente
    for nombre_agencia, requiere_oc in CLIENTES_DATA:
        try:
            # Buscar cliente existente
            cliente = db.query(ConfiguracionCliente).filter_by(
                nombre_agencia=nombre_agencia
            ).first()

            if cliente:
                # Cliente existe, verificar si necesita actualización
                if cliente.requiere_oc != requiere_oc:
                    cliente.requiere_oc = requiere_oc
                    actualizados += 1
                    accion = "🔄 Actualizado"
                else:
                    sin_cambios += 1
                    accion = "✓ Sin cambios"
            else:
                # Cliente nuevo, crear
                nuevo_cliente = ConfiguracionCliente(
                    nombre_agencia=nombre_agencia,
                    requiere_oc=requiere_oc,
                    activo=True,
                    dias_recordatorio_1=2,
                    dias_recordatorio_2=4
                )
                db.add(nuevo_cliente)
                creados += 1
                accion = "✨ Creado"

            oc_status = "SÍ requiere OC" if requiere_oc else "NO requiere OC"
            print(f"{accion:15} | {nombre_agencia:50} | {oc_status}")

        except Exception as e:
            errores += 1
            logger.error(f"Error procesando {nombre_agencia}: {e}")
            print(f"❌ Error      | {nombre_agencia:50} | {str(e)}")

    # Commit de cambios
    try:
        db.commit()
        print("\n" + "="*70)
        print("  ✅ CAMBIOS GUARDADOS EXITOSAMENTE")
        print("="*70 + "\n")
    except Exception as e:
        db.rollback()
        logger.error(f"Error guardando cambios: {e}")
        print("\n" + "="*70)
        print("  ❌ ERROR GUARDANDO CAMBIOS")
        print("="*70 + "\n")
        print(f"Error: {e}\n")
        return False

    # Resumen
    print("📊 RESUMEN DE OPERACIÓN")
    print("-" * 70)
    print(f"  ✨ Clientes creados:          {creados}")
    print(f"  🔄 Clientes actualizados:     {actualizados}")
    print(f"  ✓  Clientes sin cambios:      {sin_cambios}")
    print(f"  ❌ Errores:                    {errores}")
    print(f"  📋 Total procesados:          {len(CLIENTES_DATA)}")
    print("-" * 70)

    # Estadísticas finales
    total_clientes = db.query(ConfiguracionCliente).count()
    requieren_oc = db.query(ConfiguracionCliente).filter_by(requiere_oc=True).count()
    no_requieren_oc = db.query(ConfiguracionCliente).filter_by(requiere_oc=False).count()

    print(f"\n📈 ESTADÍSTICAS DE BASE DE DATOS")
    print("-" * 70)
    print(f"  👥 Total clientes en BD:      {total_clientes}")
    print(f"  ✅ Requieren OC:              {requieren_oc}")
    print(f"  ⭕ No requieren OC:           {no_requieren_oc}")
    print("-" * 70 + "\n")

    db.close()
    return True


if __name__ == "__main__":
    try:
        exito = cargar_clientes()
        exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario\n")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)

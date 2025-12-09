"""
Script para cargar datos de clientes desde Excel a la base de datos
Lee el archivo docs/clientes.xlsx e inserta/actualiza registros en configuracion_clientes
"""
import sys
import os

# Agregar raíz del proyecto al path Y cambiar directorio de trabajo
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

import pandas as pd
from datetime import datetime
from database import init_db, get_db, ConfiguracionCliente
from config import settings

def cargar_clientes_desde_excel(archivo_excel: str = "docs/clientes.xlsx"):
    """
    Carga clientes desde archivo Excel a la base de datos

    Args:
        archivo_excel: Ruta al archivo Excel con los datos de clientes
    """
    print("=== Cargando Clientes desde Excel ===\n")

    # Inicializar base de datos
    init_db()
    db = next(get_db())

    try:
        # Leer archivo Excel
        print(f"📄 Leyendo archivo: {archivo_excel}")
        df = pd.read_excel(archivo_excel)

        print(f"✅ Archivo leído correctamente")
        print(f"   Total de registros: {len(df)}")
        print(f"   Columnas: {df.columns.tolist()}\n")

        # Validar columnas requeridas
        if 'NOMBRE AGENCIA' not in df.columns or 'OC' not in df.columns:
            raise ValueError("El archivo debe contener las columnas 'NOMBRE AGENCIA' y 'OC'")

        # Limpiar datos duplicados manteniendo el primer registro
        df_original = len(df)
        df = df.drop_duplicates(subset=['NOMBRE AGENCIA'], keep='first')
        if df_original != len(df):
            print(f"⚠️  Se encontraron {df_original - len(df)} duplicados, se mantiene solo el primer registro\n")

        # Estadísticas antes de cargar
        clientes_con_oc = df[df['OC'].str.upper() == 'SI'].shape[0]
        clientes_sin_oc = df[df['OC'].str.upper() == 'NO'].shape[0]

        print(f"📊 Resumen de datos a cargar:")
        print(f"   • Clientes únicos: {len(df)}")
        print(f"   • Requieren OC (SI): {clientes_con_oc}")
        print(f"   • No requieren OC (NO): {clientes_sin_oc}\n")

        # Contadores
        insertados = 0
        actualizados = 0
        errores = 0

        # Procesar cada fila
        print("🔄 Procesando registros...")
        for index, row in df.iterrows():
            try:
                nombre_agencia = str(row['NOMBRE AGENCIA']).strip()
                requiere_oc_valor = str(row['OC']).strip().upper()

                # Validar valores
                if not nombre_agencia or nombre_agencia == 'nan':
                    print(f"   ⚠️  Fila {index + 2}: Nombre de agencia vacío, omitiendo...")
                    errores += 1
                    continue

                # Convertir SI/NO a booleano
                if requiere_oc_valor not in ['SI', 'NO']:
                    print(f"   ⚠️  Fila {index + 2}: Valor OC inválido '{requiere_oc_valor}' para {nombre_agencia}, usando NO por defecto")
                    requiere_oc = False
                else:
                    requiere_oc = requiere_oc_valor == 'SI'

                # Buscar si ya existe el cliente
                cliente_existente = db.query(ConfiguracionCliente).filter_by(
                    nombre_agencia=nombre_agencia
                ).first()

                if cliente_existente:
                    # Actualizar registro existente
                    cliente_existente.requiere_oc = requiere_oc
                    cliente_existente.fecha_actualizacion = datetime.utcnow()
                    actualizados += 1
                    print(f"   ✏️  Actualizado: {nombre_agencia} (OC: {requiere_oc})")
                else:
                    # Crear nuevo registro
                    nuevo_cliente = ConfiguracionCliente(
                        nombre_agencia=nombre_agencia,
                        requiere_oc=requiere_oc,
                        activo=True,
                        dias_recordatorio_1=settings.days_for_reminder_1,
                        dias_recordatorio_2=settings.days_for_reminder_2
                    )
                    db.add(nuevo_cliente)
                    insertados += 1
                    print(f"   ➕ Insertado: {nombre_agencia} (OC: {requiere_oc})")

            except Exception as e:
                errores += 1
                print(f"   ❌ Error en fila {index + 2}: {str(e)}")
                continue

        # Commit de todos los cambios
        db.commit()

        # Resumen final
        print(f"\n{'='*60}")
        print("✅ Proceso completado")
        print(f"{'='*60}")
        print(f"   • Registros insertados: {insertados}")
        print(f"   • Registros actualizados: {actualizados}")
        print(f"   • Errores: {errores}")
        print(f"   • Total procesados: {insertados + actualizados}")
        print(f"{'='*60}\n")

        # Verificar total en base de datos
        total_en_db = db.query(ConfiguracionCliente).count()
        print(f"📊 Total de clientes en base de datos: {total_en_db}")

        # Mostrar algunos ejemplos de clientes que requieren OC
        clientes_con_oc = db.query(ConfiguracionCliente).filter_by(requiere_oc=True).limit(5).all()
        if clientes_con_oc:
            print(f"\n🔍 Ejemplos de clientes que requieren OC:")
            for cliente in clientes_con_oc:
                print(f"   • {cliente.nombre_agencia}")

        return True

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {archivo_excel}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    exito = cargar_clientes_desde_excel()
    if exito:
        print("\n✅ Clientes cargados exitosamente desde Excel")
    else:
        print("\n❌ Hubo errores al cargar los clientes")

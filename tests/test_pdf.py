#!/usr/bin/env python3
"""
Script de prueba para el procesador de PDF
Prueba la extracción de datos del PDF de ejemplo
"""
import sys
from pathlib import Path

try:
    from src.pdf_processor import pdf_processor
    from loguru import logger
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("💡 Ejecuta primero: pip install -r requirements.txt")
    sys.exit(1)


def test_pdf(pdf_path: str):
    """Prueba la extracción de un PDF"""
    print("=" * 60)
    print("🧪 Test del Procesador de PDF")
    print("=" * 60)
    print()

    # Verificar que existe el archivo
    if not Path(pdf_path).exists():
        print(f"❌ Archivo no encontrado: {pdf_path}")
        return False

    print(f"📄 Procesando: {pdf_path}")
    print()

    # Extraer datos
    try:
        data = pdf_processor.extract_from_file(pdf_path)

        if not data:
            print("❌ No se pudieron extraer datos del PDF")
            return False

        # Mostrar datos extraídos
        print("✅ Datos extraídos exitosamente:")
        print()
        print("📋 INFORMACIÓN DE LA RESERVA")
        print("-" * 60)

        campos = [
            ("ID de Reserva", "id_reserva"),
            ("LOC Interno", "loc_interno"),
            ("Localizador", "localizador"),
            ("Agencia", "agencia"),
            ("Hotel", "nombre_hotel"),
            ("Dirección", "direccion_hotel"),
            ("Teléfono", "telefono_hotel"),
            ("Check-in", "fecha_checkin"),
            ("Check-out", "fecha_checkout"),
            ("Hora Llegada", "hora_llegada"),
            ("Hora Salida", "hora_salida"),
            ("Noches", "numero_noches"),
            ("Habitaciones", "numero_habitaciones"),
            ("Monto Total", "monto_total"),
            ("Moneda", "moneda"),
            ("Límite Cancelación", "fecha_limite_cancelacion"),
            ("Fecha Emisión", "fecha_emision"),
        ]

        for nombre, clave in campos:
            valor = data.get(clave)
            if valor:
                print(f"  {nombre:20}: {valor}")

        # Validar datos
        print()
        print("🔍 VALIDACIÓN")
        print("-" * 60)

        is_valid, errors = pdf_processor.validate_data(data)

        if is_valid:
            print("✅ Datos válidos - Todos los campos obligatorios presentes")
        else:
            print("⚠️  Advertencias de validación:")
            for error in errors:
                print(f"  - {error}")

        # Resumen
        print()
        print("=" * 60)
        print("📊 RESUMEN")
        print("=" * 60)
        print(f"  Reserva ID: {data.get('id_reserva', 'N/A')}")
        print(f"  Agencia: {data.get('agencia', 'N/A')}")
        print(f"  Monto: {data.get('moneda', 'CLP')} {data.get('monto_total', 0):,.0f}")
        print(f"  Campos extraídos: {len([v for v in data.values() if v is not None])}/{len(data)}")
        print()

        return True

    except Exception as e:
        print(f"❌ Error procesando PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Archivo PDF de prueba (en carpeta data/)
    pdf_file = Path(__file__).parent.parent / "data" / "resumen del servicio.pdf"

    if len(sys.argv) > 1:
        pdf_file = Path(sys.argv[1])

    success = test_pdf(pdf_file)

    if success:
        print("✅ Test completado exitosamente")
        sys.exit(0)
    else:
        print("❌ Test falló")
        sys.exit(1)

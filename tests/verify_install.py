#!/usr/bin/env python3
"""
Script de verificación de instalación
Verifica que todas las dependencias estén correctamente instaladas
"""
import sys

print("🔍 Verificando instalación del Sistema de Seguimiento OC...")
print("=" * 60)

# Lista de módulos requeridos
required_modules = [
    ('fastapi', 'FastAPI'),
    ('uvicorn', 'Uvicorn'),
    ('sqlalchemy', 'SQLAlchemy'),
    # ('imapclient', 'IMAPClient'),  # No necesario - usamos wrapper personalizado
    ('pdfplumber', 'pdfplumber'),
    ('PyPDF2', 'PyPDF2'),
    ('apscheduler', 'APScheduler'),
    ('jinja2', 'Jinja2'),
    ('dotenv', 'python-dotenv'),
    ('pydantic', 'Pydantic'),
    ('pydantic_settings', 'pydantic-settings'),
    ('loguru', 'Loguru'),
]

missing_modules = []
installed_modules = []

for module_name, display_name in required_modules:
    try:
        __import__(module_name)
        installed_modules.append(display_name)
        print(f"✅ {display_name:20} - Instalado")
    except ImportError:
        missing_modules.append(display_name)
        print(f"❌ {display_name:20} - Falta")

print("=" * 60)

if missing_modules:
    print(f"\n⚠️  Faltan {len(missing_modules)} módulos:")
    for module in missing_modules:
        print(f"  - {module}")
    print("\n💡 Ejecuta: pip install -r requirements.txt")
    sys.exit(1)
else:
    print(f"\n✅ Todos los módulos están instalados ({len(installed_modules)}/{len(required_modules)})")
    print("\n📚 Módulos estándar de Python (no requieren instalación):")
    print("  - email")
    print("  - imaplib (usamos wrapper personalizado)")
    print("  - smtplib")
    print("  - datetime")
    print("  - pathlib")

    print("\n📦 Módulos personalizados del proyecto:")
    print("  - imap_wrapper.py (compatible con Python 3.14+)")

    print("\n🎉 Sistema listo para usar!")
    print("\n📝 Próximos pasos:")
    print("  1. Configura tus credenciales en .env")
    print("  2. Ejecuta: python app.py")
    print("  3. Abre: http://localhost:8001")

    sys.exit(0)

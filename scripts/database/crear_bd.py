#!/usr/bin/env python3
"""Script para crear las tablas de la base de datos"""
import sys
import os

# Agregar raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

from database import Base, engine, SessionLocal, ConfiguracionCliente
from datetime import datetime

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

print("✅ Tablas creadas")

# Crear sesión e insertar clientes
db = SessionLocal()

# Verificar si ya existen clientes
existing = db.query(ConfiguracionCliente).count()
if existing == 0:
    clientes = [
        ConfiguracionCliente(
            nombre_agencia='WALVIS S.A.',
            requiere_oc=True,
            activo=True,
            fecha_creacion=datetime.now()
        ),
        ConfiguracionCliente(
            nombre_agencia='EMPRESA CORPORATIVA LTDA',
            requiere_oc=True,
            activo=True,
            fecha_creacion=datetime.now()
        ),
        ConfiguracionCliente(
            nombre_agencia='AGENCIA VIAJES XYZ',
            requiere_oc=True,
            activo=True,
            fecha_creacion=datetime.now()
        )
    ]

    for cliente in clientes:
        db.add(cliente)

    db.commit()
    print("✅ Clientes configurados")
else:
    print(f"✅ Ya existen {existing} clientes configurados")

db.close()
print("✅ Base de datos inicializada")

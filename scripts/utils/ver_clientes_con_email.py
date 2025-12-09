#!/usr/bin/env python3
"""Script temporal para ver clientes con email"""
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

from database import init_db, get_db, ConfiguracionCliente

init_db()
db = next(get_db())

# Buscar clientes CON email
con_email = db.query(ConfiguracionCliente).filter(
    ConfiguracionCliente.email_contacto.isnot(None),
    ConfiguracionCliente.email_contacto != ''
).all()

print('\nClientes CON email configurado:')
print('=' * 70)
for c in con_email:
    oc_status = 'SÍ' if c.requiere_oc else 'NO'
    print(f'{c.nombre_agencia:<45} | {c.email_contacto:<30} | OC: {oc_status}')
print('=' * 70)
print(f'Total CON email: {len(con_email)}\n')

# Ver total
total = db.query(ConfiguracionCliente).count()
con_oc = db.query(ConfiguracionCliente).filter_by(requiere_oc=True).count()
sin_oc = db.query(ConfiguracionCliente).filter_by(requiere_oc=False).count()

print(f'Total de clientes en BD: {total}')
print(f'  - Requieren OC: {con_oc}')
print(f'  - NO requieren OC: {sin_oc}\n')

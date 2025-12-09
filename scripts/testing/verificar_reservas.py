#!/usr/bin/env python3
"""Script para verificar reservas en la BD"""
import sqlite3

db = sqlite3.connect('oc_seguimiento.db')
cursor = db.cursor()

print("=== RESERVAS EN SISTEMA ===")
cursor.execute("SELECT id_reserva, agencia, estado_oc, requiere_oc, fecha_creacion FROM reservas ORDER BY fecha_creacion DESC")
reservas = cursor.fetchall()

if reservas:
    for r in reservas:
        print(f"\n📋 Reserva: {r[0]}")
        print(f"   Agencia: {r[1]}")
        print(f"   Estado: {r[2]}")
        print(f"   Requiere OC: {'Sí' if r[3] else 'No'}")
        print(f"   Fecha: {r[4]}")
else:
    print("❌ No hay reservas en el sistema aún")

print("\n=== CORREOS ENVIADOS ===")
cursor.execute("""
    SELECT ce.tipo_correo, ce.destinatario, ce.asunto, ce.estado, ce.fecha_enviado
    FROM correos_enviados ce
    ORDER BY ce.fecha_creacion DESC
""")
correos = cursor.fetchall()

if correos:
    for c in correos:
        print(f"\n📧 {c[0]}")
        print(f"   Para: {c[1]}")
        print(f"   Asunto: {c[2]}")
        print(f"   Estado: {c[3]}")
        print(f"   Enviado: {c[4]}")
else:
    print("❌ No se han enviado correos aún")

db.close()

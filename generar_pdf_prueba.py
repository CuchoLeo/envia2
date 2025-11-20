#!/usr/bin/env python3
"""
Genera un PDF de prueba para el sistema de seguimiento de OC
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime, timedelta

# Crear PDF
filename = "confirmacion_reserva_prueba.pdf"
doc = SimpleDocTemplate(filename, pagesize=letter)
elements = []

# Estilos
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#2c3e50'),
    spaceAfter=30,
    alignment=1  # Center
)

header_style = ParagraphStyle(
    'CustomHeader',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#34495e'),
    spaceAfter=12
)

# Título
elements.append(Paragraph("CONFIRMACIÓN DE RESERVA", title_style))
elements.append(Spacer(1, 0.3*inch))

# Información de la reserva
fecha_hoy = datetime.now().strftime("%d/%m/%Y")
fecha_checkin = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
fecha_checkout = (datetime.now() + timedelta(days=33)).strftime("%d/%m/%Y")

data = [
    ['LOC Interno:', 'TEST2024001'],
    ['Localizador:', '987654'],
    ['Agencia:', 'Turismo Global S.A.'],
    ['Fecha Emision:', fecha_hoy],
    ['', ''],
    ['DETALLES DEL HOTEL', ''],
    ['Hotel:', 'Hotel Plaza Santiago'],
    ['Dirección:', 'Av. Libertador Bernardo O\'Higgins 136, Santiago'],
    ['Teléfono:', '+56 2 2345 6789'],
    ['', ''],
    ['FECHAS Y HORARIOS', ''],
    ['Check In:', f'Lunes 15, diciembre. 2025'],
    ['Hora Llegada:', '3:00 PM'],
    ['Check Out:', f'Jueves 18, diciembre. 2025'],
    ['Hora Salida:', '12:00 PM'],
    ['Noches:', '3'],
    ['', ''],
    ['DETALLES DE LA RESERVA', ''],
    ['Habitaciones:', '2'],
    ['Tipo:', '1 Doble + 1 Simple'],
    ['', ''],
    ['MONTO', ''],
    ['Total:', 'CLP 450.000'],
]

# Crear tabla
table = Table(data, colWidths=[2.5*inch, 4*inch])
table.setStyle(TableStyle([
    # Estilos generales
    ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
    ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),

    # Headers de sección (fondo gris)
    ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#ecf0f1')),
    ('BACKGROUND', (0, 10), (-1, 10), colors.HexColor('#ecf0f1')),
    ('BACKGROUND', (0, 17), (-1, 17), colors.HexColor('#ecf0f1')),
    ('BACKGROUND', (0, 21), (-1, 21), colors.HexColor('#ecf0f1')),
    ('FONT', (0, 5), (-1, 5), 'Helvetica-Bold', 11),
    ('FONT', (0, 10), (-1, 10), 'Helvetica-Bold', 11),
    ('FONT', (0, 17), (-1, 17), 'Helvetica-Bold', 11),
    ('FONT', (0, 21), (-1, 21), 'Helvetica-Bold', 11),
    ('SPAN', (0, 5), (-1, 5)),
    ('SPAN', (0, 10), (-1, 10)),
    ('SPAN', (0, 17), (-1, 17)),
    ('SPAN', (0, 21), (-1, 21)),

    # Total destacado
    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#3498db')),
    ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
    ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 12),
    ('SPAN', (0, -1), (-1, -1)),
    ('ALIGN', (0, -1), (-1, -1), 'CENTER'),

    # Padding
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
]))

elements.append(table)
elements.append(Spacer(1, 0.5*inch))

# Notas al pie
nota_style = ParagraphStyle(
    'Nota',
    parent=styles['Normal'],
    fontSize=9,
    textColor=colors.HexColor('#7f8c8d'),
    alignment=1
)
elements.append(Paragraph("Por favor, enviar Orden de Compra para proceder con la reserva", nota_style))
elements.append(Spacer(1, 0.2*inch))
elements.append(Paragraph("Kontrol Travel - Sistema Automático", nota_style))

# Generar PDF
doc.build(elements)
print(f"✅ PDF generado: {filename}")
print(f"\n📋 Datos de la reserva:")
print(f"   LOC Interno: TEST2024001")
print(f"   Agencia: Turismo Global S.A.")
print(f"   Hotel: Hotel Plaza Santiago")
print(f"   Check In: 15 diciembre 2025")
print(f"   Check Out: 18 diciembre 2025")
print(f"   Total: CLP 450.000")
print(f"\n📧 Ahora puedes:")
print(f"   1. Enviar este PDF desde v.rodriguezy@gmail.com")
print(f"   2. A: seguimientoocx@gmail.com")
print(f"   3. Asunto: 'Confirmación de Reserva Hotel Plaza'")

# 📋 Plan de Pruebas con Cliente

**Fecha:** 2025-11-17
**Sistema:** Seguimiento de Órdenes de Compra
**Cliente:** Kontrol Travel

---

## 🎯 Objetivo

Validar el funcionamiento completo del sistema antes de pasar a producción.

---

## ✅ Pre-requisitos

- [ ] 1-2 cuentas de Gmail configuradas
- [ ] Contraseñas de aplicación de Gmail generadas
- [ ] Verificación en 2 pasos habilitada en Gmail
- [ ] Información de agencias recopilada
- [ ] 2-3 PDFs de confirmación reales del cliente

---

## 🧪 Fase 1: Pruebas de Configuración (30 min)

### Test 1.1: Conexión IMAP
```bash
python3 -c "
from src.imap_wrapper import SimpleIMAPClient
from config import settings

client = SimpleIMAPClient(
    host=settings.imap_host,
    port=settings.imap_port,
    username=settings.imap_username,
    password=settings.imap_password,
    use_ssl=settings.imap_use_ssl
)
client.connect()
print('✅ Conexión IMAP exitosa')
"
```

**Resultado Esperado:** ✅ Conexión y autenticación exitosa

### Test 1.2: Conexión SMTP
```bash
python3 -c "
import smtplib
from config import settings

with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
    server.starttls()
    server.login(settings.smtp_username, settings.smtp_password)
    print('✅ Conexión SMTP exitosa')
"
```

**Resultado Esperado:** ✅ Login exitoso

### Test 1.3: Verificar Configuración de Clientes
```bash
python3 -c "
from database import get_db, ConfiguracionCliente, init_db
init_db()
db = next(get_db())
clientes = db.query(ConfiguracionCliente).all()
print(f'Total clientes configurados: {len(clientes)}')
for c in clientes:
    print(f'  - {c.nombre_agencia}: {c.email_contacto} (Requiere OC: {c.requiere_oc})')
db.close()
"
```

**Resultado Esperado:** Lista de todas las agencias configuradas

---

## 🧪 Fase 2: Pruebas con PDFs Reales (1 hora)

### Test 2.1: Procesamiento de PDF Real

**Pasos:**
1. Solicitar al cliente 2-3 PDFs de confirmación reales
2. Copiar PDFs a `data/`
3. Ejecutar extracción:

```bash
python3 -c "
from src.pdf_processor import pdf_processor
from pathlib import Path

pdf_path = Path('data/confirmacion_real_1.pdf')
datos = pdf_processor.extract_from_file(pdf_path)
print('Datos extraídos:')
print(f'  ID Reserva: {datos.get(\"id_reserva\")}')
print(f'  Agencia: {datos.get(\"agencia\")}')
print(f'  Hotel: {datos.get(\"nombre_hotel\")}')
print(f'  Monto: {datos.get(\"monto_total\")}')
"
```

**Resultado Esperado:** Todos los campos extraídos correctamente

**Si falla:** Ajustar regex en `src/pdf_processor.py` según formato del cliente

### Test 2.2: Crear Reserva desde PDF Real

```bash
cd scripts
python3 crear_reserva_desde_pdf.py ../data/confirmacion_real_1.pdf
```

**Resultado Esperado:** Reserva creada en BD con todos los datos

---

## 🧪 Fase 3: Flujo Completo End-to-End (2 horas)

### Test 3.1: Detección de Confirmación

**Pasos:**
1. Cliente envía email de confirmación REAL a la bandeja configurada
2. Iniciar servidor: `python3 app.py`
3. Esperar 1-2 minutos
4. Verificar en logs:

```
✅ Encontrados 1 correos no leídos
✅ Procesando correo: Confirmación de Reserva...
✅ Datos extraídos: ID=XXXXX, Agencia=...
✅ Nueva reserva creada: XXXXX
```

**Verificar en BD:**
```bash
python3 -c "
from database import get_db, Reserva, init_db
init_db()
db = next(get_db())
reservas = db.query(Reserva).filter_by(requiere_oc=True).all()
print(f'Total reservas: {len(reservas)}')
for r in reservas:
    print(f'  {r.id_reserva} - {r.agencia} - Estado: {r.estado_oc}')
db.close()
"
```

**Resultado Esperado:** Reserva detectada y creada con estado PENDIENTE

### Test 3.2: Envío de Solicitud de OC

**Opción A - Automático (esperar ~5 min):**
El scheduler enviará automáticamente

**Opción B - Manual:**
```bash
cd scripts
python3 enviar_solicitud_oc.py
# Seleccionar la reserva
# Seleccionar "Solicitud Inicial"
# Confirmar envío
```

**Verificar:**
1. Email llegó al cliente (revisar con ellos)
2. Email tiene formato correcto
3. Datos de la reserva son correctos
4. Links funcionan

**Resultado Esperado:** Email de solicitud recibido por el cliente

### Test 3.3: Recepción de OC

**Pasos:**
1. Solicitar al cliente que responda el email con:
   - Asunto conteniendo "Orden de Compra" o "OC"
   - Adjuntar PDF (puede ser cualquier PDF de prueba)
   - Mencionar el ID de reserva en el cuerpo
2. Esperar 1-2 minutos
3. Verificar logs del servidor

**Verificar en BD:**
```bash
python3 -c "
from database import get_db, Reserva, OrdenCompra, init_db
init_db()
db = next(get_db())
reserva = db.query(Reserva).first()
print(f'Estado: {reserva.estado_oc}')
oc = db.query(OrdenCompra).filter_by(reserva_id=reserva.id).first()
if oc:
    print(f'OC: {oc.archivo_nombre} - {oc.email_remitente}')
db.close()
"
```

**Resultado Esperado:**
- Estado cambia a RECIBIDA
- OC registrada en BD

---

## 🧪 Fase 4: Pruebas de Recordatorios (3-4 días)

### Test 4.1: Primer Recordatorio

**Setup:**
1. Modificar temporalmente `DAYS_FOR_REMINDER_1=0` en `.env`
2. Reiniciar servidor
3. Esperar ciclo del scheduler (~5 min)

**Resultado Esperado:** Email de recordatorio 1 enviado

### Test 4.2: Segundo Recordatorio

**Setup:**
1. Modificar `DAYS_FOR_REMINDER_2=0` en `.env`
2. Esperar ciclo

**Resultado Esperado:** Email de recordatorio 2 enviado

### Test 4.3: Ultimátum

**Resultado Esperado:** Email de ultimátum con tono urgente

---

## 🧪 Fase 5: Pruebas de Estrés (Opcional)

### Test 5.1: Múltiples Reservas Simultáneas

**Pasos:**
1. Enviar 5-10 emails de confirmación
2. Verificar que todos se procesen
3. Verificar que no haya duplicados

### Test 5.2: Correos con Formato Diferente

**Pasos:**
1. Probar con diferentes formatos de PDF del cliente
2. Ajustar regex si es necesario

---

## 📊 Criterios de Éxito

Para pasar a producción, TODOS estos deben estar ✅:

### Detección de Confirmaciones
- [ ] Detecta emails correctamente
- [ ] Extrae datos del PDF sin errores
- [ ] Crea reserva en BD con todos los campos
- [ ] Identifica correctamente agencias que requieren OC

### Envío de Solicitudes
- [ ] Emails se envían a destinatarios correctos
- [ ] Templates se ven bien en Gmail/Outlook
- [ ] Links funcionan
- [ ] CC a administración funciona

### Recepción de OC
- [ ] Detecta respuestas con OC
- [ ] Asocia correctamente con reserva
- [ ] Actualiza estado a RECIBIDA
- [ ] Guarda adjuntos

### Recordatorios
- [ ] Se envían en días correctos
- [ ] No envía duplicados
- [ ] Tono escala apropiadamente

### Sistema General
- [ ] No hay crashes en 24 horas
- [ ] Logs son claros
- [ ] No consume recursos excesivos
- [ ] Reconecta automáticamente si falla IMAP

---

## 🐛 Registro de Problemas

| Fecha | Problema | Solución | Estado |
|-------|----------|----------|--------|
| | | | |

---

## 📞 Contacto durante Pruebas

**Soporte Técnico:** [Tu contacto]
**Horario de Pruebas:** Lunes-Viernes 9:00-18:00
**Tiempo Estimado Total:** 2-3 días

---

## ✅ Firma de Aprobación

Aprobado para producción:

**Cliente:** _________________ Fecha: _______
**Técnico:** _________________ Fecha: _______

---

**Notas:**
- Mantener logs de todos los tests
- Documentar cualquier ajuste necesario
- Backup de BD antes de cada fase

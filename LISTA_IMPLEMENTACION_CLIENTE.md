# ✅ Lista de Implementación con Cliente

**Sistema de Seguimiento de OC - Kontrol Travel**
**Fecha:** 2025-11-17

---

## 📋 RESPUESTA A TU PREGUNTA

### ¿Cuántos correos necesito?

**Respuesta:** **SOLO 1 cuenta de Gmail**

### 📧 Cuenta Necesaria:

**`seguimientoocx@gmail.com`** (o similar)

Esta cuenta hace TODO:
- ✅ Recibe confirmaciones de `kontroltravel@ideasfractal.com`
- ✅ Detecta qué agencias requieren OC
- ✅ Envía solicitudes de OC a las agencias
- ✅ Envía recordatorios automáticos
- ✅ Recibe respuestas con OC
- ✅ Confirma recepción

### 🔄 Flujo Completo:

```
kontroltravel@ideasfractal.com
         │
         ├─> Envía PDF confirmación al cliente
         │
         └─> Envía PDF confirmación a seguimientoocx@gmail.com
                    │
                    ├─> Sistema detecta y procesa
                    ├─> Identifica si requiere OC
                    ├─> Envía solicitud a agencia
                    ├─> Envía recordatorios (días 2, 4, 6)
                    └─> Recibe OC de la agencia
```

**✅ Solo necesitas 1 cuenta Gmail**

---

## 📝 INFORMACIÓN A SOLICITAR

### ✅ INFORMACIÓN MÍNIMA (Obligatoria):

1. **Cuenta de Email:**
   - [ ] 1 email de Gmail: `seguimientoocx@gmail.com` (o similar)
   - [ ] Contraseña de aplicación de Gmail (requiere verificación en 2 pasos)
   - [ ] IMAP habilitado en Gmail (habilitado por defecto)

2. **Lista de Agencias:**
   - [ ] Nombres de agencias que requieren OC
   - [ ] Email de contacto de cada agencia
   - [ ] Teléfono (opcional)

3. **PDFs de Ejemplo:**
   - [ ] 2-3 PDFs reales de confirmación de reserva
   - Necesarios para configurar la extracción de datos

### ✅ INFORMACIÓN ADICIONAL (Recomendada):

4. **Configuración de Recordatorios:**
   - [ ] ¿Cuántos días para 1er recordatorio? (sugerido: 2)
   - [ ] ¿Cuántos días para 2do recordatorio? (sugerido: 4)

5. **Emails en Copia:**
   - [ ] Email de administración
   - [ ] Email de finanzas/contabilidad
   - [ ] Otros (opcional)

6. **Branding (Opcional):**
   - [ ] Logo de la empresa (PNG, 200x60px)
   - [ ] Color corporativo (#hexadecimal)

---

## 📁 DOCUMENTOS PARA ENVIAR AL CLIENTE

He creado estos documentos listos para enviar:

### 1. **Para el Cliente (Enviar estos):**

```
📄 docs/RESUMEN_PARA_CLIENTE.md
   → Explicación ejecutiva del sistema (1 página)

📄 docs/SOLICITUD_INFO_CLIENTE.md
   → Formulario a completar con toda la info necesaria
   → ENVIAR ESTE PRIMERO ✅
```

### 2. **Para Ti (Uso Interno):**

```
📄 docs/PLAN_PRUEBAS_CLIENTE.md
   → Plan completo de testing (2-3 días)

📄 scripts/configurar_cliente.py
   → Script interactivo para configurar .env

📄 scripts/test_conexion.py
   → Verificar que todo funciona antes de empezar
```

---

## 🚀 PROCESO PASO A PASO

### FASE 1: Solicitud de Información (1-2 días)

```bash
# 1. Enviar al cliente:
- docs/RESUMEN_PARA_CLIENTE.md
- docs/SOLICITUD_INFO_CLIENTE.md

# 2. Esperar que cliente complete y envíe:
- Información de correos
- Lista de agencias
- 2-3 PDFs de ejemplo
```

**Output esperado:**
- ✅ 1 email de Gmail (`seguimientoocx@gmail.com`) con contraseña de aplicación
- ✅ Verificación en 2 pasos habilitada
- ✅ Lista de ~5-10 agencias con emails
- ✅ 2-3 PDFs reales de confirmación

---

### FASE 2: Configuración Inicial (1 día)

```bash
# 1. Configurar el sistema con la info del cliente
cd /path/to/envia2
python3 scripts/configurar_cliente.py

# El script te guiará interactivamente y creará el .env

# 2. Verificar configuración
cat .env  # Revisar que todo esté correcto

# 3. Configurar emails de contacto de agencias
# (Editar manualmente en BD o crear script)

# 4. Copiar PDFs del cliente a data/
cp /path/to/cliente_pdfs/*.pdf data/

# 5. Probar extracción de PDFs
python3 -c "
from src.pdf_processor import pdf_processor
from pathlib import Path
for pdf in Path('data').glob('*.pdf'):
    print(f'\nProcesando: {pdf.name}')
    datos = pdf_processor.extract_from_file(pdf)
    print(f'  ID: {datos.get(\"id_reserva\")}')
    print(f'  Agencia: {datos.get(\"agencia\")}')
"

# Si hay errores de extracción, ajustar regex en src/pdf_processor.py
```

**Output esperado:**
- ✅ Archivo .env configurado
- ✅ PDFs se extraen correctamente
- ✅ Agencias en base de datos

---

### FASE 3: Verificación de Conexiones (30 min)

```bash
# Ejecutar suite de tests
python3 scripts/test_conexion.py

# Debe mostrar:
# ✅ PASS  IMAP Confirmaciones
# ✅ PASS  IMAP OC
# ✅ PASS  SMTP
# ✅ PASS  Base de Datos
# ✅ PASS  Templates
# ✅ PASS  Configuración
#
# Total: 6/6 tests pasados
# ✅ TODOS LOS TESTS PASARON - SISTEMA LISTO
```

**Si algún test falla:**
- IMAP/SMTP: Verificar contraseñas de aplicación
- Base de datos: `rm data/oc_seguimiento.db` y reintentar
- Templates: Verificar que existen en `templates/`

---

### FASE 4: Pruebas con Cliente (2-3 días)

Seguir el plan detallado en `docs/PLAN_PRUEBAS_CLIENTE.md`

**Resumen de pruebas:**

#### Test 1: Detección de Confirmación (1 hora)
```bash
# 1. Cliente envía email de confirmación REAL
# 2. Iniciar servidor
python3 app.py

# 3. Verificar logs - debe mostrar:
#    ✅ Encontrados 1 correos no leídos
#    ✅ Procesando correo: Confirmación...
#    ✅ Nueva reserva creada

# 4. Verificar en BD
python3 -c "
from database import get_db, Reserva, init_db
init_db()
db = next(get_db())
reservas = db.query(Reserva).filter_by(requiere_oc=True).all()
for r in reservas:
    print(f'{r.id_reserva} - {r.agencia} - {r.estado_oc}')
db.close()
"
```

#### Test 2: Envío de Solicitud (30 min)
```bash
# Opción A: Esperar ~5 min (automático)
# Opción B: Manual
cd scripts
python3 enviar_solicitud_oc.py
# Seleccionar reserva → Solicitud Inicial → Confirmar

# Verificar con cliente que recibió el email
```

#### Test 3: Recepción de OC (30 min)
```bash
# 1. Cliente responde con:
#    - Asunto: "Orden de Compra" o "OC"
#    - Adjunto: Cualquier PDF
#    - Menciona ID de reserva en cuerpo

# 2. Esperar 1-2 minutos

# 3. Verificar estado cambió a RECIBIDA
python3 -c "
from database import get_db, Reserva, init_db
init_db()
db = next(get_db())
reserva = db.query(Reserva).first()
print(f'Estado: {reserva.estado_oc}')  # Debe ser RECIBIDA
db.close()
"
```

#### Test 4: Recordatorios (Días siguientes)
```bash
# Para acelerar tests, temporalmente:
# 1. Editar .env:
#    DAYS_FOR_REMINDER_1=0
#    DAYS_FOR_REMINDER_2=0
# 2. Reiniciar servidor
# 3. Esperar ~5 min
# 4. Verificar emails de recordatorio enviados
```

**Output esperado:**
- ✅ Confirmaciones detectadas automáticamente
- ✅ Solicitudes enviadas correctamente
- ✅ OC recibidas y procesadas
- ✅ Recordatorios funcionando

---

### FASE 5: Producción (Deploy)

**Opción A: Google Cloud Platform (Recomendado)**

```bash
# Ver documentación en:
deployment/DESPLIEGUE_GCP.md

# Resumen:
# 1. Crear proyecto en GCP
# 2. Configurar Cloud Run
# 3. Deploy automático
# 4. Monitoreo activo

# Costo: ~$12 USD/mes
```

**Opción B: Servidor Local**

```bash
# 1. Copiar todo el proyecto al servidor
rsync -avz envia2/ usuario@servidor:/home/usuario/envia2/

# 2. Instalar dependencias
ssh usuario@servidor
cd envia2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Crear servicio systemd
sudo nano /etc/systemd/system/oc-sistema.service

# [Unit]
# Description=Sistema Seguimiento OC
# After=network.target
#
# [Service]
# Type=simple
# User=usuario
# WorkingDirectory=/home/usuario/envia2
# ExecStart=/home/usuario/envia2/venv/bin/python3 app.py
# Restart=always
#
# [Install]
# WantedBy=multi-user.target

# 4. Iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable oc-sistema
sudo systemctl start oc-sistema
sudo systemctl status oc-sistema

# 5. Verificar
curl http://localhost:8001/health
```

---

## ✅ CHECKLIST FINAL

Antes de declarar "listo para producción":

### Funcionalidad:
- [ ] Detecta confirmaciones correctamente
- [ ] Extrae datos del PDF sin errores
- [ ] Envía solicitudes a emails correctos
- [ ] Recordatorios se envían en días correctos
- [ ] Recibe y procesa OC correctamente
- [ ] Estado se actualiza automáticamente

### Configuración:
- [ ] Todas las agencias están en BD
- [ ] Emails de contacto verificados
- [ ] Templates personalizados (si aplica)
- [ ] CC configurados
- [ ] Días de recordatorio ajustados

### Sistema:
- [ ] No hay crashes en 24 horas
- [ ] Reconecta automáticamente si falla IMAP
- [ ] Logs son claros y útiles
- [ ] Backup de BD configurado

### Cliente:
- [ ] Cliente ha probado el flujo completo
- [ ] Cliente aprueba el contenido de emails
- [ ] Cliente entiende el panel web
- [ ] Cliente satisfecho con el sistema

---

## 📞 DURANTE LA IMPLEMENTACIÓN

**Mantén contacto frecuente con el cliente:**

- ✅ Día 1: Confirmación de recepción de info
- ✅ Día 2: Confirmación de configuración completada
- ✅ Día 3-4: Updates diarios durante pruebas
- ✅ Día 5: Revisión final y go-live

**Documentar todo:**
- Problemas encontrados y soluciones
- Ajustes específicos del cliente
- Configuración final
- Credenciales de acceso

---

## 🎯 RESUMEN EJECUTIVO

### ¿Qué solicitar?
**Mínimo:** 1 email de Gmail (`seguimientoocx@gmail.com`) + lista agencias + 2-3 PDFs

### ¿Cómo funciona el flujo?
`kontroltravel@ideasfractal.com` envía confirmaciones a `seguimientoocx@gmail.com`, que gestiona TODO el ciclo de OC automáticamente

### ¿Cuánto tiempo?
**Total:** 5-7 días desde recepción de info

### ¿Qué documentos enviar?
**Primero:** `docs/SOLICITUD_INFO_CLIENTE.md`
**Después:** `docs/RESUMEN_PARA_CLIENTE.md`

### ¿Cómo configurar?
**Script:** `python3 scripts/configurar_cliente.py`
**Verificar:** `python3 scripts/test_conexion.py`

### ¿Cómo probar?
**Seguir:** `docs/PLAN_PRUEBAS_CLIENTE.md`

---

## 💡 TIPS

1. **Pide los PDFs primero** - Son críticos para configurar la extracción

2. **Usa el configurador** - El script `configurar_cliente.py` evita errores

3. **Prueba con datos reales** - No con datos de prueba

4. **Documenta ajustes** - Si modificas regex o templates

5. **Backup siempre** - Antes de cada fase de pruebas

6. **Logs completos** - Ayudan mucho para troubleshooting

7. **Cliente involucrado** - Que pruebe cada fase contigo

---

## 🚨 PROBLEMAS COMUNES

### "No detecta los PDFs"
→ Ajustar regex en `src/pdf_processor.py`
→ Ver `docs/troubleshooting/`

### "Emails no se envían"
→ Verificar contraseña de aplicación
→ Ejecutar `scripts/test_conexion.py`

### "Estado no se actualiza"
→ Verificar que OC tiene adjunto PDF
→ Verificar que asunto contiene "OC" o "Orden de Compra"

### "Base de datos corrupta"
→ `rm data/oc_seguimiento.db`
→ Reiniciar sistema

---

**¿Listo para empezar?** 🚀

**Siguiente paso:**
```bash
# Enviar al cliente:
docs/SOLICITUD_INFO_CLIENTE.md
```

**¡Éxito con la implementación!** 💪

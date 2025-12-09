# 🧪 Guía de Prueba Local con Gmail Personal

Guía paso a paso para probar el Sistema de Seguimiento de OC usando 2 cuentas Gmail personales.

**Versión**: 1.3.0 | **Última actualización**: 8 de Diciembre de 2024

> 📖 **Para inicio rápido**: Ver `INICIO_RAPIDO.md` para configuración en 10 minutos.
>
> Esta guía es más detallada y cubre escenarios adicionales.

## 📋 Requisitos Previos

- **2 cuentas Gmail** (puedes crear cuentas nuevas si es necesario)
- Ejemplo:
  - `cuenta1@gmail.com` - Para recibir confirmaciones y OC (actúa como servidor)
  - `cuenta2@gmail.com` - Para enviar correos (actúa como Kontrol Travel)

---

## 🔐 Paso 1: Configurar Acceso a Gmail

Gmail requiere configuración especial para permitir acceso IMAP/SMTP desde aplicaciones.

### Opción A: Contraseña de Aplicación (RECOMENDADO)

**Para CADA cuenta Gmail:**

1. Ve a tu cuenta Google: https://myaccount.google.com/
2. Click en **Seguridad** (menú izquierdo)
3. Habilita **Verificación en 2 pasos** si no está activada:
   - Click en "Verificación en 2 pasos"
   - Sigue los pasos (necesitarás tu teléfono)
4. Una vez habilitada la verificación en 2 pasos:
   - Regresa a **Seguridad**
   - Busca **Contraseñas de aplicaciones** (al final de la sección)
   - Click en "Contraseñas de aplicaciones"
5. Genera una contraseña:
   - En "Selecciona la app": Elige "Correo"
   - En "Selecciona el dispositivo": Elige "Otro (nombre personalizado)"
   - Escribe: "Sistema OC"
   - Click en **Generar**
6. **GUARDA la contraseña de 16 caracteres** (aparece con espacios, ejemplo: `abcd efgh ijkl mnop`)
7. Esta contraseña la usarás en el `.env` en lugar de tu contraseña normal

### Opción B: Acceso de Apps Menos Seguras (NO RECOMENDADO)

⚠️ Google está eliminando esta opción gradualmente.

1. Ve a: https://myaccount.google.com/lesssecureapps
2. Activa "Permitir el acceso de aplicaciones menos seguras"

---

## ⚙️ Paso 2: Configurar el Sistema

### 1. Editar archivo `.env`

```bash
cd /Users/cucho/Library/CloudStorage/OneDrive-Personal/DESARROLLOS/agente-travelIA/envia2
nano .env
```

### 2. Configuración para 2 cuentas Gmail

**Escenario: Usar UNA sola cuenta para todo (más simple)**

```bash
# ==================== CONFIGURACIÓN GENERAL ====================
APP_NAME="Sistema de Seguimiento OC - Prueba Local"
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# ==================== BASE DE DATOS ====================
# Nueva ubicación v1.3.0: data/oc_seguimiento.db
DATABASE_URL=sqlite:///./data/oc_seguimiento.db

# ==================== CORREO DE MONITOREO (IMAP) ====================
# Cuenta Gmail #1 - Donde llegarán las confirmaciones con PDF
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=cuenta1@gmail.com
IMAP_PASSWORD=abcd efgh ijkl mnop    # ← Tu contraseña de aplicación (sin espacios)
IMAP_MAILBOX=INBOX
IMAP_USE_SSL=True
IMAP_CHECK_INTERVAL=60   # Verificar cada 60 segundos

# ==================== CORREO DE ENVÍO (SMTP) ====================
# Cuenta Gmail #2 - Desde donde se enviarán las solicitudes
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=cuenta2@gmail.com
SMTP_PASSWORD=wxyz abcd efgh ijkl    # ← Tu contraseña de aplicación (sin espacios)
SMTP_FROM_EMAIL=cuenta2@gmail.com
SMTP_FROM_NAME=Sistema de Prueba OC
SMTP_USE_TLS=True

# ==================== CORREO DE RECEPCIÓN DE OC ====================
# Misma cuenta Gmail #1 - Donde los clientes enviarán las OC
OC_INBOX_HOST=imap.gmail.com
OC_INBOX_PORT=993
OC_INBOX_USERNAME=cuenta1@gmail.com
OC_INBOX_PASSWORD=abcd efgh ijkl mnop    # ← Misma contraseña
OC_INBOX_MAILBOX=INBOX
OC_INBOX_USE_SSL=True
OC_CHECK_INTERVAL=60

# ==================== SCHEDULER ====================
SCHEDULER_CHECK_HOUR=9
SCHEDULER_CHECK_MINUTE=0
SCHEDULER_CHECKS_PER_DAY=24   # Verificar cada hora en pruebas

# ==================== INTERFAZ WEB ====================
WEB_HOST=0.0.0.0
WEB_PORT=8001
WEB_RELOAD=True

# ==================== CONFIGURACIÓN DE CORREOS ====================
# Quién recibe copia de todos los correos
EMAIL_CC_RECIPIENTS=cuenta1@gmail.com

# Días para recordatorios (reducidos para pruebas rápidas)
DAYS_FOR_REMINDER_1=0   # Enviar recordatorio inmediatamente (para pruebas)
DAYS_FOR_REMINDER_2=0   # Enviar ultimátum inmediatamente (para pruebas)

# ==================== CLIENTES QUE REQUIEREN OC ====================
# El nombre debe coincidir EXACTAMENTE con lo que aparece en el PDF
AGENCIES_REQUIRING_OC=WALVIS S.A.,MI EMPRESA DE PRUEBA
```

**IMPORTANTE:**
- Reemplaza `cuenta1@gmail.com` y `cuenta2@gmail.com` con tus cuentas reales
- Reemplaza las contraseñas con tus contraseñas de aplicación (sin espacios)
- Las contraseñas de aplicación se ven así: `abcdefghijklmnop` (16 caracteres seguidos)

---

## 🧪 Paso 3: Probar el Sistema Paso a Paso

### Test 1: Verificar Instalación

```bash
source venv/bin/activate
python verify_install.py
```

Deberías ver:
```
✅ Todos los módulos están instalados
🎉 Sistema listo para usar!
```

### Test 2: Probar Extracción de PDF

```bash
python tests/test_pdf.py "data/reservas_prueba/resumen del servicio.pdf"
```

Deberías ver:
```
✅ Datos extraídos exitosamente:
  ID de Reserva: 45215412
  Agencia: WALVIS S.A.
  ...
```

### Test 3: Probar Configuración

```bash
python config.py
```

Deberías ver:
```
=== Configuración del Sistema ===
Aplicación: Sistema de Seguimiento OC - Prueba Local
✅ Configuración válida
```

### Test 4: Inicializar Base de Datos

```bash
python database.py
```

Deberías ver:
```
=== Inicializando Base de Datos ===
✅ Base de datos creada: sqlite:///./oc_seguimiento.db
✅ Clientes configurados: WALVIS S.A., MI EMPRESA DE PRUEBA
```

---

## 🚀 Paso 4: Ejecutar el Sistema Completo

### 1. Iniciar el sistema

```bash
python app.py
```

Deberías ver:
```
🚀 Iniciando Sistema de Seguimiento de OC...
✅ Configuración validada
✅ Base de datos inicializada
✅ Scheduler iniciado
✅ Monitores de correo iniciados
🎉 Sistema iniciado correctamente en development mode
```

### 2. Abrir Dashboard

Abre tu navegador en: **http://localhost:8001**

---

## 📧 Paso 5: Simular el Flujo Completo

### Escenario 1: Enviar Confirmación de Reserva (Manual)

**Desde tu cuenta personal:**

1. Abre Gmail
2. **Compón un correo nuevo**
3. **Para:** `cuenta1@gmail.com` (la cuenta de monitoreo)
4. **Asunto:** `Confirmación de Reserva Hotel - ID 45215412`
5. **Adjunta:** El archivo `resumen del servicio.pdf`
6. **Envía el correo**

**¿Qué debería pasar?**

El sistema:
1. ✅ Detectará el correo en 60 segundos (máximo)
2. ✅ Extraerá los datos del PDF
3. ✅ Verificará que "WALVIS S.A." requiere OC
4. ✅ Creará la reserva en la base de datos
5. ✅ Enviará automáticamente la solicitud inicial a `cuenta2@gmail.com`

**Ver en el Dashboard:**
- Refrescar http://localhost:8001
- Deberías ver la reserva en "Reservas Pendientes de OC"

**Ver en logs:**
```bash
tail -f logs/oc_seguimiento_*.log
```

### Escenario 2: Simular Envío de OC

**Desde tu cuenta personal (simular cliente):**

1. Abre Gmail
2. **Compón un correo nuevo**
3. **Para:** `cuenta1@gmail.com` (donde se reciben las OC)
4. **Asunto:** `OC para Reserva ID 45215412 - LOC AAFTTAT`
5. **Adjunta:** Un PDF cualquiera (puede ser el mismo PDF de reserva)
6. **Envía el correo**

**¿Qué debería pasar?**

El sistema:
1. ✅ Detectará el correo con adjunto PDF
2. ✅ Buscará la reserva por ID o LOC en el asunto
3. ✅ Marcará la OC como RECIBIDA
4. ✅ Detendrá el envío de recordatorios

**Ver en el Dashboard:**
- La reserva ahora aparece en "OC Recibidas Recientemente"
- El estado cambió a "Recibida"

---

## 🔧 Paso 6: Pruebas Avanzadas

### A. Forzar Procesamiento Inmediato

En el Dashboard, click en el botón:
```
🔄 Procesar Correos Ahora
```

### B. Probar API REST

```bash
# Ver estadísticas
curl http://localhost:8001/api/stats

# Listar reservas
curl http://localhost:8001/api/reservas

# Ver reservas pendientes
curl http://localhost:8001/api/reservas?estado=pendiente

# Ver detalles de reserva
curl http://localhost:8001/api/reservas/1
```

### C. Marcar OC Manualmente

```bash
curl -X POST http://localhost:8001/api/reservas/1/marcar-oc-recibida \
  -H "Content-Type: application/json" \
  -d '{"numero_oc": "OC-12345"}'
```

### D. Reenviar Correo Manualmente

```bash
curl -X POST "http://localhost:8001/api/reservas/1/reenviar-correo?tipo_correo=solicitud_inicial"
```

---

## 📊 Paso 7: Verificar Resultados

### En Gmail (cuenta1@gmail.com)

Deberías ver correos recibidos:
1. ✅ Tu correo manual con el PDF adjunto
2. ✅ Solicitud de OC (enviada automáticamente por el sistema)

### En Gmail (cuenta2@gmail.com)

Deberías ver:
1. ✅ Correo enviado: "Solicitud de Orden de Compra - Reserva 45215412"

### En el Dashboard

1. ✅ Estadísticas actualizadas
2. ✅ Reserva visible con su estado
3. ✅ Historial de correos enviados

### En la Base de Datos

```bash
sqlite3 oc_seguimiento.db
```

```sql
-- Ver todas las reservas
SELECT id_reserva, agencia, estado_oc FROM reservas;

-- Ver correos enviados
SELECT tipo_correo, estado, fecha_enviado FROM correos_enviados;

-- Ver OC recibidas
SELECT numero_oc, fecha_creacion FROM ordenes_compra;
```

---

## 🐛 Solución de Problemas

### Problema 1: "No se detectan correos nuevos"

**Verificar:**
```bash
# Probar conexión IMAP manualmente
python -c "
from email_monitor import ReservaMonitor
m = ReservaMonitor()
print('✅ Conectado' if m.connect() else '❌ Error')
m.disconnect()
"
```

**Soluciones:**
- Verifica que la contraseña de aplicación sea correcta
- Verifica que IMAP esté habilitado en Gmail
- Revisa los logs: `tail -f logs/oc_seguimiento_*.log`

### Problema 2: "No se envían correos"

**Verificar:**
```bash
# Probar envío SMTP manualmente
python -c "
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('Test')
msg['Subject'] = 'Test'
msg['From'] = 'cuenta2@gmail.com'
msg['To'] = 'cuenta1@gmail.com'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('cuenta2@gmail.com', 'tu_password_app')
server.send_message(msg)
server.quit()
print('✅ Correo enviado')
"
```

**Soluciones:**
- Verifica credenciales SMTP
- Verifica que el puerto sea 587
- Revisa que `SMTP_USE_TLS=True`

### Problema 3: "No se extrae información del PDF"

**Verificar:**
```bash
python tests/test_pdf.py "data/reservas_prueba/resumen del servicio.pdf"
```

**Si falla:**
- Verifica que el PDF no esté corrupto
- Verifica que pdfplumber esté instalado: `pip install pdfplumber`

### Problema 4: "Errores de autenticación Gmail"

**Gmail bloqueó el acceso:**
1. Ve a: https://myaccount.google.com/notifications
2. Busca notificaciones de "Intento de inicio de sesión bloqueado"
3. Click en "Sí, fui yo"
4. O genera una nueva contraseña de aplicación

---

## 📝 Tips para Pruebas

### 1. Acortar Tiempos para Pruebas Rápidas

En `.env`:
```bash
DAYS_FOR_REMINDER_1=0  # Recordatorio inmediato
DAYS_FOR_REMINDER_2=0  # Ultimátum inmediato
IMAP_CHECK_INTERVAL=30  # Verificar cada 30 segundos
```

### 2. Ver Logs en Tiempo Real

```bash
tail -f logs/oc_seguimiento_*.log | grep -E "✅|❌|📧|📎"
```

### 3. Resetear la Base de Datos

```bash
rm oc_seguimiento.db
python database.py
```

### 4. Enviar Correos de Prueba con Diferentes Agencias

Edita el PDF o crea nuevos con diferentes nombres de agencia para probar:
- Agencias que requieren OC (aparecen en `AGENCIES_REQUIRING_OC`)
- Agencias que NO requieren OC (no envía correos)

---

## ✅ Checklist de Pruebas Completas

- [ ] Instalación verificada
- [ ] Configuración de Gmail completada (2 cuentas)
- [ ] Contraseñas de aplicación generadas
- [ ] Archivo .env configurado
- [ ] Sistema inicia sin errores
- [ ] Dashboard accesible en http://localhost:8001
- [ ] PDF se extrae correctamente
- [ ] Correo con PDF es detectado por IMAP
- [ ] Reserva se crea en base de datos
- [ ] Solicitud inicial se envía automáticamente
- [ ] Correo de OC es detectado
- [ ] OC se marca como recibida
- [ ] Recordatorios se detienen
- [ ] API REST funciona
- [ ] Logs se generan correctamente

---

## 🆕 Novedades v1.3.0

El proyecto ha sido reorganizado con una estructura profesional:

### Sistema de Gestión Integrado

```bash
# Gestionar el sistema fácilmente
./scripts/gestion/gestionar_sistema.sh start     # Iniciar sistema
./scripts/gestion/gestionar_sistema.sh stop      # Detener sistema
./scripts/gestion/gestionar_sistema.sh status    # Ver estado
./scripts/gestion/gestionar_sistema.sh logs      # Ver logs en tiempo real
./scripts/gestion/gestionar_sistema.sh restart   # Reiniciar sistema
```

### Scripts Organizados por Categoría

```bash
# Base de Datos
python scripts/database/crear_bd.py              # Crear BD
python scripts/database/limpiar_base_datos.py    # Limpiar datos
python scripts/database/cargar_clientes_excel.py # Cargar clientes

# Testing y Verificación
python scripts/testing/check_inbox.py            # Verificar correos
python scripts/testing/generar_pdf_prueba.py     # Generar PDFs
python scripts/testing/verificar_correos.py      # Verificar config

# Utilidades
python scripts/utils/test_conexion.py            # Test IMAP/SMTP
python scripts/utils/enviar_prueba.py            # Enviar pruebas
python scripts/utils/configurar_cliente.py       # Configuración
```

### Nuevas Vistas Web

- **Vista de Reservas**: http://localhost:8001/reservas
  - Todas las reservas con filtros y búsqueda
  - Estadísticas en tiempo real

- **Gestión de Clientes**: http://localhost:8001/clientes
  - 79 clientes configurados desde Excel
  - Filtros por requiere/no requiere OC

### Estructura Actualizada

- Base de datos ahora en: `data/oc_seguimiento.db`
- PDFs de prueba en: `data/reservas_prueba/`
- Scripts organizados en: `scripts/gestion/`, `database/`, `testing/`, `utils/`
- Documentación categorizada en: `docs/`

### Más Información

- **Estructura completa**: `ESTRUCTURA_PROYECTO.md`
- **Guía de scripts**: `scripts/README.md`
- **Índice de docs**: `docs/README.md`
- **Changelog**: `CHANGELOG.md`

---

## 🎯 Próximos Pasos

Una vez que todo funcione localmente:

1. **Configurar con correos reales** de Kontrol Travel
2. **Agregar más clientes** a `AGENCIES_REQUIRING_OC`
3. **Ajustar tiempos** de recordatorios (día 2, día 4)
4. **Desplegar en producción** (GCP, VPS, etc.)

---

¿Necesitas ayuda con algún paso específico? 🚀

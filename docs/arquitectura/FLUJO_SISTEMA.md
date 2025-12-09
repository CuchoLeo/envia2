# 🔄 Flujo del Sistema de Seguimiento de OC

**Sistema:** Seguimiento Automático de Órdenes de Compra
**Empresa:** Kontrol Travel

---

## 📋 Resumen Ejecutivo

El sistema automatiza el seguimiento de Órdenes de Compra (OC) requeridas por ciertas agencias antes de prestar servicios. Usa **1 sola cuenta Gmail** que gestiona todo el ciclo.

---

## 🎯 Componentes del Sistema

### 1. **Sistemas Principales** (Externos)
- **Emails:**
  - `kontroltravel@ideasfractal.com` (Principal)
  - `v.rodriguezy@gmail.com` (Secundario)
- **Función:** Generan y envían confirmaciones de reserva
- **Acción:** Envían PDF de confirmación al cliente Y a seguimientoocx@gmail.com

### 2. **Sistema de Seguimiento OC** (Este sistema)
- **Email:** `seguimientoocx@gmail.com`
- **Función:** Gestiona TODO el ciclo de OC
- **Acciones:**
  - Recibe confirmaciones
  - Detecta agencias que requieren OC
  - Solicita OC a las agencias
  - Envía recordatorios automáticos
  - Recibe y registra OC
  - Confirma recepción

### 3. **Agencias** (Externas)
- **Emails:** Configurados en BD por agencia
- **Función:** Responden con OC en PDF
- **Acción:** Envían OC como respuesta a solicitud

---

## 🔄 Flujo Completo Paso a Paso

### **Fase 1: Generación de Reserva**

```
┌─────────────────────────────────────┐
│ Sistemas Principales                │
│ - kontroltravel@ideasfractal.com    │
│ - v.rodriguezy@gmail.com            │
└────────────┬────────────────────────┘
             │
             │ Genera confirmación
             │ con PDF
             │
             ├─────────────────┐
             │                 │
             ▼                 ▼
    ┌────────────────┐  ┌──────────────────────┐
    │    Cliente     │  │ seguimientoocx       │
    │                │  │ @gmail.com           │
    │ (Agencia)      │  │                      │
    └────────────────┘  └──────────┬───────────┘
                                   │
                                   │ Sistema monitorea
                                   │ IMAP cada 5 min
                                   │ Solo remitentes autorizados
                                   ▼
```

---

### **Fase 2: Detección y Procesamiento**

```
┌──────────────────────────────────────┐
│ Sistema de Seguimiento OC            │
│                                      │
│ 1. Detecta nuevo email               │
│    └─> Con asunto: "Confirmación"   │
│    └─> Con adjunto: PDF             │
│                                      │
│ 2. Extrae datos del PDF              │
│    ├─> ID Reserva                   │
│    ├─> Nombre Agencia               │
│    ├─> Hotel                        │
│    ├─> Fechas                       │
│    └─> Monto                        │
│                                      │
│ 3. Busca en BD                       │
│    └─> ¿Agencia requiere OC?        │
│        ├─> SÍ: Crea reserva         │
│        │   Estado: PENDIENTE         │
│        └─> NO: Solo registra        │
│            Estado: NO_REQUIERE       │
└──────────────────────────────────────┘
```

---

### **Fase 3: Solicitud de OC** (Solo si requiere)

```
┌──────────────────────────────────────┐
│ Sistema de Seguimiento OC            │
│ seguimientoocx@gmail.com             │
└────────────┬─────────────────────────┘
             │
             │ Envía email con:
             │ - Datos de la reserva
             │ - PDF adjunto
             │ - Solicitud de OC
             │
             ▼
    ┌─────────────────────┐
    │ Agencia             │
    │ contacto@agencia.cl │
    │                     │
    │ CC: Admin, Finanzas │
    └─────────────────────┘

    Estado BD: PENDIENTE → SOLICITADA
    Fecha envío: Registrada
```

**Email enviado contiene:**
```
Para: contacto@agencia.cl
CC: administracion@kontroltravel.com, finanzas@kontroltravel.com
Asunto: Solicitud de Orden de Compra - Reserva #123456

Estimados,

Adjunto confirmación de reserva para hotel...

Por favor enviar Orden de Compra para proceder.

Datos de la reserva:
- ID: 123456
- Hotel: Hotel XYZ
- Fecha entrada: 2025-12-01
- Monto: $150,000

Adjunto: confirmacion_123456.pdf
```

---

### **Fase 4: Recordatorios Automáticos**

```
┌──────────────────────────────────────┐
│ Scheduler (APScheduler)              │
│ Revisa cada 6 horas                  │
└────────────┬─────────────────────────┘
             │
             │ Busca reservas con:
             │ - Estado: SOLICITADA
             │ - Sin OC recibida
             │ - Días transcurridos
             │
             ├─── Día 2 ──> Recordatorio 1 (Amable)
             │
             ├─── Día 4 ──> Recordatorio 2 (Firme)
             │
             └─── Día 6 ──> Ultimátum (Urgente)

Estado BD: SOLICITADA → RECORDATORIO_1/2/3
Contador de recordatorios: Incrementa
```

**Ejemplo Recordatorio 1:**
```
Para: contacto@agencia.cl
Asunto: Recordatorio: Orden de Compra Pendiente - Reserva #123456

Estimados,

Hace 2 días solicitamos la OC para la reserva #123456.

¿Podrían confirmar el estado?

Quedamos atentos.
```

**Ejemplo Recordatorio 2 (más firme):**
```
Asunto: 2do Recordatorio: OC Urgente - Reserva #123456

Estimados,

Necesitamos la OC para proceder con la reserva.

Por favor enviar a la brevedad.
```

**Ejemplo Ultimátum:**
```
Asunto: URGENTE: OC Requerida - Reserva #123456

Estimados,

Llevamos 6 días esperando la OC.

Sin la OC no podemos garantizar la reserva.

Por favor responder con urgencia.
```

---

### **Fase 5: Recepción de OC**

```
    ┌─────────────────────┐
    │ Agencia             │
    │ contacto@agencia.cl │
    └────────────┬────────┘
                 │
                 │ Responde email con:
                 │ - Asunto: "Orden de Compra"
                 │ - Adjunto: oc_12345.pdf
                 │ - Mención: ID Reserva
                 │
                 ▼
    ┌──────────────────────────────────┐
    │ seguimientoocx@gmail.com         │
    │                                  │
    │ Sistema detecta (cada 5 min):    │
    │ 1. Email con "OC" en asunto      │
    │ 2. Tiene adjunto PDF             │
    │ 3. Menciona ID reserva           │
    │                                  │
    │ Acciones:                        │
    │ ├─> Descarga PDF                 │
    │ ├─> Guarda en data/oc/           │
    │ ├─> Registra en tabla OC         │
    │ └─> Actualiza estado reserva     │
    └──────────────────────────────────┘

Estado BD: RECORDATORIO_X → RECIBIDA
OC registrada con:
- archivo_nombre: oc_12345.pdf
- archivo_path: data/oc/20251120_123456_oc.pdf
- email_remitente: contacto@agencia.cl
- fecha_recepcion: 2025-11-20 14:30:00
```

---

### **Fase 6: Confirmación (Opcional)**

El sistema puede enviar confirmación de recepción (configurable):

```
┌──────────────────────────────────────┐
│ Sistema de Seguimiento OC            │
│ seguimientoocx@gmail.com             │
└────────────┬─────────────────────────┘
             │
             │ Email automático:
             │ "OC Recibida - Reserva #123456"
             │
             ▼
    ┌─────────────────────┐
    │ Agencia             │
    │ contacto@agencia.cl │
    │                     │
    │ CC: Admin           │
    └─────────────────────┘
```

---

## 📊 Diagrama de Estados

```
NUEVA RESERVA
     │
     │ ¿Requiere OC?
     │
     ├─NO──> NO_REQUIERE_OC (FIN)
     │
     └─SÍ──> PENDIENTE
               │
               │ Sistema envía solicitud
               ▼
           SOLICITADA
               │
               │ Scheduler revisa
               │
               ├─> Día 2 ──> RECORDATORIO_1
               │
               ├─> Día 4 ──> RECORDATORIO_2
               │
               ├─> Día 6+ ─> RECORDATORIO_3
               │
               │ Agencia responde
               ▼
           RECIBIDA (FIN ✅)
```

---

## 🔧 Configuración Técnica

### **Cuenta Gmail Única:**

```env
# IMAP - Recepción de confirmaciones Y OC
IMAP_HOST="imap.gmail.com"
IMAP_PORT=993
IMAP_USERNAME="seguimientoocx@gmail.com"
IMAP_PASSWORD="contraseña_aplicacion_aqui"

# SMTP - Envío de solicitudes y recordatorios
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USERNAME="seguimientoocx@gmail.com"
SMTP_PASSWORD="contraseña_aplicacion_aqui"

# OC Inbox (misma cuenta)
OC_INBOX_HOST="imap.gmail.com"
OC_INBOX_PORT=993
OC_INBOX_USERNAME="seguimientoocx@gmail.com"
OC_INBOX_PASSWORD="contraseña_aplicacion_aqui"

# Remitentes autorizados para enviar confirmaciones
ALLOWED_CONFIRMATION_SENDERS="kontroltravel@ideasfractal.com,v.rodriguezy@gmail.com"
```

---

## ⏱️ Ciclos del Sistema

### **1. Monitor de Confirmaciones (ReservaMonitor)**
- **Frecuencia:** Cada 5 minutos
- **Acción:** Busca emails de remitentes autorizados
- **Filtro:**
  - Asunto contiene: "confirmación" o "reserva"
  - Remitente autorizado: kontroltravel@ideasfractal.com o v.rodriguezy@gmail.com
  - Tiene adjunto PDF
- **Proceso:**
  1. Lee email
  2. Valida remitente autorizado
  3. Descarga PDF
  4. Extrae datos
  5. Crea reserva en BD
  6. Marca email como leído

### **2. Monitor de OC (OCMonitor)**
- **Frecuencia:** Cada 5 minutos
- **Acción:** Busca respuestas con OC
- **Filtro:**
  - Asunto contiene: "OC", "Orden de Compra", "orden compra"
  - Tiene adjunto PDF
  - Email de agencias conocidas
- **Proceso:**
  1. Lee email
  2. Extrae ID reserva del cuerpo/asunto
  3. Descarga PDF
  4. Registra OC en BD
  5. Actualiza estado a RECIBIDA
  6. Marca email como leído

### **3. Scheduler (Solicitudes y Recordatorios)**
- **Frecuencia:** Cada 6 horas (00:00, 06:00, 12:00, 18:00)
- **Acción:**
  1. Busca reservas PENDIENTES → Envía solicitud inicial
  2. Busca reservas SOLICITADAS sin OC:
     - Día 2: Envía recordatorio 1
     - Día 4: Envía recordatorio 2
     - Día 6+: Envía ultimátum

---

## 📁 Estructura de Archivos

```
data/
├── oc_seguimiento.db          # Base de datos SQLite
├── confirmaciones/            # PDFs de confirmaciones recibidas
│   ├── 20251120_123456.pdf
│   └── 20251120_123457.pdf
└── oc/                        # PDFs de OC recibidas
    ├── 20251120_123456_oc.pdf
    └── 20251121_123457_oc.pdf
```

---

## 🎯 Casos de Uso

### **Caso 1: Flujo Normal (Todo OK)**
```
1. [09:00] Sistema recibe confirmación → Crea reserva PENDIENTE
2. [09:05] Scheduler envía solicitud → Estado: SOLICITADA
3. [10:30] Agencia responde con OC → Estado: RECIBIDA
   ✅ FIN (24 horas)
```

### **Caso 2: Con Recordatorios**
```
1. [Lun 09:00] Sistema recibe confirmación → PENDIENTE
2. [Lun 09:05] Scheduler envía solicitud → SOLICITADA
3. [Mié 09:00] Sin respuesta → Envía recordatorio 1
4. [Vie 09:00] Sin respuesta → Envía recordatorio 2
5. [Vie 15:30] Agencia responde con OC → RECIBIDA
   ✅ FIN (5 días)
```

### **Caso 3: Sin OC (Manual)**
```
1. [Lun 09:00] Sistema recibe confirmación → PENDIENTE
2. [Lun 09:05] Scheduler envía solicitud → SOLICITADA
3. [Mié 09:00] Recordatorio 1
4. [Vie 09:00] Recordatorio 2
5. [Dom 09:00] Ultimátum
6. [Lun] Sin respuesta
   ⚠️ Estado: RECORDATORIO_3 (requiere intervención manual)
```

---

## 🔐 Seguridad

### **Información Sensible:**
- Contraseñas de aplicación Gmail
- PDFs con datos de clientes
- Emails de agencias
- Base de datos con reservas

### **Protección:**
- ✅ Contraseñas en .env (no en código)
- ✅ .env en .gitignore
- ✅ PDFs en data/ (no en Git)
- ✅ Base de datos en data/ (no en Git)
- ✅ Logs sin información sensible
- ✅ Conexiones IMAP/SMTP con SSL/TLS

---

## 📞 Contactos del Flujo

```
Sistemas Principales (Remitentes Autorizados):
- Email 1: kontroltravel@ideasfractal.com
- Email 2: v.rodriguezy@gmail.com
- Función: Envían confirmaciones

Sistema de OC:
- Email: seguimientoocx@gmail.com
- Función: Gestiona ciclo completo de OC

Administración:
- Email: [configurar en .env]
- Recibe: Copias de todas las solicitudes

Finanzas/Contabilidad:
- Email: [configurar en .env]
- Recibe: Copias de todas las solicitudes
```

---

## ✅ Resumen

**1 sola cuenta Gmail gestiona TODO el flujo:**

```
seguimientoocx@gmail.com
├── RECIBE confirmaciones de:
│   ├── kontroltravel@ideasfractal.com
│   └── v.rodriguezy@gmail.com
├── ENVÍA solicitudes a agencias
├── ENVÍA recordatorios automáticos
└── RECIBE OC de agencias
```

**Flujo en 6 fases:**
1. ➡️ Generación (Sistema Principal)
2. 🔍 Detección (Sistema OC)
3. 📤 Solicitud (Sistema OC → Agencia)
4. ⏰ Recordatorios (Automáticos)
5. 📥 Recepción (Agencia → Sistema OC)
6. ✅ Confirmación (Opcional)

**Estados posibles:**
- NO_REQUIERE_OC
- PENDIENTE
- SOLICITADA
- RECORDATORIO_1 / 2 / 3
- RECIBIDA ✅

---

**Sistema 100% Automático** 🚀

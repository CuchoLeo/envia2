# Sistema de Seguimiento de Órdenes de Compra (OC) 📋

Sistema automatizado para gestionar el seguimiento de órdenes de compra en reservas hoteleras corporativas.

**Versión**: 1.3.4 | **Estado**: Producción | **Cliente**: Kontrol Travel | **Última Actualización**: 9 de Diciembre de 2024

📄 **[Ver Alcance Completo del Proyecto →](./ALCANCE_PROYECTO.md)**

⚠️ **NUEVO en v1.3.4**: El flujo de seguimiento ahora se calcula desde la **Fecha de Emisión del PDF** en lugar de la fecha de llegada del correo. **[Ver Detalles →](./docs/CHANGELOG_FECHA_EMISION.md)**

⚠️ **NUEVO en v1.3.3**: Sistema de emails configurado por cliente. **[Ver Próximos Pasos →](./PROXIMOS_PASOS_EMAILS.md)**

## 📖 Descripción

Este sistema independiente monitorea automáticamente los correos de confirmación de reservas, identifica clientes corporativos que requieren orden de compra formal, y gestiona un flujo escalonado de comunicaciones para solicitar y hacer seguimiento a estas órdenes.

**Objetivo**: Automatizar el 100% del proceso de solicitud y recepción de OC, eliminando intervención manual y asegurando cumplimiento documental.

### Flujo de Comunicaciones

- **Día 0**: Solicitud inicial de OC (inmediatamente después de detectar la reserva)
- **Día 2**: Recordatorio amable si no se ha recibido la OC
- **Día 4**: Ultimátum indicando suspensión al día hábil siguiente
- **Automático**: Detección de OC recibida y detención del flujo

## ✨ Características Principales

### 🔄 Monitoreo Automático
- Monitoreo continuo de casillas IMAP para nuevas reservas
- **Extracción automática mejorada** de datos de PDFs adjuntos
  - **13+ formatos de monto soportados**: Total, Monto Total, Total a Pagar, Precio Total, etc.
  - Detección flexible con múltiples patrones y fallback automático
  - Logs informativos del patrón que detectó cada campo
- Detección de órdenes de compra recibidas por correo
- Patrones flexibles de detección:
  - "Reserva CODIGO" - ej: "Orden de Compra - Reserva AAFVDUA"
  - "LOC CODIGO" - ej: "OC para LOC TEST2024002"
  - "Orden de Compra CODIGO" - ej: "orden de compra AAFWHWS"
  - "OC CODIGO" - ej: "OC AAFWHWS"
  - Búsqueda case-insensitive y flexible

### 📧 Gestión de Comunicaciones
- Tres niveles de correos con plantillas HTML profesionales
- Envío programado según días transcurridos
- Reintentos automáticos en caso de fallos
- Copia a administración en todos los envíos

### 💾 Base de Datos y Seguimiento
- Registro completo de reservas y su estado
- Historial de correos enviados
- Órdenes de compra recibidas y validadas
- Configuración flexible por cliente

### 🎯 Interfaz Web de Administración
- **Dashboard principal** con estadísticas en tiempo real
- **Vista de Reservas** (`/reservas`) - Gestión completa con filtros y búsqueda
  - Filtros por estado (Pendientes, Recibidas, Todas)
  - Búsqueda en tiempo real por ID, agencia, hotel
  - Estadísticas dinámicas
- **Vista de Clientes** (`/clientes`) - Configuración de clientes
  - **78 clientes configurados** en base de datos
  - Filtros por requiere/no requiere OC
  - Estadísticas completas (40 requieren OC, 38 no requieren)
  - **Sistema de emails configurables** por cliente (v1.3.3)
- Acciones manuales (marcar OC recibida, reenviar correos)
- **API REST completa** documentada

## 🏗️ Arquitectura del Sistema

📊 **Ver documentación de diagramas completa:**
- **[FLUJO_DETALLADO_SISTEMA.md](./docs/FLUJO_DETALLADO_SISTEMA.md)** - Diagramas detallados de flujos y configuraciones (v1.3.3)
- **[DIAGRAMAS.md](./DIAGRAMAS.md)** - Diagramas de arquitectura general

```
┌─────────────────────────────────────────────────────────┐
│                    Sistema de Seguimiento OC            │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Email Monitor│    │   Scheduler  │    │  Web Admin   │
│   (IMAP)     │    │  (APScheduler)│    │  (FastAPI)   │
└──────┬───────┘    └──────┬───────┘    └──────────────┘
       │                   │
       ▼                   ▼
┌──────────────┐    ┌──────────────┐
│ PDF Processor│    │ Email Sender │
│  (pdfplumber)│    │    (SMTP)    │
└──────┬───────┘    └──────┬───────┘
       │                   │
       └─────────┬─────────┘
                 ▼
         ┌──────────────┐
         │   Database   │
         │   (SQLite)   │
         └──────────────┘
```

## 📋 Requisitos Previos

- **Python 3.10+**
- **Acceso a servidor IMAP/SMTP** (Gmail, Outlook, hosting propio)
- **Servidor donde ejecutar** (local, VPS, o GCP)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd envia2
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar el archivo de ejemplo y editarlo con tus credenciales:

```bash
cp .env.example .env
nano .env  # o usar tu editor preferido
```

**Configuración mínima requerida:**

```bash
# Correo de monitoreo (donde llegan las confirmaciones)
IMAP_HOST=imap.gmail.com
IMAP_USERNAME=seguimiento-oc@ideasfractal.com
IMAP_PASSWORD=tu_password_aqui

# Correo de envío (desde donde se envían las solicitudes)
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=kontroltravel@ideasfractal.com
SMTP_PASSWORD=tu_password_aqui
SMTP_FROM_EMAIL=kontroltravel@ideasfractal.com

# Correo de recepción de OC
OC_INBOX_HOST=imap.gmail.com
OC_INBOX_USERNAME=oc-recibidas@ideasfractal.com
OC_INBOX_PASSWORD=tu_password_aqui

# Clientes que requieren OC (separados por coma)
AGENCIES_REQUIRING_OC=WALVIS S.A.,EMPRESA CORPORATIVA LTDA
```

### 5. Crear directorios necesarios

```bash
mkdir -p logs static
```

### 6. Inicializar base de datos

```bash
python database.py
```

## 🎮 Uso

### Iniciar el Sistema

```bash
python app.py
```

El sistema iniciará:
- ✅ Servidor web en `http://localhost:8001`
- ✅ Monitores de correo (IMAP)
- ✅ Scheduler de envíos automáticos
- ✅ API REST

### Acceder al Dashboard

Abre tu navegador en: **http://localhost:8001**

Verás:
- Estadísticas en tiempo real
- Reservas pendientes de OC
- OC recibidas recientemente
- Acceso a la API REST

### Usar la API REST

#### Endpoints principales:

```bash
# Verificar estado del sistema
curl http://localhost:8001/api/health

# Obtener estadísticas
curl http://localhost:8001/api/stats

# Listar reservas
curl http://localhost:8001/api/reservas

# Listar solo pendientes
curl http://localhost:8001/api/reservas?estado=pendiente

# Obtener detalles de una reserva
curl http://localhost:8001/api/reservas/1

# Marcar OC como recibida manualmente
curl -X POST http://localhost:8001/api/reservas/1/marcar-oc-recibida \
  -H "Content-Type: application/json" \
  -d '{"numero_oc": "OC-12345"}'

# Reenviar correo manualmente
curl -X POST "http://localhost:8001/api/reservas/1/reenviar-correo?tipo_correo=solicitud_inicial"

# Forzar procesamiento inmediato
curl -X POST http://localhost:8001/api/process-now
```

Documentación completa de la API: **http://localhost:8001/docs**

📮 **¿Primera vez usando APIs?** Ver la **[Guía de Postman para Principiantes](./docs/GUIA_POSTMAN_BASICA.md)**

## 📁 Estructura del Proyecto

```
envia2/
├── README.md                   # Esta documentación
├── CHANGELOG.md                # Historial de cambios (v1.3.3)
├── PROXIMOS_PASOS_EMAILS.md    # 📧 Estado y próximos pasos emails (v1.3.3)
├── requirements.txt            # Dependencias Python
├── .env                        # Configuración (no en Git)
├── .env.example                # Ejemplo de configuración
│
├── app.py                      # 🚀 Aplicación principal FastAPI
├── config.py                   # ⚙️ Configuración central
├── database.py                 # 💾 Modelos SQLAlchemy
│
├── src/                        # 📦 Código fuente principal
│   ├── email_monitor.py        # Monitoreo de emails (IMAP)
│   ├── email_sender.py         # Envío de emails (SMTP)
│   ├── imap_wrapper.py         # Wrapper de conexión IMAP
│   ├── pdf_processor.py        # Extracción de datos de PDF
│   └── scheduler.py            # Tareas programadas (APScheduler)
│
├── templates/                  # 🎨 Plantillas HTML (Jinja2)
│   ├── dashboard.html          # Dashboard principal
│   ├── reservas.html           # Vista de todas las reservas
│   ├── clientes.html           # Gestión de clientes
│   ├── solicitud_inicial.html  # Template email día 0
│   ├── recordatorio_dia2.html  # Template email día 2
│   └── ultimatum_dia4.html     # Template email día 4
│
├── scripts/                    # 🔧 Scripts utilitarios
│   ├── README.md               # Documentación de scripts
│   ├── gestion/                # Gestión del sistema
│   │   ├── gestionar_sistema.sh    # Script principal (start/stop/status)
│   │   ├── detener_sistema.py      # Detener sistema (Python)
│   │   └── detener_sistema.sh      # Detener sistema (Bash)
│   ├── database/               # Scripts de base de datos
│   │   ├── crear_bd.py             # Crear/inicializar BD
│   │   ├── limpiar_base_datos.py   # Limpiar datos de prueba
│   │   └── cargar_clientes_excel.py # Importar clientes desde Excel
│   ├── testing/                # Scripts de prueba
│   │   ├── check_inbox.py          # Verificar emails en inbox
│   │   ├── generar_pdf_prueba.py   # Generar PDFs de prueba
│   │   ├── marcar_correos_no_leidos.py
│   │   ├── verificar_correos.py
│   │   └── verificar_reservas.py
│   └── utils/                  # Utilidades generales
│       ├── configurar_cliente.py         # Configuración interactiva
│       ├── actualizar_emails_clientes.py # 📧 Actualizar emails de contacto (v1.3.3)
│       ├── test_conexion.py              # Verificar conexiones IMAP/SMTP
│       ├── enviar_solicitud_oc.py        # Envío manual de solicitudes
│       └── verificar_emails.py           # Verificar emails recibidos
│
├── tests/                      # 🧪 Tests automatizados
│   ├── test_flujo_completo.py # Test end-to-end
│   └── test_pdf.py            # Test procesador PDF
│
├── docs/                       # 📚 Documentación completa
│   ├── README.md               # Índice de documentación
│   ├── ALCANCE_PROYECTO.md     # Alcance y objetivos
│   ├── DIAGRAMAS.md            # Diagramas del sistema
│   ├── SCRIPTS_GESTION.md      # Documentación de scripts
│   ├── LISTA_IMPLEMENTACION_CLIENTE.md  # Tareas de implementación
│   ├── CAMBIO_EMAIL_CONTACTO.md         # 📧 Documentación técnica emails (v1.3.3)
│   ├── GUIA_ACTUALIZACION_EMAILS.md     # 📧 Guía de actualización emails (v1.3.3)
│   ├── arquitectura/           # Arquitectura del sistema
│   │   ├── FLUJO_SISTEMA.md
│   │   ├── ANALISIS_MODELO_DATOS.md    # 📊 Análisis completo del modelo de datos
│   │   └── COMPARATIVA_ARQUITECTURAS_GCP.md
│   ├── configuracion/          # Guías de configuración
│   │   └── CONFIGURACION_GMAIL.md
│   ├── cliente/                # Docs para el cliente
│   │   ├── RESUMEN_PARA_CLIENTE.md
│   │   ├── PLAN_PRUEBAS_CLIENTE.md
│   │   └── SOLICITUD_INFO_CLIENTE.md
│   ├── inicio-rapido/          # Guías de inicio
│   │   ├── LEEME_PRIMERO.txt
│   │   ├── INICIO_RAPIDO.md
│   │   └── GUIA_PRUEBA_LOCAL.md
│   ├── git/
│   │   └── INSTRUCCIONES_GIT.md
│   └── troubleshooting/        # Solución de problemas
│       ├── TROUBLESHOOTING.md
│       ├── ERRORES_COMUNES.md
│       ├── SOLUCION_0_CORREOS.md
│       └── SOLUCION_PYTHON314.txt
│
├── data/                       # 💾 Datos del sistema
│   ├── oc_seguimiento.db       # Base de datos SQLite
│   ├── emails_clientes_template.csv  # 📧 Plantilla para actualizar emails (v1.3.3)
│   ├── clientes.xlsx           # Archivo de clientes
│   ├── reservas_prueba/        # PDFs de prueba
│   └── clientes_backup/        # Backup de configuraciones
│
├── logs/                       # 📋 Logs del sistema
├── static/                     # 🌐 Archivos estáticos web
│
└── deprecated/                 # 🗄️  Código antiguo (no usar)
    ├── README.md               # Info sobre archivos deprecados
    ├── integraciones/          # Integraciones obsoletas (API, n8n)
    ├── documentacion/          # Docs de sesiones antiguas
    ├── scripts_diagnostico/    # Scripts de diagnóstico antiguos
    └── tests_desarrollo/       # Tests de desarrollo

**Nota**: Ver `docs/README.md` para el índice completo de documentación.
**Nota**: Ver `scripts/README.md` para detalles de uso de los scripts.
```

## ⚙️ Configuración Avanzada

### Personalizar Días de Recordatorios

En `.env`:

```bash
DAYS_FOR_REMINDER_1=2    # Primer recordatorio
DAYS_FOR_REMINDER_2=4    # Ultimátum
```

### Configurar Verificaciones Periódicas

```bash
SCHEDULER_CHECKS_PER_DAY=4     # Verificar 4 veces al día
IMAP_CHECK_INTERVAL=300        # Verificar correos cada 5 minutos
```

### Agregar Destinatarios en Copia

```bash
EMAIL_CC_RECIPIENTS=admin@ideasfractal.com,finanzas@ideasfractal.com
```

### Configuración para Gmail

Si usas Gmail, necesitas:

1. **Habilitar "Acceso de apps menos seguras"** o
2. **Crear una contraseña de aplicación**:
   - Ve a tu cuenta de Google
   - Seguridad → Verificación en dos pasos
   - Contraseñas de aplicaciones
   - Genera una contraseña para "Correo"

## 🔒 Seguridad

### Recomendaciones:

1. **Nunca commitear el archivo `.env`** con credenciales reales
2. **Usar contraseñas de aplicación** en lugar de contraseñas principales
3. **Restringir acceso** al dashboard en producción
4. **Usar HTTPS** en producción (con certificado SSL)
5. **Revisar logs** regularmente para detectar anomalías

## 🐛 Solución de Problemas

### El sistema no detecta correos nuevos

1. Verificar credenciales IMAP en `.env`
2. Revisar logs en `logs/oc_seguimiento_*.log`
3. Probar conexión IMAP manualmente:

```bash
python -c "from email_monitor import ReservaMonitor; m = ReservaMonitor(); print('OK' if m.connect() else 'ERROR')"
```

### Los correos no se envían

1. Verificar credenciales SMTP en `.env`
2. Revisar que el puerto SMTP sea correcto (587 para TLS, 465 para SSL)
3. Verificar límites de envío de tu proveedor

### Error al extraer datos del PDF

1. Verificar que el PDF no esté corrupto
2. Probar el procesador manualmente:

```bash
python pdf_processor.py "resumen del servicio.pdf"
```

### Base de datos bloqueada (SQLite)

Si estás en producción con mucho tráfico, considera migrar a PostgreSQL:

```bash
# En .env
DATABASE_URL=postgresql://user:password@localhost:5432/oc_seguimiento
```

## 📊 Monitoreo y Logs

### Ubicación de logs

- **Logs del sistema**: `logs/oc_seguimiento_YYYY-MM-DD.log`
- **Rotación**: Diaria
- **Retención**: 30 días

### Niveles de log

```bash
# En .env, cambiar nivel de log:
LOG_LEVEL=INFO    # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Revisar logs en tiempo real

```bash
tail -f logs/oc_seguimiento_$(date +%Y-%m-%d).log
```

## 🚀 Despliegue en Producción

### Opción 1: Servidor Linux con systemd

Crear archivo de servicio `/etc/systemd/system/oc-seguimiento.service`:

```ini
[Unit]
Description=Sistema de Seguimiento OC
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/envia2
Environment="PATH=/path/to/envia2/venv/bin"
ExecStart=/path/to/envia2/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar:

```bash
sudo systemctl enable oc-seguimiento
sudo systemctl start oc-seguimiento
sudo systemctl status oc-seguimiento
```

### Opción 2: Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### Opción 3: Google Cloud Platform

Ver documentación detallada en el directorio `deployment/` del proyecto principal.

## 🧪 Testing y Utilidades

### Probar extracción de PDF

```bash
python pdf_processor.py "resumen del servicio.pdf"
```

### Probar conexión IMAP

```bash
python email_monitor.py
```

### Gestión de Base de Datos

```bash
# Modo interactivo - Menú completo
python limpiar_base_datos.py

# Ver estadísticas
python limpiar_base_datos.py --stats

# Listar todas las reservas
python limpiar_base_datos.py --list

# Eliminar reserva específica
python limpiar_base_datos.py --id TEST2024001

# Eliminar solo reservas de prueba (TEST*)
python limpiar_base_datos.py --test

# Eliminar TODAS las reservas (⚠️ cuidado)
python limpiar_base_datos.py --all
```

### Cargar Clientes desde Excel

```bash
# Cargar/actualizar clientes desde docs/clientes.xlsx
python cargar_clientes_excel.py
```

### Reprocesar Correos

```bash
# Marcar correos como no leídos para reprocesar
python marcar_correos_no_leidos.py

# Filtrar por remitente
python marcar_correos_no_leidos.py --sender "email@ejemplo.com"

# Filtrar por asunto
python marcar_correos_no_leidos.py --subject "confirmación"
```

### Probar configuración completa

```bash
python config.py
```

## 📈 Métricas y Rendimiento

### Capacidad

- **Reservas procesadas**: Ilimitadas (depende del hardware)
- **Correos por día**: Depende del proveedor SMTP
- **Latencia**: < 1 segundo para procesamiento de PDF
- **Base de datos**: SQLite soporta hasta ~100K reservas sin problemas

### Consumo de Recursos

- **RAM**: ~100-200 MB
- **CPU**: Mínimo (< 5% en promedio)
- **Disco**: ~10 MB + logs + base de datos

## 🤝 Soporte y Contribuciones

Para problemas o sugerencias:

1. Revisar esta documentación
2. Verificar logs del sistema
3. Ejecutar tests de diagnóstico

## 📦 Carpeta Deprecated

La carpeta `/deprecated/` contiene arquitecturas y código de versiones anteriores del sistema que ya no se utilizan. Incluye:

- **Integraciones obsoletas:** API REST pública, workflows de n8n
- **Documentación antigua:** Docs de sesiones de desarrollo anteriores
- **Scripts de diagnóstico:** Tools que fueron reemplazados por versiones mejoradas
- **Tests de desarrollo:** Tests básicos reemplazados por tests E2E

**⚠️ No usar estos archivos en producción.** Se mantienen solo como referencia histórica.

Ver `deprecated/README.md` para más detalles sobre qué contiene cada subcarpeta y por qué fue deprecado.

---

## 📄 Licencia

Propietario - Todos los derechos reservados

---

**Desarrollado para Kontrol Travel**
Sistema de gestión automatizada de órdenes de compra v1.1.1

# Estructura del Proyecto

Sistema de Seguimiento de Órdenes de Compra (OC) para Reservas Hoteleras

## 📁 Organización del Repositorio

```
envia2/
├── 📄 README.md                      # Documentación principal
├── 📄 ESTRUCTURA.md                  # Este archivo
├── requirements.txt                 # Dependencias Python
├── .env                             # Variables de entorno (no versionado)
├── .gitignore                       # Archivos ignorados por Git
│
├── 🚀 app.py                         # Aplicación FastAPI principal
├── ⚙️  config.py                      # Configuración del sistema
├── 🗄️  database.py                    # Modelos y conexión a BD
│
├── src/                             # 📦 Código fuente principal
│   ├── __init__.py
│   ├── email_monitor.py             # Monitor de correos IMAP
│   ├── email_sender.py              # Envío de correos SMTP
│   ├── imap_wrapper.py              # Cliente IMAP simplificado
│   ├── pdf_processor.py             # Procesamiento de PDFs
│   └── scheduler.py                 # Scheduler de tareas automáticas
│
├── tests/                           # 🧪 Tests y verificaciones
│   ├── __init__.py
│   ├── test_flujo_completo.py       # Test end-to-end
│   ├── test_imap.py                 # Test de conexión IMAP
│   ├── test_imap_simple.py          # Test IMAP simplificado
│   ├── test_pdf.py                  # Test de procesamiento PDF
│   ├── test_peek.py                 # Test de BODY.PEEK
│   └── verify_install.py            # Verificación de instalación
│
├── scripts/                         # 🛠️ Scripts de utilidad
│   ├── enviar_prueba.py             # Enviar emails de prueba
│   ├── diagnose_imap.py             # Diagnóstico de IMAP
│   ├── marcar_no_leido.py           # Marcar emails como no leídos
│   ├── verificar_emails.py          # Verificar buzón IMAP
│   ├── setup.sh                     # Script de instalación
│   ├── deploy_gcp.sh                # Deploy a Google Cloud
│   └── fix_imap.sh                  # Fix de problemas IMAP
│
├── docs/                            # 📚 Documentación
│   ├── inicio-rapido/               # Guías de inicio
│   │   ├── INICIO_RAPIDO.md         # Guía rápida de inicio
│   │   ├── LEEME_PRIMERO.txt        # Instrucciones iniciales
│   │   └── GUIA_PRUEBA_LOCAL.md     # Cómo probar localmente
│   │
│   ├── troubleshooting/             # Resolución de problemas
│   │   ├── TROUBLESHOOTING.md       # Guía general
│   │   ├── ERRORES_COMUNES.md       # Errores frecuentes
│   │   ├── SOLUCION_0_CORREOS.md    # Fix: 0 correos detectados
│   │   └── SOLUCION_PYTHON314.txt   # Fix: Python 3.14
│   │
│   └── COMPARACION_PYTHON_VS_N8N.md # Comparativa de implementaciones
│
├── api/                             # 🌐 API y colecciones
│   └── postman/                     # Colecciones de Postman
│       ├── TravelIA_OC_API.postman_collection.json
│       ├── TravelIA_Development.postman_environment.json
│       └── POSTMAN_SETUP.md         # Guía de configuración
│
├── n8n/                             # 🔄 Workflows de N8N
│   ├── README.md                    # Documentación de workflows
│   ├── README_INSTALACION_N8N.md    # Instalación de N8N
│   ├── GUIA_CONFIGURACION_SISTEMA.md
│   └── workflows/                   # JSON de workflows
│       ├── workflow_deteccion_oc.json
│       ├── workflow_monitoreo_reservas.json
│       └── workflow_recordatorios.json
│
├── templates/                       # 📧 Templates HTML de emails
│   ├── base.html                    # Template base
│   ├── solicitud_inicial.html       # Primera solicitud de OC
│   ├── recordatorio_1.html          # Primer recordatorio
│   ├── recordatorio_2.html          # Segundo recordatorio
│   └── ultimatum.html               # Email de urgencia
│
├── static/                          # 🎨 Archivos estáticos (CSS, JS, img)
│   └── (archivos estáticos del dashboard web)
│
├── data/                            # 💾 Datos y base de datos
│   ├── oc_seguimiento.db            # Base de datos SQLite
│   └── resumen del servicio.pdf     # PDF de ejemplo para tests
│
└── logs/                            # 📝 Logs del sistema (generados)
    └── oc_seguimiento_*.log
```

---

## 🎯 Descripción de Componentes

### Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `app.py` | Aplicación FastAPI con endpoints REST y dashboard web |
| `config.py` | Configuración centralizada usando Pydantic Settings |
| `database.py` | Modelos SQLAlchemy y gestión de base de datos |

### Directorio `src/`

Contiene el código fuente modularizado del sistema:

- **`email_monitor.py`**: Monitoreo IMAP de buzones para detectar confirmaciones de reserva y OC recibidas
- **`email_sender.py`**: Envío de correos SMTP con templates HTML
- **`imap_wrapper.py`**: Wrapper simplificado del protocolo IMAP con reconexión automática
- **`pdf_processor.py`**: Extracción de datos de PDFs (reservas y OC)
- **`scheduler.py`**: Tareas programadas para envío automático de recordatorios

### Directorio `tests/`

Scripts de testing y verificación:

- **`test_flujo_completo.py`**: Test end-to-end del flujo completo
- **`test_imap.py`**: Verificación de conexión y funciones IMAP
- **`test_pdf.py`**: Pruebas de extracción de datos de PDFs
- **`verify_install.py`**: Verificación de dependencias instaladas

### Directorio `scripts/`

Utilidades y herramientas de desarrollo:

- **`enviar_prueba.py`**: Enviar emails de prueba (confirmación o OC)
- **`diagnose_imap.py`**: Diagnóstico de problemas IMAP
- **`verificar_emails.py`**: Inspeccionar buzón IMAP manualmente
- **`setup.sh`**: Instalación automática de dependencias
- **`deploy_gcp.sh`**: Despliegue a Google Cloud Platform

### Directorio `docs/`

Documentación organizada por tema:

**Inicio Rápido:**
- Guías para comenzar a usar el sistema
- Instrucciones de configuración inicial
- Pruebas locales

**Troubleshooting:**
- Solución de problemas comunes
- Errores conocidos y sus fixes
- Compatibilidad con Python 3.14+

### Directorio `api/postman/`

Colecciones de Postman para testing de API:

- Colección con todos los endpoints
- Environment de desarrollo
- Guía de configuración

### Directorio `n8n/`

Workflows alternativos usando N8N:

- Implementación alternativa del sistema
- Workflows JSON importables
- Documentación de configuración

### Directorio `templates/`

Templates Jinja2 para emails HTML:

- Template base con estilos
- Email de solicitud inicial
- Recordatorios (1 y 2)
- Email de ultimatum

### Directorio `data/`

Datos persistentes:

- Base de datos SQLite
- PDFs de ejemplo para testing
- Archivos de OC recibidas (en producción)

---

## 🔄 Flujo de Datos

```
1. Confirmación de Reserva (Email → IMAP)
   ↓
2. ReservaMonitor detecta email con PDF
   ↓
3. pdf_processor extrae datos
   ↓
4. database.py crea registro de Reserva
   ↓
5. scheduler.py programa envío de solicitud OC
   ↓
6. email_sender.py envía solicitud al cliente
   ↓
7. Cliente responde con OC (Email → IMAP)
   ↓
8. OCMonitor detecta email con PDF de OC
   ↓
9. pdf_processor valida OC
   ↓
10. database.py actualiza estado a "recibida"
```

---

## 🚀 Comandos Útiles

### Iniciar el sistema
```bash
python3 app.py
```

### Ejecutar tests
```bash
# Test de flujo completo
python3 tests/test_flujo_completo.py

# Verificar instalación
python3 tests/verify_install.py

# Test de IMAP
python3 tests/test_imap.py
```

### Utilidades
```bash
# Enviar email de prueba
python3 scripts/enviar_prueba.py

# Verificar buzón
python3 scripts/verificar_emails.py

# Diagnóstico IMAP
python3 scripts/diagnose_imap.py
```

### API Testing
```bash
# Health check
curl http://localhost:8001/api/health

# Listar reservas
curl http://localhost:8001/api/reservas

# Ver reserva específica
curl http://localhost:8001/api/reservas/1
```

---

## 📝 Convenciones

### Imports
- Archivos en `src/` usan imports relativos: `from src.module import Class`
- Archivos raíz (`app.py`, `config.py`, `database.py`) se importan directamente
- Tests usan imports absolutos desde root

### Logging
- Logs se guardan en `logs/` con rotación diaria
- Nivel de log configurable en `.env` (`LOG_LEVEL=INFO`)

### Base de Datos
- SQLite por defecto en `data/oc_seguimiento.db`
- Migraciones no versionadas (desarrollo activo)
- Backups recomendados antes de cambios mayores

---

## 🔗 Enlaces Útiles

- **Dashboard Web**: http://localhost:8001/
- **API Docs (Swagger)**: http://localhost:8001/docs
- **API Docs (ReDoc)**: http://localhost:8001/redoc
- **Health Check**: http://localhost:8001/api/health

---

## 📌 Notas Importantes

1. **Nunca commits .env**: Contiene credenciales sensibles
2. **La carpeta `logs/` se genera automáticamente**: No necesita crearse manualmente
3. **`data/` contiene la BD**: Hacer backups regulares en producción
4. **Templates HTML**: Usar Jinja2 syntax para variables dinámicas
5. **IMAP usa PEEK**: Los emails no se marcan como leídos hasta procesarlos

---

## 🤝 Contribución

Al agregar nuevos archivos:

1. Colócalos en el directorio apropiado según su función
2. Actualiza este archivo `ESTRUCTURA.md` si creas nuevas carpetas
3. Documenta los imports necesarios
4. Agrega tests correspondientes en `tests/`

---

**Última actualización**: 2025-11-16
**Versión**: 1.0.0

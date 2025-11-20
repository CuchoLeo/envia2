# 📦 Archivos Deprecados

Esta carpeta contiene archivos y módulos de arquitecturas anteriores que ya no se usan en la versión actual del sistema.

**Fecha de deprecación:** 2025-11-20

---

## 📂 Estructura

### `/integraciones/`
Integraciones con sistemas externos que ya no se utilizan:

#### `/integraciones/api/postman/`
- Colecciones de Postman para testing de API REST
- **Motivo deprecación:** El sistema ya no expone API REST pública
- **Archivos:**
  - `TravelIA_OC_API.postman_collection.json`
  - `TravelIA_Development.postman_environment.json`
  - `POSTMAN_SETUP.md`

#### `/integraciones/n8n/`
- Workflows de automatización con n8n
- **Motivo deprecación:** Migrado a arquitectura interna con APScheduler
- **Archivos:**
  - `workflow_monitoreo_reservas.json` - Monitoreo de confirmaciones
  - `workflow_deteccion_oc.json` - Detección de OC recibidas
  - `workflow_recordatorios.json` - Sistema de recordatorios
  - `README.md` - Guía de uso de n8n
  - `GUIA_CONFIGURACION_SISTEMA.md` - Configuración del sistema con n8n
  - `README_INSTALACION_N8N.md` - Instalación de n8n

**Nota:** Los workflows de n8n fueron reemplazados por:
- `src/email_monitor.py` - Monitoreo de emails
- `src/scheduler.py` - Recordatorios automáticos

---

### `/documentacion/`
Documentación de sesiones de desarrollo anteriores:

- `CONTEXTO_PROYECTO.md` - Contexto inicial del proyecto
- `ESTRUCTURA.md` - Documentación de estructura antigua
- `SESION_2025-11-16.md` - Notas de sesión de desarrollo
- `INDICE_DOCUMENTACION.md` - Índice obsoleto de documentos
- `.env_bkp` - Backup antiguo de configuración

**Motivo deprecación:** Reemplazado por documentación actualizada en `/docs/`

**Documentación vigente:**
- `docs/FLUJO_SISTEMA.md` - Flujo completo del sistema
- `docs/CONFIGURACION_GMAIL.md` - Configuración de Gmail
- `docs/SOLICITUD_INFO_CLIENTE.md` - Formulario para cliente
- `docs/RESUMEN_PARA_CLIENTE.md` - Resumen ejecutivo
- `docs/PLAN_PRUEBAS_CLIENTE.md` - Plan de pruebas
- `LISTA_IMPLEMENTACION_CLIENTE.md` - Guía de implementación

---

### `/scripts_diagnostico/`
Scripts de diagnóstico y configuración inicial:

- `diagnose_imap.py` - Diagnóstico de conexión IMAP
- `fix_imap.sh` - Script para arreglar problemas IMAP
- `setup.sh` - Script de instalación inicial
- `deploy_gcp.sh` - Script de despliegue en GCP

**Motivo deprecación:** Funcionalidad integrada en:
- `scripts/test_conexion.py` - Verificación completa de conexiones
- `scripts/configurar_cliente.py` - Configuración interactiva
- Documentación en `docs/CONFIGURACION_GMAIL.md`

**Scripts vigentes en `/scripts/`:**
- `configurar_cliente.py` - Configuración interactiva completa
- `test_conexion.py` - Test de conexiones IMAP/SMTP
- `enviar_solicitud_oc.py` - Envío manual de solicitudes
- `marcar_no_leido.py` - Utilidad para testing
- `verificar_emails.py` - Verificar emails recibidos

---

### `/tests_desarrollo/`
Tests de desarrollo y archivos de prueba:

- `test_imap.py` - Tests básicos de IMAP
- `test_imap_simple.py` - Tests simplificados de IMAP
- `test_peek.py` - Tests de comando PEEK
- `verify_install.py` - Verificación de instalación
- `resumen_servicio.pdf` - PDF de prueba

**Motivo deprecación:** Reemplazados por tests más completos

**Tests vigentes en `/tests/`:**
- `test_flujo_completo.py` - Test end-to-end del flujo completo
- `test_pdf.py` - Test del procesador de PDFs

---

## 🔄 Arquitectura Actual

### **Sistema Vigente:**

```
Sistema de Seguimiento de OC
├── app.py                      # FastAPI server
├── config.py                   # Configuración
├── database.py                 # SQLAlchemy models
├── requirements.txt            # Dependencias
│
├── src/                        # Módulos principales
│   ├── email_monitor.py        # Monitoreo de emails
│   ├── email_sender.py         # Envío de emails
│   ├── imap_wrapper.py         # Wrapper de IMAP
│   ├── pdf_processor.py        # Procesamiento de PDFs
│   └── scheduler.py            # Scheduler de tareas
│
├── scripts/                    # Scripts útiles
│   ├── configurar_cliente.py  # Setup interactivo
│   ├── test_conexion.py       # Test de conexiones
│   ├── enviar_solicitud_oc.py # Envío manual
│   ├── marcar_no_leido.py     # Utilidad testing
│   └── verificar_emails.py    # Verificar emails
│
├── tests/                      # Tests
│   ├── test_flujo_completo.py # Test E2E
│   └── test_pdf.py            # Test PDF
│
├── templates/                  # Templates de emails
│   ├── solicitud_inicial.html
│   ├── recordatorio_1.html
│   ├── recordatorio_2.html
│   └── ultimatum.html
│
├── docs/                       # Documentación
│   ├── FLUJO_SISTEMA.md
│   ├── CONFIGURACION_GMAIL.md
│   ├── SOLICITUD_INFO_CLIENTE.md
│   ├── RESUMEN_PARA_CLIENTE.md
│   └── PLAN_PRUEBAS_CLIENTE.md
│
└── data/                       # Datos del sistema
    ├── oc_seguimiento.db
    ├── confirmaciones/
    └── oc/
```

---

## 🗑️ ¿Puedo Eliminar Esta Carpeta?

**Recomendación:** Mantener por ahora como referencia histórica.

**Cuándo eliminar:**
- Después de 3-6 meses en producción sin necesidad de referenciar
- Si el espacio en disco es crítico
- Si se requiere limpieza total del repositorio

**Ventajas de mantener:**
- Referencia para entender decisiones de arquitectura
- Workflows de n8n pueden ser útiles para otros proyectos
- Scripts de diagnóstico pueden servir en troubleshooting

---

## 📝 Notas

- Esta carpeta NO es parte del sistema en producción
- NO modificar archivos aquí (solo referencia)
- Ver documentación vigente en `/docs/`
- Para dudas sobre migración: revisar commit history

---

**Última actualización:** 2025-11-20
**Razón:** Limpieza de arquitecturas antiguas y consolidación en arquitectura vigente

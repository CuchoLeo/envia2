# Estructura del Proyecto - Sistema de Seguimiento de OC

**Versión**: 1.3.0 | **Fecha**: 8 de Diciembre de 2024

Este documento describe la estructura organizada del proyecto después de la reorganización v1.3.0.

---

## 📂 Estructura de Directorios

```
envia2/
│
├── 📄 Archivos Principales (Raíz)
│   ├── app.py                      # 🚀 Aplicación FastAPI principal
│   ├── config.py                   # ⚙️  Configuración central (pydantic-settings)
│   ├── database.py                 # 💾 Modelos SQLAlchemy y gestión de BD
│   ├── requirements.txt            # 📦 Dependencias Python
│   ├── README.md                   # 📖 Documentación principal
│   ├── CHANGELOG.md                # 📝 Historial de cambios
│   ├── .env                        # 🔒 Configuración (no en Git)
│   └── .env.example                # 📋 Ejemplo de configuración
│
├── 📦 src/                         # Código fuente principal
│   ├── email_monitor.py            # 👁️  Monitoreo IMAP de confirmaciones y OC
│   ├── email_sender.py             # 📮 Envío de correos via SMTP
│   ├── pdf_processor.py            # 📄 Extracción de datos de PDFs
│   ├── imap_wrapper.py             # 🔌 Wrapper de conexión IMAP
│   └── scheduler.py                # ⏰ Tareas programadas (APScheduler)
│
├── 🎨 templates/                   # Plantillas HTML (Jinja2)
│   ├── dashboard.html              # Dashboard principal con estadísticas
│   ├── reservas.html               # Vista completa de reservas
│   ├── clientes.html               # Gestión de clientes
│   ├── solicitud_inicial.html      # Template email día 0
│   ├── recordatorio_dia2.html      # Template email día 2
│   └── ultimatum_dia4.html         # Template email día 4
│
├── 🔧 scripts/                     # Scripts utilitarios organizados
│   ├── README.md                   # Documentación de scripts
│   │
│   ├── gestion/                    # 🎮 Gestión del sistema
│   │   ├── gestionar_sistema.sh    # Script maestro (start/stop/restart/status/logs)
│   │   ├── detener_sistema.py      # Detención inteligente (Python)
│   │   └── detener_sistema.sh      # Detención rápida (Bash)
│   │
│   ├── database/                   # 💾 Scripts de base de datos
│   │   ├── crear_bd.py             # Crear/inicializar base de datos
│   │   ├── limpiar_base_datos.py   # Limpieza con menú interactivo
│   │   └── cargar_clientes_excel.py # Importar clientes desde Excel
│   │
│   ├── testing/                    # 🧪 Scripts de prueba
│   │   ├── check_inbox.py          # Verificar correos en inbox
│   │   ├── generar_pdf_prueba.py   # Generar PDFs de prueba
│   │   ├── marcar_correos_no_leidos.py
│   │   ├── marcar_no_leido.py
│   │   ├── marcar_oc_no_leido.py
│   │   ├── verificar_correos.py
│   │   └── verificar_reservas.py
│   │
│   └── utils/                      # 🛠️  Utilidades generales
│       ├── configurar_cliente.py   # Configuración interactiva
│       ├── test_conexion.py        # Verificar conexiones IMAP/SMTP
│       ├── enviar_solicitud_oc.py  # Envío manual de solicitudes
│       ├── enviar_prueba.py        # Enviar correos de prueba
│       └── verificar_emails.py     # Verificar configuración de emails
│
├── 📚 docs/                        # Documentación completa
│   ├── README.md                   # 📑 Índice de documentación
│   ├── ALCANCE_PROYECTO.md         # Alcance y objetivos
│   ├── DIAGRAMAS.md                # Diagramas del sistema
│   ├── SCRIPTS_GESTION.md          # Documentación de scripts
│   ├── LISTA_IMPLEMENTACION_CLIENTE.md
│   │
│   ├── arquitectura/               # 🏗️  Arquitectura del sistema
│   │   ├── FLUJO_SISTEMA.md
│   │   └── COMPARATIVA_ARQUITECTURAS_GCP.md
│   │
│   ├── configuracion/              # ⚙️  Guías de configuración
│   │   └── CONFIGURACION_GMAIL.md
│   │
│   ├── cliente/                    # 👥 Documentación para el cliente
│   │   ├── RESUMEN_PARA_CLIENTE.md
│   │   ├── PLAN_PRUEBAS_CLIENTE.md
│   │   └── SOLICITUD_INFO_CLIENTE.md
│   │
│   ├── inicio-rapido/              # 🚀 Guías de inicio
│   │   ├── LEEME_PRIMERO.txt
│   │   ├── INICIO_RAPIDO.md
│   │   └── GUIA_PRUEBA_LOCAL.md
│   │
│   ├── git/                        # 🔧 Control de versiones
│   │   └── INSTRUCCIONES_GIT.md
│   │
│   └── troubleshooting/            # 🔍 Solución de problemas
│       ├── TROUBLESHOOTING.md
│       ├── ERRORES_COMUNES.md
│       ├── SOLUCION_0_CORREOS.md
│       └── SOLUCION_PYTHON314.txt
│
├── 💾 data/                        # Datos del sistema
│   ├── oc_seguimiento.db           # Base de datos SQLite
│   ├── clientes.xlsx               # Archivo de clientes (opcional)
│   ├── reservas_prueba/            # PDFs de prueba
│   └── clientes_backup/            # Backups de configuraciones
│
├── 🧪 tests/                       # Tests automatizados
│   ├── test_flujo_completo.py      # Test end-to-end
│   └── test_pdf.py                 # Test procesador PDF
│
├── 📋 logs/                        # Logs del sistema
│   └── .gitkeep                    # (archivos .log son generados automáticamente)
│
├── 🌐 static/                      # Archivos estáticos web
│   └── (assets CSS/JS si necesario)
│
└── 🗄️  deprecated/                 # Código antiguo (no usar)
    ├── README.md                   # Explicación de archivos deprecados
    ├── integraciones/              # Integraciones obsoletas (n8n, etc)
    ├── documentacion/              # Docs de sesiones antiguas
    ├── scripts_diagnostico/        # Scripts de diagnóstico antiguos
    └── tests_desarrollo/           # Tests de desarrollo

```

---

## 🎯 Principios de Organización

### 1. **Separación por Función**
- **Raíz**: Solo archivos principales de configuración y entrada del sistema
- **src/**: Código fuente del sistema (módulos core)
- **scripts/**: Scripts utilitarios organizados por propósito
- **docs/**: Documentación organizada por audiencia y tema
- **data/**: Todos los archivos de datos centralizados
- **templates/**: Plantillas HTML para web y emails

### 2. **Subcategorías Lógicas**
- **scripts/** dividido en 4 categorías: gestión, database, testing, utils
- **docs/** dividido por tipo: arquitectura, cliente, configuración, troubleshooting

### 3. **Código Deprecated Separado**
- Todo código obsoleto en carpeta `deprecated/`
- No interfiere con estructura principal
- Útil para referencia histórica

---

## 📖 Guías de Uso

### Ejecutar Scripts

**IMPORTANTE**: Todos los scripts deben ejecutarse desde la raíz del proyecto.

```bash
# ✅ Correcto
cd /ruta/al/proyecto/envia2
python scripts/database/crear_bd.py

# ❌ Incorrecto
cd scripts/database
python crear_bd.py  # Esto fallará
```

Ver `scripts/README.md` para más detalles.

### Navegar la Documentación

1. **Inicio rápido**: `docs/inicio-rapido/INICIO_RAPIDO.md`
2. **Arquitectura**: `docs/DIAGRAMAS.md` y `docs/arquitectura/`
3. **Para clientes**: `docs/cliente/`
4. **Problemas**: `docs/troubleshooting/`

Ver `docs/README.md` para índice completo.

### Gestionar el Sistema

```bash
# Iniciar
./scripts/gestion/gestionar_sistema.sh start

# Ver estado
./scripts/gestion/gestionar_sistema.sh status

# Detener
./scripts/gestion/gestionar_sistema.sh stop

# Ver logs
./scripts/gestion/gestionar_sistema.sh logs
```

Ver `docs/SCRIPTS_GESTION.md` para más opciones.

---

## 🔗 Referencias Rápidas

| Necesito... | Ver... |
|------------|--------|
| Iniciar el sistema | `scripts/gestion/gestionar_sistema.sh` |
| Entender arquitectura | `docs/DIAGRAMAS.md` |
| Configurar Gmail | `docs/configuracion/CONFIGURACION_GMAIL.md` |
| Solucionar problemas | `docs/troubleshooting/TROUBLESHOOTING.md` |
| Limpiar base de datos | `scripts/database/limpiar_base_datos.py` |
| Verificar correos | `scripts/testing/check_inbox.py` |
| Documentación completa | `docs/README.md` |
| Scripts disponibles | `scripts/README.md` |

---

## 📝 Notas Importantes

1. **Rutas de Base de Datos**:
   - Configurada en `.env`: `DATABASE_URL=sqlite:///./data/oc_seguimiento.db`
   - La BD está en `data/oc_seguimiento.db`

2. **Imports en Python**:
   - Los archivos principales (`app.py`, `config.py`, `database.py`) están en la raíz
   - Los módulos en `src/` se importan como: `from src.email_monitor import ...`
   - Los scripts deben ejecutarse desde la raíz del proyecto

3. **Ejecutables**:
   - Los scripts `.sh` tienen permisos de ejecución: `chmod +x scripts/gestion/*.sh`

4. **Documentación Viva**:
   - Este documento se actualiza con cada cambio de estructura
   - Ver `CHANGELOG.md` para historial completo

---

## 🔄 Historial de Reorganizaciones

- **v1.3.0** (2024-12-08): Reorganización completa del proyecto
  - Separación de scripts en subcarpetas
  - Organización de documentación por categorías
  - Centralización de datos en `data/`
  - Nuevo sistema de gestión completo

---

**Última actualización**: 2024-12-08
**Versión**: 1.3.0

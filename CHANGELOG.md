# Changelog

Todos los cambios notables en el Sistema de Seguimiento de OC serán documentados en este archivo.

## [1.3.3] - 2024-12-09

### Modificado
- **Sistema de envío de correos usa `email_contacto` de configuracion_clientes** (`src/email_sender.py`)
  - Nuevo método `_get_cliente_email()` busca el email del cliente en la BD
  - Modificados `send_solicitud_inicial()`, `send_recordatorio_dia2()`, `send_ultimatum_dia4()`
  - Ahora envía solicitudes de OC al email configurado en `configuracion_clientes.email_contacto`
  - Si no hay email configurado, registra error en BD y loguea warning
  - Eliminados todos los placeholders "contacto@agencia.com"

### Corregido
- **Todos los scripts ahora ejecutables desde cualquier directorio**
  - Agregado `os.chdir(project_root)` a 11 scripts
  - Scripts cambian automáticamente al directorio raíz del proyecto
  - Solucionados problemas con rutas relativas (ej: `data/oc_seguimiento.db`)
  - Ahora funcionan: `cd scripts/database && python limpiar_base_datos.py`

### Agregado
- **Módulo auxiliar** `scripts/_fix_path.py` para futuros scripts
- **Script de carga de clientes** `scripts/database/cargar_clientes_lista.py`
  - Carga 76 clientes desde lista hardcoded
  - Actualiza o crea registros en configuracion_clientes
  - Muestra estadísticas y resumen de operación

### Base de Datos
- **76 clientes cargados en configuracion_clientes**
  - 37 requieren OC (48.7%)
  - 39 NO requieren OC (51.3%)
  - **PENDIENTE**: Poblar campo `email_contacto` para cada cliente

### Documentación
- **Nuevo documento** `docs/CAMBIO_EMAIL_CONTACTO.md`
  - Explicación detallada del cambio
  - Flujo de envío de correos antes/después
  - Casos de error y manejo
  - Guía de testing y próximos pasos
- **Actualizado** `scripts/README.md` con instrucción de cambio de CWD
- **Actualizado** `docs/inicio-rapido/INICIO_RAPIDO.md` - Tip sobre run_script.sh
- **Actualizado** `docs/inicio-rapido/LEEME_PRIMERO.txt` - Nota sobre PYTHONPATH

## [1.3.2] - 2024-12-09

### Agregado
- **Script wrapper `run_script.sh`** para facilitar la ejecución de scripts
  - Configura automáticamente PYTHONPATH
  - Verifica que estés en la raíz del proyecto
  - Verifica que el entorno virtual esté activado
  - Muestra mensajes informativos de éxito/error
  - Uso: `./run_script.sh scripts/database/crear_bd.py`

### Modificado
- **Actualizada documentación completa** con instrucciones de PYTHONPATH
  - `scripts/README.md` - Todos los ejemplos ahora incluyen `PYTHONPATH=.`
  - `docs/inicio-rapido/INICIO_RAPIDO.md` - Actualizada guía con comandos correctos
  - `docs/inicio-rapido/LEEME_PRIMERO.txt` - Agregada nota sobre PYTHONPATH
  - Sección de troubleshooting expandida con 3 soluciones alternativas

### Corregido
- **Problema con ejecución de scripts** - ModuleNotFoundError
  - Ahora todos los ejemplos incluyen `PYTHONPATH=.`
  - Documentado el uso del script wrapper
  - Agregadas 3 soluciones: PYTHONPATH directo, wrapper, o alias permanente

### Documentación
- Actualizada versión del sistema a 1.3.2 en todas las guías
- Agregadas notas importantes al inicio de INICIO_RAPIDO.md y LEEME_PRIMERO.txt
- Expandida sección de troubleshooting en scripts/README.md

## [1.3.1] - 2024-12-09

### Corregido
- **Error crítico en IMAP wrapper** (`src/imap_wrapper.py:fetch_message`)
  - Agregada validación robusta para datos retornados por IMAP fetch
  - Corregido error: "'int' object has no attribute 'decode'"
  - Ahora verifica que `data` no esté vacío antes de procesarlo
  - Valida que `data[0]` sea tupla con formato correcto
  - Verifica que `raw_email` sea bytes antes de parsear
  - Agregado traceback detallado para debugging
  - Previene crashes cuando IMAP retorna formatos inesperados

### Agregado
- **Script de prueba IMAP**: `scripts/testing/test_imap_fetch.py`
  - Prueba conexión IMAP y fetch de mensajes
  - Útil para diagnosticar problemas con mensajes específicos
  - Muestra estadísticas de éxito/errores
  - Ejecutar: `python scripts/testing/test_imap_fetch.py`

## [1.3.0] - 2024-12-08

### 🔄 Reorganización Completa del Proyecto

#### Estructura de Carpetas
- **Reorganización completa** de archivos y carpetas con estructura lógica profesional
  - `scripts/` ahora organizado en subcarpetas: `gestion/`, `database/`, `testing/`, `utils/`
  - `docs/` reorganizado por categorías: `arquitectura/`, `configuracion/`, `cliente/`, `git/`, `troubleshooting/`
  - `data/` centraliza todos los archivos de datos: base de datos, PDFs de prueba, Excel de clientes

#### Scripts de Gestión
- **Nuevo sistema completo de gestión** del sistema:
  - `scripts/gestion/gestionar_sistema.sh` - Script maestro (start/stop/restart/status/logs)
  - `scripts/gestion/detener_sistema.py` - Detención inteligente con modos interactivo y forzado
  - `scripts/gestion/detener_sistema.sh` - Versión Bash optimizada

#### Scripts de Base de Datos
- Movidos a `scripts/database/`:
  - `crear_bd.py` - Inicializar base de datos
  - `limpiar_base_datos.py` - Limpieza con menú interactivo
  - `cargar_clientes_excel.py` - Importar clientes desde Excel

#### Scripts de Testing
- Movidos a `scripts/testing/`:
  - `check_inbox.py` - Verificar correos en inbox
  - `generar_pdf_prueba.py` - Generar PDFs de prueba
  - `marcar_correos_no_leidos.py` - Marcar correos para reprocesar
  - `verificar_correos.py` y `verificar_reservas.py` - Diagnóstico

#### Scripts Utilitarios
- Movidos a `scripts/utils/`:
  - `configurar_cliente.py` - Configuración interactiva
  - `test_conexion.py` - Verificar conexiones IMAP/SMTP
  - `enviar_solicitud_oc.py` - Envío manual
  - `verificar_emails.py` - Verificación de configuración

#### Documentación
- **Índice centralizado** en `docs/README.md`
- Documentación organizada por categorías:
  - `arquitectura/` - FLUJO_SISTEMA.md, COMPARATIVA_ARQUITECTURAS_GCP.md
  - `configuracion/` - CONFIGURACION_GMAIL.md
  - `cliente/` - RESUMEN, PLAN_PRUEBAS, SOLICITUD_INFO
  - `inicio-rapido/` - LEEME_PRIMERO, INICIO_RAPIDO, GUIA_PRUEBA_LOCAL
  - `git/` - INSTRUCCIONES_GIT.md
  - `troubleshooting/` - Guías completas de solución de problemas
- **Nuevo `scripts/README.md`** con documentación completa de uso
- **Actualizado README.md principal** con nueva estructura del proyecto

#### Datos
- Centralización en carpeta `data/`:
  - `oc_seguimiento.db` - Base de datos
  - `reservas_prueba/` - PDFs de prueba
  - `clientes_backup/` - Backups de configuración
  - `clientes.xlsx` - Archivo de clientes

#### Mejoras Técnicas
- Archivos `__init__.py` en todos los módulos de scripts
- Documentación de cómo ejecutar scripts desde la raíz del proyecto
- Notas de troubleshooting para problemas comunes de imports
- Configuración actualizada para rutas de base de datos

### Agregado
- **Sistema de gestión completo** con scripts Bash y Python
- **Documentación organizada** por categorías temáticas
- **README de scripts** con ejemplos de uso
- **Índice de documentación** centralizado

### Modificado
- **Rutas de base de datos** actualizadas a `data/oc_seguimiento.db`
- **Estructura del README** con árbol de proyecto actualizado
- **Enlaces de documentación** apuntando a nueva estructura

### Movido
- 7 scripts de gestión → `scripts/gestion/`
- 3 scripts de BD → `scripts/database/`
- 7 scripts de testing → `scripts/testing/`
- 6 scripts utilitarios → `scripts/utils/`
- 15+ archivos de docs → categorías en `docs/`
- Archivos de datos → `data/`

## [1.2.0] - 2025-12-07

### Agregado
- **Vistas HTML completas para gestión**:
  - `/reservas` - Vista completa de todas las reservas con filtros y búsqueda (`templates/reservas.html`)
  - `/clientes` - Vista de configuración de clientes con estadísticas (`templates/clientes.html`)
  - Botones de navegación en el dashboard principal

- **Sistema de carga de clientes desde Excel**:
  - Script `cargar_clientes_excel.py` para importar configuración desde `docs/clientes.xlsx`
  - Soporte para 79 clientes cargados desde Excel
  - Actualización automática de registros existentes
  - Validación y estadísticas de carga

- **Procesador de PDF mejorado** (`src/pdf_processor.py:155-199`):
  - Ahora acepta **13+ formatos diferentes** para detectar montos:
    - `Total: CLP 123456`
    - `Total: $123.456`
    - `Monto Total: CLP 123456`
    - `Total a Pagar: $123.456`
    - `Precio Total: CLP 123456`
    - Y 8 formatos adicionales con detección de respaldo
  - Sistema de patrones múltiples con fallback automático
  - Logs informativos del patrón que detectó el monto

- **Scripts de utilidad**:
  - `limpiar_base_datos.py` - Gestión completa de limpieza de BD con menú interactivo
    - Eliminar todas las reservas
    - Eliminar reservas específicas por ID
    - Eliminar solo reservas de prueba (TEST*)
    - Ver estadísticas y listar reservas
  - `marcar_correos_no_leidos.py` - Reprocesar correos marcándolos como no leídos
    - Filtros por asunto y remitente
    - Modo interactivo y por línea de comandos

- **Comparativa de arquitecturas GCP** (`docs/COMPARATIVA_ARQUITECTURAS_GCP.md`):
  - Análisis detallado de 4 opciones de despliegue en Google Cloud
  - Comparativa de costos ($5-$153/mes)
  - Recomendación: Compute Engine e2-micro ($9.87/mes con Free Tier)
  - Plan de migración de 4-5 horas
  - Optimizaciones de costos y arquitectura propuesta

### Modificado
- **Dashboard principal mejorado** (`templates/dashboard.html`):
  - Nuevos botones de navegación a Reservas y Clientes
  - Mejoras visuales en la interfaz
  - Enlaces actualizados en la sección API REST

- **Configuración de clientes**:
  - Base de datos ahora con 79 clientes configurados
  - 40 clientes requieren OC, 39 no requieren
  - Datos sincronizados desde archivo Excel

### Deprecado
- **Documentación obsoleta movida a `deprecated/docs/`**:
  - `COMPARACION_PYTHON_VS_N8N.md` - Ya no usamos n8n
  - `MIGRACION_OFFICE365.md` - Se mantuvo Gmail, no se migró a Office 365

### Correcciones
- Mejorada detección de montos en PDFs que antes fallaban
- Sistema ahora procesa PDFs con formatos de monto más flexibles
- Validación más robusta con múltiples intentos de extracción

### Base de Datos
- Tabla `configuracion_clientes` poblada con 79 registros desde Excel
- Sistema de limpieza automatizado para mantenimiento

## [1.1.1] - 2025-11-20

### Agregado
- Nuevo patrón de búsqueda para "Orden de Compra CODIGO" (`src/email_monitor.py:458-467`)
  - Detecta asuntos como "orden de compra AAFWHWS" o "OC AAFWHWS"
  - Búsqueda case-insensitive y flexible
  - Permite asociar OC con formato más natural

### Configuración
- Agregado `cuchohbk@gmail.com` a lista de remitentes autorizados (`.env:77`)
  - Permite recibir correos de OC desde esta casilla adicional
  - Facilita testing y flujo de trabajo de producción

### Documentación
- Agregado archivo `DIAGRAMAS.md` con visualizaciones completas del sistema:
  - Diagrama de Arquitectura del Sistema
  - Diagrama de Flujo del Proceso de OC
  - Diagrama de Secuencia - Flujo Completo
  - Diagrama de Estados de una Reserva
  - Diagrama de Componentes - Detalle Técnico
  - Diagrama de Patrones de Detección de OC
  - Diagrama ER de Base de Datos
- Actualizado `README.md` con referencia a diagramas y ejemplos de patrones de detección

### Correcciones
- Corregida inconsistencia de mayúsculas/minúsculas en nombres de agencia
  - "Hotel sales" → "Hotel Sales" para coincidir con configuración
  - Asegura correcta visualización en dashboard

## [1.1.0] - 2025-11-20

### Agregado
- Nuevo patrón de búsqueda "Reserva CODIGO" para asociar correos de OC con reservas
  - Ahora el sistema puede detectar correos con asunto "Orden de Compra - Reserva AAFVDUA" y similares
  - Búsqueda flexible por `id_reserva` o `loc_interno` (`src/email_monitor.py:447-456`)

- Scripts de utilidad para testing:
  - `marcar_oc_no_leido.py` - Marca correos de OC como no leídos para pruebas
  - `verificar_correos.py` - Verifica estado de correos en la bandeja de entrada
  - `generar_pdf_prueba.py` - Genera PDFs de prueba para flujo completo

### Modificado
- **Sistema configurado para requerir OC en TODAS las reservas** (`src/email_monitor.py:233-234`)
  - Comentada validación por agencia específica
  - Ahora `requiere_oc = True` para todas las reservas procesadas
  - Simplifica el flujo y asegura seguimiento completo

- Mejoras en la detección de remitentes de correos
  - Uso de `parseaddr()` para extraer dirección de email correctamente del campo "From"
  - Maneja correctamente formato "Nombre Completo <email@ejemplo.com>"

- PDFProcessor ahora usa LOC Interno como fallback para `id_reserva`
  - Si el campo "ID:" no existe en el PDF, usa el valor de "LOC Interno"
  - Mejora compatibilidad con diferentes formatos de confirmación

### Base de Datos
- Agregada agencia "Hotel Sales" a `configuracion_clientes`
  - Email de contacto: hotel.sales@example.com
  - Requiere OC: Sí
  - Días de recordatorio: 2 y 4

### Correcciones
- Solucionado problema con enums de estado que causaba incompatibilidad de base de datos
- Corregido problema con variables de entorno del sistema sobrescribiendo `.env`
- Arreglada lógica de filtrado en dashboard para usar `filter_by` correctamente

### Testing
- Flujo completo de OC verificado exitosamente:
  1. Correo de confirmación → Reserva creada (PENDIENTE)
  2. Correo de OC → Detección y asociación automática
  3. Estado actualizado → Reserva marcada como RECIBIDA

## [1.0.0] - 2025-11-18

### Inicial
- Lanzamiento inicial del Sistema de Seguimiento de OC
- Monitoreo automático de correos IMAP
- Extracción de datos de PDFs de confirmación
- Detección de órdenes de compra recibidas
- Flujo escalonado de comunicaciones (Día 0, 2, 4)
- Dashboard web de administración
- API REST completa
- Base de datos SQLite con modelos completos
- Scheduler automático con APScheduler
- Plantillas HTML profesionales para emails
- Sistema de logs con rotación diaria

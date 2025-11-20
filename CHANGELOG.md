# Changelog

Todos los cambios notables en el Sistema de Seguimiento de OC serán documentados en este archivo.

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

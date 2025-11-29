# Alcance del Proyecto - Sistema de Seguimiento de Órdenes de Compra

**Proyecto**: Sistema de Seguimiento de OC
**Cliente**: Kontrol Travel
**Versión Actual**: 1.1.1
**Fecha**: Noviembre 2025
**Estado**: Producción (Fase 1)

---

## 📋 Resumen Ejecutivo

El Sistema de Seguimiento de Órdenes de Compra (OC) es una solución automatizada diseñada para gestionar y hacer seguimiento de las órdenes de compra requeridas por clientes corporativos en el proceso de reservas hoteleras. El sistema automatiza la solicitud, recordatorios y recepción de órdenes de compra, reduciendo significativamente la carga administrativa manual.

---

## 🎯 Objetivo del Proyecto

Automatizar el proceso de solicitud y seguimiento de órdenes de compra para reservas hoteleras corporativas, asegurando que todas las reservas que requieren OC tengan el documento formal antes de la confirmación final, mediante un flujo escalonado de comunicaciones y monitoreo automático.

---

## ✅ Alcance Actual (v1.1.1)

### 1. Monitoreo Automático de Correos

**QUÉ HACE:**
- Monitorea casilla IMAP (`seguimientoocx@gmail.com`) cada 60 segundos
- Detecta correos de confirmación de reserva con PDFs adjuntos
- Detecta correos de órdenes de compra recibidas
- Valida remitentes autorizados configurable
- Soporta múltiples remitentes autorizados simultáneamente

**QUÉ NO HACE:**
- No procesa correos de otras casillas simultáneamente
- No clasifica correos automáticamente (spam, promociones, etc.)
- No responde automáticamente a los correos recibidos
- No reenvía correos a otras direcciones
- No elimina correos del servidor

**LIMITACIONES:**
- Solo Gmail/IMAP compatible (requiere configuración de apps menos seguras)
- Intervalo mínimo de verificación: 60 segundos (configurable)
- No soporta autenticación OAuth2 (solo usuario/contraseña)

---

### 2. Procesamiento de PDFs

**QUÉ HACE:**
- Extrae datos de PDFs de confirmación de reserva:
  - ID de reserva / LOC Interno
  - Nombre de agencia/cliente
  - Hotel y dirección
  - Fechas de check-in/check-out
  - Número de noches
  - Monto total
- Valida estructura y campos obligatorios
- Guarda PDFs en `data/confirmaciones/`
- Usa LOC Interno como fallback para ID

**QUÉ NO HACE:**
- No procesa PDFs escaneados (solo PDFs con texto seleccionable)
- No extrae imágenes de los PDFs
- No valida montos contra tarifas reales
- No convierte PDFs a otros formatos
- No comprime o modifica PDFs originales
- No procesa PDFs protegidos con contraseña

**LIMITACIONES:**
- Requiere formato específico de PDF de Kontrol Travel
- Campos deben estar en ubicaciones predecibles
- Archivos máximo ~10MB (configurable en servidor)
- No OCR (reconocimiento óptico de caracteres)

---

### 3. Gestión de Estado de Reservas

**QUÉ HACE:**
- Crea reservas automáticamente desde PDFs
- Gestiona estados de OC:
  - `NO_REQUIERE_OC`: Cliente no necesita OC
  - `PENDIENTE`: OC requerida, esperando envío inicial
  - `SOLICITADA`: Solicitud enviada, esperando respuesta
  - `RECIBIDA`: OC recibida y asociada
  - `CANCELADA`: Reserva cancelada manualmente
  - `EXPIRADA`: Check-in pasó sin recibir OC
- Evita duplicados por ID de reserva
- Actualiza timestamps automáticamente

**QUÉ NO HACE:**
- No cancela reservas automáticamente
- No sincroniza con sistemas externos (PMS, CRM)
- No valida disponibilidad hotelera
- No gestiona pagos o facturación
- No envía confirmaciones al pasajero final
- No modifica tarifas o condiciones

**LIMITACIONES:**
- Estado `EXPIRADA` debe marcarse manualmente
- No hay workflow de aprobación multi-nivel
- No soporta reservas multi-destino en un solo registro

---

### 4. Flujo Escalonado de Comunicaciones

**QUÉ HACE:**
- Envía correo automático en 3 momentos:
  - **Día 0**: Solicitud inicial inmediata
  - **Día 2**: Recordatorio amable (configurable)
  - **Día 4**: Ultimátum (configurable)
- Plantillas HTML profesionales personalizables
- Incluye datos de la reserva en el correo
- CC automático a administración
- Registra todos los envíos en base de datos
- Maneja reintentos en caso de fallo SMTP

**QUÉ NO HACE:**
- No envía correos fuera del flujo de 3 niveles
- No permite personalización por cliente (todas las agencias reciben mismo formato)
- No adjunta PDFs en los correos de solicitud
- No usa plantillas dinámicas (ej: según idioma del cliente)
- No envía SMS o notificaciones push
- No programa envíos en horarios específicos (ej: solo lunes-viernes)

**LIMITACIONES:**
- Solo un flujo de comunicación por reserva
- Días de recordatorio globales (no por cliente)
- No soporta múltiples idiomas
- Requiere servidor SMTP externo (Gmail)

---

### 5. Detección de OC Recibidas

**QUÉ HACE:**
- Detecta correos de OC con 4 patrones:
  1. "Reserva CODIGO" → `Orden de Compra - Reserva AAFVDUA`
  2. "LOC CODIGO" → `OC para LOC TEST2024002`
  3. "Orden de Compra CODIGO" → `orden de compra AAFWHWS`
  4. "OC CODIGO" → `OC AAFWHWS`
- Búsqueda case-insensitive
- Asocia automáticamente con reserva existente
- Actualiza estado a `RECIBIDA`
- Detiene flujo de recordatorios
- Registra número de OC y fecha de recepción

**QUÉ NO HACE:**
- No valida contenido del correo de OC
- No requiere adjuntos (solo detecta por asunto)
- No verifica que el PDF adjunto sea una OC real
- No valida montos en la OC contra reserva
- No detecta OC duplicadas
- No notifica al cliente que la OC fue recibida

**LIMITACIONES:**
- Depende 100% del formato del asunto del correo
- Si el asunto no incluye el código, no se asocia
- No hay validación de OC real vs. correo falso
- No soporta códigos alfanuméricos complejos

---

### 6. Dashboard Web de Administración

**QUÉ HACE:**
- Visualización en tiempo real:
  - Estadísticas generales
  - Reservas pendientes de OC
  - OC recibidas recientemente
- Acciones manuales:
  - Marcar OC como recibida
  - Reenviar correos
  - Ver detalles de reserva
- Interfaz responsive (móvil/desktop)
- API REST completa documentada

**QUÉ NO HACE:**
- No permite editar datos de reservas
- No permite eliminar reservas
- No tiene sistema de usuarios/roles
- No genera reportes en PDF/Excel
- No tiene gráficos o charts estadísticos
- No permite configurar el sistema desde la web
- No tiene búsqueda avanzada o filtros complejos

**LIMITACIONES:**
- Autenticación básica (usuario/contraseña estático)
- Un solo usuario administrador
- No hay registro de auditoría de acciones
- No soporta múltiples sesiones simultáneas
- Actualización manual (sin websockets)

---

### 7. Base de Datos

**QUÉ HACE:**
- SQLite para almacenamiento local
- 4 tablas principales:
  - `reservas`: Datos de reservas
  - `ordenes_compra`: OC recibidas
  - `correos_enviados`: Historial de envíos
  - `configuracion_clientes`: Config por agencia
- Timestamps automáticos
- Relaciones definidas (FK)
- Migraciones con SQLAlchemy

**QUÉ NO HACE:**
- No tiene respaldos automáticos
- No soporta clustering o réplicas
- No encripta datos sensibles
- No tiene compresión de datos históricos
- No archiva datos antiguos automáticamente

**LIMITACIONES:**
- SQLite: límite práctico ~100K registros
- No transaccional complejo
- Un solo proceso escritor a la vez
- No optimizado para reportes pesados
- Archivo único vulnerable a corrupción

---

### 8. Configuración del Sistema

**QUÉ HACE:**
- Archivo `.env` para todas las configuraciones
- Variables para:
  - Credenciales IMAP/SMTP
  - Intervalos de verificación
  - Días de recordatorios
  - Remitentes autorizados
  - Agencias que requieren OC
- Validación de configuración al iniciar
- Mensajes de error claros si falta config

**QUÉ NO HACE:**
- No valida credenciales hasta el primer uso
- No encripta credenciales en `.env`
- No permite configuración por interfaz web
- No tiene perfiles de configuración (dev/staging/prod)
- No sincroniza config entre instancias

**LIMITACIONES:**
- Requiere reiniciar sistema para aplicar cambios
- No hay validación de sintaxis en `.env`
- Contraseñas en texto plano (riesgo de seguridad)

---

## ❌ Fuera del Alcance Actual

### Funcionalidades NO Incluidas en v1.1.1

1. **Integración con Sistemas Externos**
   - No se conecta a PMS (Property Management System) hotelero
   - No sincroniza con CRM existente
   - No se integra con sistemas de facturación
   - No consulta APIs de hoteles o proveedores

2. **Procesamiento Avanzado de Documentos**
   - No hace OCR de documentos escaneados
   - No valida firmas digitales en PDFs
   - No compara versiones de OC (revisiones)
   - No detecta alteraciones en documentos

3. **Gestión de Usuarios y Permisos**
   - No hay roles diferenciados (admin, operador, solo lectura)
   - No hay autenticación con SSO o OAuth
   - No hay registro de auditoría de acciones por usuario
   - No permite asignación de reservas a usuarios específicos

4. **Reportes y Analytics**
   - No genera reportes automáticos periódicos
   - No tiene dashboards con gráficos avanzados
   - No calcula KPIs o métricas de negocio
   - No exporta a Excel/CSV/PDF

5. **Comunicaciones Avanzadas**
   - No envía WhatsApp o SMS
   - No tiene chat en vivo con clientes
   - No soporta múltiples idiomas
   - No personaliza plantillas por cliente

6. **Workflow Avanzado**
   - No tiene aprobaciones multi-nivel
   - No permite excepciones o casos especiales automatizados
   - No escala automáticamente problemas
   - No tiene SLA tracking

7. **Integración Bancaria/Pagos**
   - No procesa pagos
   - No valida cuentas bancarias
   - No genera conciliaciones
   - No emite facturas

8. **Movilidad**
   - No hay app móvil nativa
   - No hay notificaciones push
   - Dashboard web responsive pero no optimizado para móvil

---

## 🚀 Roadmap de Expansión Futura

### Fase 2 (Próxima Versión - v2.0)

#### 2.1. Gestión Avanzada de Clientes
**Objetivo**: Configuración granular por cliente

- [ ] Archivo Excel para configuración de clientes (`docs/clientesOC.xlsx`)
  - Lista de clientes con flag de requiere OC (SI/NO)
  - Lectura automática sin reinicio del sistema
  - Validación de nombres contra PDFs
- [ ] Días de recordatorio personalizados por cliente
- [ ] Plantillas de correo personalizadas por cliente
- [ ] Idioma de comunicación por cliente
- [ ] Contactos múltiples por cliente

**Beneficios**:
- Eliminación de configuración manual en `.env`
- Fácil onboarding de nuevos clientes
- Mayor flexibilidad operativa

---

#### 2.2. Sistema de Usuarios y Roles
**Objetivo**: Acceso multi-usuario con permisos

- [ ] Autenticación con usuario/contraseña individual
- [ ] Roles: Admin, Operador, Solo Lectura
- [ ] Registro de auditoría completo
- [ ] Asignación de reservas a operadores
- [ ] Notificaciones por email a usuarios

**Beneficios**:
- Mayor seguridad
- Trazabilidad de acciones
- Distribución de carga de trabajo

---

#### 2.3. Reportes y Analytics
**Objetivo**: Visibilidad de desempeño del sistema

- [ ] Dashboard con gráficos (Chart.js)
- [ ] Reportes automáticos semanales/mensuales
- [ ] Exportación a Excel/CSV
- [ ] KPIs: Tiempo promedio de recepción de OC, tasa de cumplimiento
- [ ] Alertas de reservas vencidas

**Beneficios**:
- Toma de decisiones basada en datos
- Identificación de clientes problemáticos
- Mejora continua del proceso

---

### Fase 3 (Mediano Plazo - v3.0)

#### 3.1. Integración con Sistemas Externos
**Objetivo**: Sincronización bidireccional

- [ ] API REST consumible por sistemas externos
- [ ] Webhooks para notificaciones en tiempo real
- [ ] Integración con PMS hotelero (ej: Opera, Mews)
- [ ] Conexión con sistema de facturación
- [ ] Sincronización con CRM (ej: Salesforce, HubSpot)

**Beneficios**:
- Eliminación de doble captura de datos
- Flujo de información automático
- Reducción de errores humanos

---

#### 3.2. Procesamiento Avanzado de Documentos
**Objetivo**: Mayor automatización en extracción

- [ ] OCR para PDFs escaneados (Tesseract o Google Vision API)
- [ ] Validación de campos contra reglas de negocio
- [ ] Detección de alteraciones en documentos
- [ ] Extracción de datos de formatos variados (Word, imágenes)
- [ ] Clasificación automática de documentos (OC vs. Factura vs. Confirmación)

**Beneficios**:
- Menor dependencia de formatos específicos
- Procesamiento de más tipos de documentos
- Mayor precisión en extracción

---

#### 3.3. Comunicaciones Multi-Canal
**Objetivo**: Llegar a clientes por su canal preferido

- [ ] Envío de SMS vía Twilio o similar
- [ ] Integración con WhatsApp Business API
- [ ] Notificaciones push en app móvil
- [ ] Chat en vivo en dashboard
- [ ] Preferencia de canal por cliente

**Beneficios**:
- Mayor tasa de respuesta
- Mejor experiencia de cliente
- Reducción de tiempos de gestión

---

### Fase 4 (Largo Plazo - v4.0+)

#### 4.1. Inteligencia Artificial y Machine Learning

- [ ] Predicción de probabilidad de recepción de OC a tiempo
- [ ] Clasificación automática de urgencia de seguimiento
- [ ] Detección de anomalías en documentos
- [ ] Sugerencias de mejores horarios de envío
- [ ] Chatbot para responder preguntas frecuentes

---

#### 4.2. Escalabilidad Enterprise

- [ ] Migración a PostgreSQL o base de datos cloud
- [ ] Arquitectura de microservicios
- [ ] Balanceo de carga y alta disponibilidad
- [ ] Multi-tenancy (múltiples empresas en una instancia)
- [ ] Disaster recovery y backups automáticos

---

#### 4.3. Movilidad y Accesibilidad

- [ ] App móvil nativa (iOS/Android)
- [ ] PWA (Progressive Web App) offline-first
- [ ] Notificaciones push móviles
- [ ] Escaneo de documentos desde móvil
- [ ] Aprobación de OC desde móvil

---

## 📊 Criterios de Éxito Actual (v1.1.1)

### Métricas Clave

1. **Automatización**
   - ✅ 100% de correos de confirmación procesados automáticamente
   - ✅ 95%+ de OC detectadas correctamente al recibirse
   - ✅ 0 intervención manual para envíos programados

2. **Reducción de Carga Manual**
   - ✅ Eliminación de revisión manual de bandeja de entrada
   - ✅ Envío automático de 3 niveles de comunicación
   - ✅ Detección automática de OC sin clasificación manual

3. **Confiabilidad**
   - ✅ Sistema operativo 24/7 sin intervención
   - ✅ < 5 minutos de downtime mensual
   - ✅ Recuperación automática de fallos IMAP/SMTP

4. **Visibilidad**
   - ✅ Dashboard con estado actual de todas las reservas
   - ✅ Historial completo de comunicaciones
   - ✅ Identificación rápida de reservas pendientes

---

## 🔒 Consideraciones de Seguridad

### Implementadas

- Validación de remitentes autorizados
- Contraseñas en archivo `.env` (no en código)
- SSL/TLS para conexiones IMAP/SMTP
- Timestamps para auditoría básica

### Pendientes (Futuras Fases)

- Encriptación de credenciales en `.env`
- Autenticación OAuth2 para Gmail
- Certificados SSL para dashboard
- Encriptación de datos sensibles en BD
- Rate limiting en API
- Registro completo de auditoría

---

## 🛠️ Requisitos Técnicos

### Mínimos (Actual)

- **Sistema Operativo**: Linux/macOS/Windows
- **Python**: 3.10 o superior
- **RAM**: 512 MB mínimo, 1 GB recomendado
- **Disco**: 500 MB (+ espacio para PDFs y logs)
- **Red**: Conexión estable a Internet
- **Email**: Cuenta Gmail con IMAP/SMTP habilitado

### Recomendados (Producción)

- **Sistema Operativo**: Ubuntu Server 20.04 LTS o superior
- **Python**: 3.11+
- **RAM**: 2 GB
- **Disco**: 10 GB SSD
- **Servidor**: VPS o Cloud (GCP e2-micro o superior)
- **Base de Datos**: PostgreSQL 14+ (futuro)

---

## 📈 Indicadores de Escalamiento

### Cuándo Migrar a Fase 2

- Más de 20 clientes corporativos activos
- Más de 100 reservas/mes procesadas
- Necesidad de reportes mensuales
- Equipo de más de 2 personas operando el sistema

### Cuándo Migrar a Fase 3

- Más de 50 clientes corporativos
- Más de 500 reservas/mes
- Integración con sistemas externos requerida
- Necesidad de escalabilidad horizontal

### Cuándo Migrar a Fase 4

- Multi-país o multi-empresa
- Más de 2000 reservas/mes
- Equipo distribuido geográficamente
- Requerimientos de SLA enterprise

---

## 🤝 Stakeholders

### Internos
- **Equipo de Operaciones**: Usuarios principales del dashboard
- **Administración**: Visibilidad de cumplimiento de OC
- **Finanzas**: Aseguramiento de documentación para facturación
- **IT**: Mantenimiento y soporte del sistema

### Externos
- **Clientes Corporativos**: Reciben solicitudes de OC
- **Proveedores Hoteleros**: Beneficiados indirectamente por proceso ágil

---

## 📞 Soporte y Mantenimiento

### Incluido en v1.1.1

- Logs detallados para troubleshooting
- Documentación técnica completa
- Scripts de utilidad para testing
- Configuración de ejemplo (`.env.example`)

### No Incluido

- Soporte 24/7
- Actualización automática de código
- Monitoreo externo (uptime monitoring)
- Respaldos automáticos programados

---

## 📝 Notas Finales

Este documento define claramente el alcance actual del Sistema de Seguimiento de OC v1.1.1 y establece un roadmap realista para futuras expansiones. El diseño modular del sistema permite agregar funcionalidades de manera incremental sin refactorización completa.

**Filosofía de Desarrollo**: Enfoque iterativo y pragmático. Cada fase se completa y valida antes de avanzar a la siguiente, asegurando que el valor se entrega progresivamente y el sistema se mantiene estable.

---

**Última Actualización**: Noviembre 2025
**Próxima Revisión**: Enero 2026

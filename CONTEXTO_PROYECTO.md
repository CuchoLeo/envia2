# Contexto del Proyecto - Sistema de Seguimiento de OC

**Última actualización**: 2025-11-16
**Sesión de trabajo**: Reorganización y optimización del sistema

---

## 📌 Estado Actual del Proyecto

### Sistema Funcional ✅
- **Aplicación**: Sistema de seguimiento de órdenes de compra para reservas hoteleras
- **Stack**: Python 3.14+, FastAPI, SQLite, IMAP/SMTP
- **Estado**: Funcional en desarrollo, listo para despliegue

### Última Configuración Conocida
- **Puerto**: 8001
- **Base de datos**: `data/oc_seguimiento.db` (SQLite)
- **Email monitoreo**: cuchohbk@gmail.com
- **IMAP**: Gmail (imap.gmail.com:993)
- **SMTP**: Gmail (smtp.gmail.com:587)

---

## 🔄 Flujo del Sistema

```
1. Hotel envía confirmación de reserva (PDF) → cuchohbk@gmail.com
   ↓
2. ReservaMonitor detecta email con palabras clave:
   - "confirmación" / "confirmacion" / "confirmation"
   ↓
3. pdf_processor extrae datos del PDF
   ↓
4. Se crea registro en base de datos (estado: "pendiente")
   ↓
5. scheduler programa envío de solicitud de OC al cliente
   ↓
6. email_sender envía solicitud automática
   ↓
7. Cliente responde con OC (PDF) → cuchohbk@gmail.com
   ↓
8. OCMonitor detecta email con palabras clave:
   - "orden de compra" / "oc" / "purchase order" / "orden compra"
   ↓
9. pdf_processor valida que contenga ID de reserva y agencia
   ↓
10. Estado actualiza a "recibida" → Ciclo completado ✅
```

---

## 🐛 Problemas Resueltos en Esta Sesión

### 1. ❌ Emails marcados como leídos antes de ser procesados
**Problema**:
- `imap_wrapper.py` usaba `RFC822` que marca automáticamente los emails como leídos
- ReservaMonitor leía el email → Gmail lo marcaba como leído
- OCMonitor no encontraba el email porque ya estaba marcado como leído

**Solución**: `imap_wrapper.py:165`
```python
# ANTES (marcaba como leído):
status, data = self.client.fetch(str(message_id), '(RFC822)')

# DESPUÉS (usa PEEK para no marcar como leído):
status, data = self.client.fetch(str(message_id), '(BODY.PEEK[])')
```

**Resultado**: ✅ Los emails permanecen como no leídos hasta que el monitor correcto los procese

---

### 2. ❌ Filtros de asunto no implementados
**Problema**:
- ReservaMonitor y OCMonitor procesaban TODOS los emails
- Ambos monitores competían por los mismos mensajes
- OC se procesaba como confirmación de reserva

**Solución**: Implementados filtros en `email_monitor.py`

**ReservaMonitor** (`lines 191-195`):
```python
subject = email_data['subject'].lower()
if 'confirmación' not in subject and 'confirmacion' not in subject and 'confirmation' not in subject:
    self.logger.debug(f"Correo no es confirmación de reserva: {email_data['subject']}")
    continue
```

**OCMonitor** (`lines 342-345`):
```python
subject = email_data['subject'].lower()
if not any(keyword in subject for keyword in ['orden de compra', 'oc', 'purchase order', 'orden compra']):
    self.logger.debug(f"Correo no es orden de compra: {email_data['subject']}")
    continue
```

**Resultado**: ✅ Cada monitor solo procesa los emails que le corresponden

---

### 3. ❌ Estructura del repositorio desorganizada
**Problema**:
- Archivos mezclados en raíz
- Tests, scripts, docs sin organización
- Difícil navegación y mantenimiento

**Solución**: Reorganización completa del repositorio
```
Antes:                          Después:
├── *.py (mezclados)           ├── src/ (código fuente)
├── *.md (dispersos)           ├── tests/ (testing)
├── *.sh (scripts)             ├── scripts/ (utilidades)
├── archivos de prueba         ├── docs/ (documentación organizada)
└── ...                        ├── api/postman/ (colecciones API)
                               ├── data/ (BD y archivos)
                               └── n8n/workflows/ (workflows)
```

**Archivos actualizados**:
- ✅ Imports corregidos: `from src.module import Class`
- ✅ Rutas de BD actualizadas: `data/oc_seguimiento.db`
- ✅ Rutas de PDF actualizadas: `data/resumen del servicio.pdf`
- ✅ `.gitignore` actualizado

**Resultado**: ✅ Estructura profesional, escalable y mantenible

---

## 🔧 Configuración Actual

### Variables de Entorno Críticas (.env)

```bash
# IMAP - Monitoreo de confirmaciones
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=cuchohbk@gmail.com
IMAP_PASSWORD=<contraseña de aplicación>
IMAP_MAILBOX=INBOX
IMAP_CHECK_INTERVAL=300  # 5 minutos

# SMTP - Envío de correos
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=cuchohbk@gmail.com
SMTP_PASSWORD=<contraseña de aplicación>
SMTP_FROM_EMAIL=cuchohbk@gmail.com

# OC - Recepción de órdenes de compra (mismo buzón)
OC_INBOX_HOST=imap.gmail.com
OC_INBOX_USERNAME=cuchohbk@gmail.com
OC_INBOX_PASSWORD=<contraseña de aplicación>
OC_CHECK_INTERVAL=300  # 5 minutos

# Base de datos
DATABASE_URL=sqlite:///./data/oc_seguimiento.db

# Agencias que requieren OC
AGENCIES_REQUIRING_OC=WALVIS S.A.,EMPRESA CORPORATIVA LTDA,AGENCIA VIAJES XYZ
```

### Base de Datos (SQLite)

**Ubicación**: `data/oc_seguimiento.db`

**Tablas principales**:
1. `reservas` - Reservas hoteleras
2. `ordenes_compra` - OC recibidas
3. `correos_enviados` - Historial de correos
4. `configuracion_clientes` - Configuración por agencia
5. `log_sistema` - Logs de eventos

**Estados de OC**:
- `PENDIENTE`: Esperando OC del cliente
- `RECIBIDA`: OC recibida y validada
- `EXPIRADA`: Pasó límite de tiempo

---

## 🧪 Testing

### Scripts de Prueba Disponibles

```bash
# Test de flujo completo (E2E)
cd tests
python3 test_flujo_completo.py

# Test de procesamiento PDF
python3 test_pdf.py

# Test de conexión IMAP
python3 test_imap.py

# Verificar instalación
python3 verify_install.py
```

### Scripts de Utilidad

```bash
# Enviar email de prueba
cd scripts
python3 enviar_prueba.py

# Verificar buzón IMAP
python3 verificar_emails.py

# Diagnóstico de problemas IMAP
python3 diagnose_imap.py

# Marcar email como no leído
python3 marcar_no_leido.py
```

---

## 📊 Datos de Prueba

### Email de Confirmación de Reserva
**Asunto**: Debe contener "confirmación", "confirmacion" o "confirmation"
**Ejemplo**: `"Confirmación de Reserva Hotel - ID 45215412"`
**Adjunto**: PDF con datos de reserva
**Destinatario**: cuchohbk@gmail.com

### Email de Orden de Compra
**Asunto**: Debe contener "orden de compra", "oc", "purchase order" o "orden compra"
**Ejemplo**: `"Orden de Compra - Reserva ID 45215412 - LOC AAFTTAT"`
**Adjunto**: PDF con ID de reserva y agencia
**Destinatario**: cuchohbk@gmail.com

### PDF de Ejemplo
**Ubicación**: `data/resumen del servicio.pdf`
**Datos contenidos**:
- ID Reserva: 45215412
- LOC Interno: AAFTTAT
- Agencia: WALVIS S.A.
- Monto: CLP 528,701

---

## 🚀 Comandos Frecuentes

### Iniciar el Sistema
```bash
# Servidor principal
python3 app.py

# Dashboard web
open http://localhost:8001/

# API Docs (Swagger)
open http://localhost:8001/docs
```

### Verificar Estado
```bash
# Health check
curl http://localhost:8001/api/health

# Estadísticas
curl http://localhost:8001/api/stats

# Listar reservas
curl http://localhost:8001/api/reservas

# Ver reserva específica
curl http://localhost:8001/api/reservas/1
```

### Depuración
```bash
# Ver logs en tiempo real
tail -f logs/oc_seguimiento_*.log

# Verificar emails no leídos
python3 scripts/verificar_emails.py

# Test de extracción PDF
python3 tests/test_pdf.py
```

---

## 🔐 Seguridad

### Contraseñas de Aplicación Gmail
- ✅ Configuradas para IMAP y SMTP
- ✅ Almacenadas en `.env` (no versionado)
- ⚠️ Nunca compartir o hacer commit de `.env`

### Archivos Sensibles
- `.env` - Credenciales (NUNCA commitear)
- `data/*.db` - Base de datos con datos reales
- `logs/*.log` - Pueden contener información sensible

---

## 📝 Decisiones Técnicas Importantes

### 1. ¿Por qué BODY.PEEK[] en lugar de RFC822?
**RFC822** marca automáticamente los mensajes como leídos al obtenerlos. Con dos monitores (ReservaMonitor y OCMonitor) revisando el mismo buzón, el primero en leer un email lo marcaba como leído, impidiendo que el segundo monitor lo detectara.

**BODY.PEEK[]** permite leer el contenido sin marcar como leído. Así, ambos monitores pueden ver todos los emails y filtrar por asunto.

### 2. ¿Por qué filtrar por asunto en lugar de por remitente?
Los hoteles pueden enviar desde diferentes dominios. Es más confiable filtrar por palabras clave en el asunto que pueden controlarse.

### 3. ¿Por qué SQLite y no PostgreSQL?
Para desarrollo y despliegue inicial, SQLite es suficiente. Es fácil de backupear, no requiere servidor adicional, y puede migrar a PostgreSQL si el volumen crece.

### 4. ¿Por qué monitoreo cada 5 minutos?
Balance entre:
- Responsividad (detectar emails rápido)
- Carga del servidor de Gmail
- Consumo de recursos

Se puede ajustar con `IMAP_CHECK_INTERVAL` en `.env`.

---

## 🎯 Próximos Pasos Sugeridos

### Corto Plazo
1. [ ] Completar test de flujo E2E con servidor corriendo
2. [ ] Verificar que los recordatorios automáticos funcionan
3. [ ] Testear con emails reales de hoteles

### Mediano Plazo
1. [ ] Implementar autenticación en dashboard web
2. [ ] Agregar notificaciones Slack/email para eventos críticos
3. [ ] Mejorar templates de email con diseño profesional

### Largo Plazo
1. [ ] Desplegar en Google Cloud Platform
2. [ ] Migrar a PostgreSQL si el volumen lo requiere
3. [ ] Implementar API webhooks para integraciones

---

## 📚 Documentación de Referencia

### Archivos Clave de Documentación
- `README.md` - Documentación principal
- `ESTRUCTURA.md` - Organización del repositorio
- `docs/inicio-rapido/` - Guías de inicio
- `docs/troubleshooting/` - Solución de problemas
- `api/postman/POSTMAN_SETUP.md` - Configuración de API testing

### Logs de Cambios
- Ver commits en Git para historial completo
- Búsqueda en logs: `grep "ERROR\|WARNING" logs/*.log`

---

## 🤝 Retomar el Trabajo

### Al volver a trabajar en el proyecto:

1. **Revisar este archivo** para recordar el contexto
2. **Verificar configuración**: `python3 config.py`
3. **Actualizar dependencias**: `pip install -r requirements.txt`
4. **Verificar base de datos**: Backup si tiene datos importantes
5. **Iniciar servidor**: `python3 app.py`
6. **Revisar logs**: `tail -f logs/oc_seguimiento_*.log`

### Preguntas clave a responder:
- ✅ ¿El servidor arranca sin errores?
- ✅ ¿Los monitores IMAP conectan correctamente?
- ✅ ¿El SMTP puede enviar correos?
- ✅ ¿Los filtros de asunto funcionan?
- ✅ ¿El procesamiento de PDF extrae datos correctamente?

---

## 💡 Notas Técnicas

### Intervalos de Chequeo
- ReservaMonitor: cada 5 minutos (300 seg)
- OCMonitor: cada 5 minutos (300 seg)
- Scheduler de recordatorios: 4 veces al día

### Timeouts Importantes
- IMAP connection timeout: 30 segundos
- SMTP send timeout: 30 segundos
- API request timeout: 60 segundos

### Límites Conocidos
- Gmail IMAP: ~450 requests/día con conexión persistente
- SQLite: Hasta ~100K transacciones/día sin problemas
- PDF processing: Archivos hasta 10MB

---

**Fin del contexto - Versión 2025-11-16**

Para actualizar este archivo en el futuro:
```bash
# Editar manualmente o regenerar con IA
vim CONTEXTO_PROYECTO.md
```

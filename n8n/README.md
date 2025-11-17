# 🤖 Sistema de Seguimiento de OC - Solución n8n

## 📁 Contenido de esta Carpeta

Esta carpeta contiene la implementación completa del Sistema de Seguimiento de Órdenes de Compra usando **n8n** (plataforma de automatización visual).

### Archivos Incluidos:

```
n8n/
├── README.md                              # Este archivo
├── README_INSTALACION_N8N.md             # Guía completa de instalación
├── GUIA_CONFIGURACION_SISTEMA.md         # Configuración detallada
├── workflow_monitoreo_reservas.json      # Workflow 1: Detectar reservas
├── workflow_recordatorios.json           # Workflow 2: Enviar recordatorios
└── workflow_deteccion_oc.json            # Workflow 3: Detectar OC recibidas
```

---

## 🎯 ¿Qué es esta solución?

Esta es una **alternativa visual y sin código** al sistema Python/FastAPI desarrollado en el directorio principal.

### Comparación:

| Característica | Sistema Python | Sistema n8n |
|----------------|----------------|-------------|
| **Complejidad** | Requiere programación | Visual, sin código |
| **Instalación** | pip install, Python 3.14 | Docker o npm install |
| **Modificaciones** | Editar código | Arrastrar y soltar nodos |
| **Debugging** | Leer logs en archivos | Ver datos en cada paso visualmente |
| **Mantenimiento** | Manual | Más simple |
| **Ideal para** | Desarrolladores | Equipos mixtos (técnicos y no técnicos) |

---

## 🚀 Inicio Rápido

### Opción 1: Instalación Rápida (5 minutos)

```bash
# 1. Instalar n8n
npm install -g n8n

# 2. Iniciar n8n
n8n start

# 3. Abrir navegador
# http://localhost:5678

# 4. Importar workflows
# Arrastra cada archivo .json a la interfaz de n8n
```

### Opción 2: Instalación con Docker (Recomendado)

```bash
# 1. Crear directorio
mkdir ~/n8n-oc-system
cd ~/n8n-oc-system

# 2. Copiar docker-compose.yml desde README_INSTALACION_N8N.md

# 3. Iniciar
docker-compose up -d

# 4. Abrir navegador
# http://localhost:5678
```

---

## 📚 Documentación

### 1. **[README_INSTALACION_N8N.md](./README_INSTALACION_N8N.md)**

Guía completa de instalación que cubre:
- ✅ Instalación de n8n (npm, Docker, Docker Compose)
- ✅ Configuración de PostgreSQL
- ✅ Importar workflows
- ✅ Configurar credenciales (Gmail, PostgreSQL)
- ✅ Despliegue en producción
- ✅ Configurar HTTPS
- ✅ Backups y mantenimiento

**Leer primero si:** Aún no tienes n8n instalado.

### 2. **[GUIA_CONFIGURACION_SISTEMA.md](./GUIA_CONFIGURACION_SISTEMA.md)**

Guía detallada de configuración que cubre:
- ✅ Explicación de cada workflow
- ✅ Configuración de nodos
- ✅ Personalización de correos HTML
- ✅ Ajuste de intervalos de ejecución
- ✅ Solución de problemas comunes
- ✅ Monitoreo y debugging
- ✅ Escalabilidad

**Leer primero si:** Ya tienes n8n instalado y quieres configurar el sistema.

---

## 🔄 Workflows Incluidos

### 1. **Monitoreo de Reservas** (`workflow_monitoreo_reservas.json`)

**Función:** Detecta correos con PDFs de reservas, extrae datos y solicita OC.

**Flujo:**
```
Trigger (cada 1 min)
  ↓
Leer IMAP (correos no leídos)
  ↓
Filtrar: tiene adjuntos?
  ↓
Dividir adjuntos
  ↓
Filtrar: es PDF?
  ↓
Extraer texto del PDF
  ↓
Parsear datos (regex)
  ↓
Validar datos
  ↓
Verificar si requiere OC
  ↓
Guardar en PostgreSQL
  ↓
SI requiere OC:
  ├─ Construir correo HTML
  ├─ Enviar correo de solicitud
  └─ Registrar envío
```

### 2. **Recordatorios** (`workflow_recordatorios.json`)

**Función:** Envía recordatorios escalados para OC pendientes.

**Flujo:**
```
Trigger (cada 6 horas)
  ↓
Query: Buscar OC pendientes
  ↓
Determinar tipo de correo (día 2 o día 4)
  ↓
Construir correo (recordatorio o ultimátum)
  ↓
Enviar correo
  ↓
Registrar envío
  ↓
SI es día 4+ y no hay respuesta:
  └─ Marcar como EXPIRADA
```

### 3. **Detección de OC** (`workflow_deteccion_oc.json`)

**Función:** Detecta cuando se recibe una OC y detiene recordatorios.

**Flujo:**
```
Trigger (cada 2 min)
  ↓
Leer correos en inbox OC
  ↓
Filtrar: tiene adjuntos?
  ↓
Extraer ID/LOC del correo
  ↓
Buscar reserva en DB
  ↓
SI encontró reserva:
  ├─ Guardar PDF de OC
  ├─ Registrar OC en DB
  ├─ Actualizar estado → RECIBIDA
  ├─ Construir confirmación
  └─ Enviar email de confirmación
```

---

## ⚙️ Configuración Mínima Requerida

### 1. Credenciales

Necesitas configurar en n8n:

- **Gmail OAuth2 (IMAP)** - Para leer correos de reservas
- **Gmail OAuth2 (SMTP)** - Para enviar correos
- **Gmail OAuth2 (OC Inbox)** - Para recibir OC (puede ser la misma cuenta)
- **PostgreSQL** - Base de datos

### 2. Base de Datos

Ejecutar el schema SQL para crear tablas:
- `reservas`
- `correos_enviados`
- `ordenes_compra`

(Ver `README_INSTALACION_N8N.md` para SQL completo)

### 3. Personalización

**Mínima personalización requerida:**

1. **Lista de agencias con OC** (en workflow_monitoreo_reservas.json):
   ```javascript
   const agenciasConOC = [
     'CODELCO',
     'ENAP',
     // AGREGAR TUS CLIENTES AQUÍ
   ];
   ```

2. **Email para recibir OC** (en workflow_deteccion_oc.json):
   ```yaml
   Filtros: "to:TU_EMAIL@dominio.com"
   ```

3. **Patrones regex** (si tus PDFs tienen formato diferente):
   ```javascript
   id_reserva: extractField(/ID:\s*(\d+)/i, text)
   // Ajustar regex según tu formato
   ```

---

## 🎬 Primeros Pasos (Checklist)

- [ ] 1. Instalar n8n (npm o Docker)
- [ ] 2. Crear base de datos PostgreSQL
- [ ] 3. Ejecutar SQL para crear tablas
- [ ] 4. Importar los 3 workflows a n8n
- [ ] 5. Configurar credencial: Gmail IMAP OAuth2
- [ ] 6. Configurar credencial: Gmail SMTP OAuth2
- [ ] 7. Configurar credencial: PostgreSQL
- [ ] 8. Asignar credenciales a cada nodo
- [ ] 9. Personalizar lista de agencias con OC
- [ ] 10. Personalizar email de recepción OC
- [ ] 11. Activar Workflow 1: Monitoreo de Reservas
- [ ] 12. Activar Workflow 2: Recordatorios
- [ ] 13. Activar Workflow 3: Detección de OC
- [ ] 14. Enviar correo de prueba con PDF
- [ ] 15. Verificar ejecución en n8n (Executions)
- [ ] 16. Verificar registro en base de datos

---

## 🧪 Testing

### Test 1: Enviar Reserva de Prueba

```bash
# Opción A: Usar script Python
cd ..  # Volver al directorio principal
python enviar_prueba.py

# Opción B: Enviar correo manual
# 1. Crea un correo con un PDF adjunto
# 2. Incluye en el PDF: ID, LOC Interno, Agencia, Hotel, etc.
# 3. Envíalo a la cuenta Gmail configurada para IMAP
```

### Test 2: Verificar Detección

1. Ve a n8n: http://localhost:5678
2. Click en **Executions** (menú izquierdo)
3. Deberías ver una ejecución de "Monitoreo de Reservas"
4. Click en la ejecución para ver detalles
5. Revisa cada nodo:
   - ✅ "Leer Correos IMAP" debe mostrar el correo
   - ✅ "Es PDF?" debe detectar el PDF
   - ✅ "Parsear Datos" debe extraer campos
   - ✅ "Guardar en DB" debe tener resultado exitoso

### Test 3: Verificar Base de Datos

```sql
-- Conectar a PostgreSQL
psql -U n8n -d reservas_oc

-- Ver reservas creadas
SELECT id_reserva, agencia, nombre_hotel, requiere_oc, estado_oc
FROM reservas
ORDER BY fecha_creacion DESC
LIMIT 5;

-- Ver correos enviados
SELECT r.id_reserva, ce.tipo_correo, ce.destinatario, ce.fecha_envio
FROM correos_enviados ce
JOIN reservas r ON ce.reserva_id = r.id
ORDER BY ce.fecha_envio DESC
LIMIT 5;
```

### Test 4: Probar OC

1. Responde al correo de solicitud OC
2. Adjunta un PDF (cualquiera)
3. En el asunto o cuerpo incluye: "ID: [el_id_de_tu_reserva]"
4. Espera 2 minutos (intervalo del workflow)
5. Verifica en n8n → Executions → "Detección de OC"
6. Verifica en DB:

```sql
SELECT * FROM reservas WHERE estado_oc = 'RECIBIDA';
SELECT * FROM ordenes_compra;
```

---

## 🔍 Debugging

### Ver Logs en Tiempo Real

**Con npm:**
```bash
# Los logs aparecen en la consola donde ejecutaste n8n
```

**Con Docker:**
```bash
docker-compose logs -f n8n
```

### Solución de Problemas Comunes

#### ❌ "No se ejecuta el workflow"

**Solución:**
- Verifica que el workflow esté **Active** (toggle ON)
- Revisa el trigger (Schedule debe tener intervalo configurado)
- Check logs para errores

#### ❌ "No detecta correos"

**Solución:**
- Verifica credenciales de Gmail
- Asegúrate de que hay correos NO LEÍDOS
- Test conexión IMAP manualmente
- Revisa filtros en el nodo IMAP

#### ❌ "Error en base de datos"

**Solución:**
- Test credencial de PostgreSQL en n8n
- Verifica que las tablas existen
- Revisa el query SQL por errores de sintaxis

---

## 📊 Monitoreo en Producción

### Dashboard de n8n

Accede a: **http://tu-servidor:5678**

En el dashboard puedes:
- ✅ Ver ejecuciones en tiempo real
- ✅ Filtrar por workflow
- ✅ Identificar errores rápidamente
- ✅ Ver throughput (ejecuciones por día)
- ✅ Pausar/reanudar workflows

### Alertas (Opcional)

Crea un workflow adicional:

```yaml
Trigger: Webhook (POST request)
  ↓
Cuando hay error en algún workflow
  ↓
Enviar email a admin@dominio.com
  ↓
O enviar a Slack/Discord/Telegram
```

---

## 🚀 Próximos Pasos

### 1. Sistema Funcionando

Si ya tienes todo funcionando:
- ✅ Lee `GUIA_CONFIGURACION_SISTEMA.md` para personalizaciones avanzadas
- ✅ Configura HTTPS si está en producción
- ✅ Implementa backups automáticos
- ✅ Crea workflow de reportes diarios

### 2. Migrar desde Python

Si vienes del sistema Python:
- ✅ Ambos sistemas pueden correr en paralelo
- ✅ Usa la misma base de datos PostgreSQL
- ✅ Migra workflow por workflow
- ✅ Prueba exhaustivamente antes de apagar Python

### 3. Extender Funcionalidad

Ideas de extensión:
- ✅ Dashboard web personalizado (conectar n8n API)
- ✅ Notificaciones por Slack/Telegram
- ✅ Integración con CRM
- ✅ Reportes automáticos por email
- ✅ Webhooks para eventos en tiempo real

---

## 📞 Ayuda y Soporte

### Documentación

- **n8n Oficial:** https://docs.n8n.io
- **Comunidad n8n:** https://community.n8n.io
- **Este Proyecto:**
  - `README_INSTALACION_N8N.md` - Instalación completa
  - `GUIA_CONFIGURACION_SISTEMA.md` - Configuración detallada

### Recursos

- [Tutoriales n8n](https://docs.n8n.io/courses/)
- [Workflows de ejemplo](https://n8n.io/workflows)
- [Discord n8n](https://discord.gg/n8n)

### Errores Comunes

Ver sección "🚨 Solución de Problemas Comunes" en `GUIA_CONFIGURACION_SISTEMA.md`

---

## 📜 Licencia

Este sistema es de código abierto. n8n se distribuye bajo licencia Apache 2.0.

---

## ✅ Ventajas de n8n para este Proyecto

1. **Visual y Accesible** - Cualquiera puede entender el flujo
2. **Sin Código** - No necesitas ser programador para modificar
3. **Debugging Fácil** - Ves datos en cada paso
4. **Escalable** - Agrega workers fácilmente
5. **Comunidad Activa** - Miles de workflows de ejemplo
6. **Gratis** - 100% gratuito si auto-hospedas
7. **Integrado** - 300+ integraciones pre-built
8. **Mantenible** - Cambios sin tocar código

---

**¿Listo para empezar?**

👉 **[Ir a Instalación](./README_INSTALACION_N8N.md)**

👉 **[Ir a Configuración](./GUIA_CONFIGURACION_SISTEMA.md)**

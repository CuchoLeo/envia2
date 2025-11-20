# 📖 Guía de Configuración del Sistema de OC en n8n

## 🎯 Resumen del Sistema

Este sistema automatiza completamente el seguimiento de Órdenes de Compra (OC) para reservas hoteleras corporativas usando n8n.

### Componentes del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO COMPLETO DEL SISTEMA               │
└─────────────────────────────────────────────────────────────┘

1. 📧 MONITOREO DE RESERVAS
   ├─ Lee correos IMAP cada 1 minuto
   ├─ Detecta PDFs adjuntos
   ├─ Extrae datos con regex
   ├─ Guarda en PostgreSQL
   └─ Envía solicitud OC (si requiere)

2. ⏰ RECORDATORIOS PROGRAMADOS
   ├─ Ejecuta cada 6 horas
   ├─ Busca OC pendientes
   ├─ Día 2: Recordatorio amigable
   ├─ Día 4: Ultimátum
   └─ Día 5+: Marca como expirada

3. ✅ DETECCIÓN DE OC RECIBIDAS
   ├─ Monitorea inbox de OC cada 2 minutos
   ├─ Identifica reserva por ID/LOC
   ├─ Guarda PDF de OC
   ├─ Actualiza estado a RECIBIDA
   └─ Envía confirmación
```

---

## 🔧 Configuración Detallada de Workflows

### Workflow 1: Monitoreo de Reservas

**Archivo:** `workflow_monitoreo_reservas.json`

#### Nodos y Configuración:

**1. Trigger: Cada 1 Minuto**
```yaml
Tipo: Schedule Trigger
Intervalo: 1 minuto
Configuración:
  - Para desarrollo: 1 minuto
  - Para producción: 2-5 minutos (reduce carga)
```

**2. Leer Correos IMAP**
```yaml
Tipo: Email Read IMAP
Credencial: Gmail IMAP OAuth2
Filtros:
  - seen:false (solo no leídos)
Opciones:
  - downloadAttachments: true
  - attachmentsPrefix: "attachment_"
```

**3. Filtro: Tiene Adjuntos?**
```yaml
Tipo: IF Node
Condición: $json.attachments.length > 0
```

**4. Dividir Adjuntos**
```yaml
Tipo: Item Lists
Operación: Split
Campo: attachments
```

**5. Filtro: Es PDF?**
```yaml
Tipo: IF Node
Condición: $json.attachment.mimeType == "application/pdf"
```

**6. Extraer Texto de PDF**
```yaml
Tipo: PDF Node
Operación: Extract Text
Binary Property: attachment
```

**7. Parsear Datos del PDF (CODE NODE)**

Este es el nodo más importante. Extrae los datos del PDF:

```javascript
const text = $input.item.json.text || '';

// Patrones regex para extraer campos
const data = {
  id_reserva: extractField(/ID:\s*(\d+)/i, text),
  loc_interno: extractField(/LOC\s+Interno:\s*([A-Z0-9]+)/i, text),
  agencia: extractField(/Agencia:\s*([^\n]+)/i, text),
  nombre_hotel: extractField(/Hotel:\s*([^\n]+)/i, text),
  // ... más campos
};
```

**Personalización:** Ajusta los patrones regex según el formato de tus PDFs.

**8. Validar Datos**
```yaml
Tipo: IF Node
Condición: $json.valido == true
```

**9. Verificar si Requiere OC (CODE NODE)**

Lista de agencias que requieren OC:

```javascript
const agenciasConOC = [
  'CODELCO',
  'ENAP',
  'BANCO DE CHILE',
  // ... agregar más
];
```

**⚠️ IMPORTANTE:** Edita esta lista según tus clientes corporativos.

**10. Guardar en DB**
```yaml
Tipo: PostgreSQL
Operación: Execute Query
Query: INSERT INTO reservas (...)
On Conflict: DO NOTHING (evita duplicados)
```

**11. Construir y Enviar Correo**

Si requiere OC, construye HTML y envía email de solicitud.

---

### Workflow 2: Recordatorios Programados

**Archivo:** `workflow_recordatorios.json`

#### Lógica de Recordatorios:

```
Día 0 ────► Solicitud Inicial (enviada por Workflow 1)

Día 2 ────► Recordatorio Amigable
    │       "Le recordamos que hace 2 días..."
    │
Día 4 ────► Ultimátum
    │       "🚨 ÚLTIMO AVISO - Consecuencias de no enviar..."
    │
Día 5+ ───► Estado: EXPIRADA
            Se detienen los recordatorios
```

#### Configuración de Intervalos:

**Nodo: Cada 6 Horas**
```yaml
Tipo: Schedule Trigger
Intervalo: 6 horas

Opciones para producción:
  - Cada 12 horas: 08:00 y 20:00
  - Cada día: 09:00 (solo días laborables)
```

**Query SQL - Buscar Pendientes:**
```sql
SELECT
  r.*,
  EXTRACT(DAY FROM (NOW() - r.fecha_creacion)) as dias_desde_creacion,
  ce.tipo_correo as ultimo_correo_enviado
FROM reservas r
LEFT JOIN LATERAL (
  SELECT tipo_correo
  FROM correos_enviados
  WHERE reserva_id = r.id
  ORDER BY fecha_envio DESC
  LIMIT 1
) ce ON true
WHERE
  r.requiere_oc = true
  AND r.estado_oc = 'PENDIENTE'
  AND r.fecha_checkin > NOW()
ORDER BY r.fecha_creacion ASC;
```

#### Personalizar Correos:

**Nodo: Construir Correo Recordatorio (CODE)**

Puedes modificar:
- Colores del header
- Texto de los mensajes
- Estructura HTML
- Información mostrada

**Ejemplo - Cambiar color del header:**
```javascript
// Recordatorio Día 2
.header {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

// Ultimátum Día 4
.header {
  background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
}
```

---

### Workflow 3: Detección de OC Recibidas

**Archivo:** `workflow_deteccion_oc.json`

#### Configuración del Inbox de OC:

**Nodo: Leer Correos OC**
```yaml
Tipo: Email Read IMAP
Credencial: Gmail OC Inbox OAuth2  # Cuenta separada
Filtros:
  - seen:false
  - to:oc@kontroltravel.com  # ⚠️ CAMBIAR a tu email
Opciones:
  - downloadAttachments: true
  - attachmentsPrefix: "oc_"
```

**⚠️ IMPORTANTE:** Cambia `oc@kontroltravel.com` por tu email real.

#### Búsqueda de Reserva:

**Nodo: Extraer Info de Reserva (CODE)**

Busca ID o LOC en asunto y cuerpo del correo:

```javascript
const searchText = `${subject} ${body}`;

// Buscar patrones
const idMatch = searchText.match(/ID[:\s]*(\d+)/i);
const locMatch = searchText.match(/LOC[:\s]+([A-Z0-9]+)/i);
```

**Formatos aceptados:**
- "ID: 12345"
- "ID:12345"
- "Reserva ID 12345"
- "LOC: ABC123"
- "LOC INTERNO: ABC123"

**Query de Búsqueda:**
```sql
SELECT * FROM reservas
WHERE
  estado_oc = 'PENDIENTE'
  AND requiere_oc = true
  AND (
    id_reserva = '{{ ID_ENCONTRADO }}'
    OR loc_interno = '{{ LOC_ENCONTRADO }}'
  )
LIMIT 1;
```

#### Guardar Archivo OC:

**Nodo: Guardar Archivo OC**
```yaml
Tipo: Write Binary File
Ruta: /oc_files/{{ $json.id_reserva }}_{{ $json.attachment.fileName }}
```

**⚠️ CONFIGURAR:** Asegúrate de que la carpeta `/oc_files/` existe y tiene permisos de escritura.

```bash
# Crear carpeta
mkdir -p ~/oc_files
chmod 755 ~/oc_files

# Si usas Docker, montar volumen en docker-compose.yml:
volumes:
  - ./oc_files:/home/node/oc_files
```

---

## 🎨 Personalización de Correos HTML

### Estructura de un Correo:

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* Estilos CSS inline para compatibilidad con clientes de correo */
    body { font-family: Arial, sans-serif; }
    .header { background: gradient; color: white; }
    .content { background: #f9f9f9; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Título</h1>
    </div>
    <div class="content">
      <p>Contenido...</p>
    </div>
  </div>
</body>
</html>
```

### Colores Recomendados:

```css
/* Solicitud Inicial (profesional, neutro) */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Recordatorio Día 2 (amigable, cálido) */
background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);

/* Ultimátum Día 4 (urgente, alerta) */
background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);

/* OC Recibida (éxito, positivo) */
background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
```

### Modificar Correos en n8n:

1. Abre el workflow
2. Click en nodo "Construir Correo..."
3. Click en "Edit Code"
4. Modifica la variable `html`
5. Test ejecutando el workflow manualmente
6. Save

---

## 🔍 Monitoreo y Debugging

### Ver Ejecuciones:

1. **Executions** (menú izquierdo)
2. Filtra por workflow
3. Click en una ejecución para ver:
   - ✅ Éxito o ❌ Fallo
   - Datos en cada nodo
   - Tiempo de ejecución
   - Errores (si los hay)

### Debugging Paso a Paso:

1. Abre el workflow
2. Click en "Execute Workflow" (botón play)
3. Observa cómo fluyen los datos
4. Click en cada nodo para ver output
5. Si falla, revisa el nodo en rojo

### Logs Útiles:

**Ver errores de PostgreSQL:**
```sql
-- Desde psql
SELECT * FROM pg_stat_activity WHERE datname = 'reservas_oc';
```

**Ver últimas ejecuciones desde CLI:**
```bash
# Si usas Docker
docker-compose logs n8n | tail -100

# Filtrar errores
docker-compose logs n8n | grep ERROR
```

---

## ⚙️ Configuración Avanzada

### Webhook Triggers (Opcional)

En lugar de polling cada N minutos, puedes usar webhooks:

**Beneficio:** Ejecución instantánea al recibir correo.

**Configuración:**
1. Reemplaza "Schedule Trigger" por "Webhook Trigger"
2. Configura Gmail para enviar webhook en correo nuevo
3. Requiere Gmail API o servicio de terceros (ej: Zapier hook)

### Variables de Entorno

Si usas Docker, puedes configurar variables:

```yaml
# En docker-compose.yml
environment:
  - TIMEZONE=America/Santiago
  - N8N_BASIC_AUTH_ACTIVE=true
  - N8N_BASIC_AUTH_USER=admin
  - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
  - EXECUTIONS_DATA_SAVE_ON_SUCCESS=all
  - EXECUTIONS_DATA_SAVE_ON_ERROR=all
```

### Escalabilidad

Para alto volumen de correos:

```yaml
# docker-compose.yml - añadir workers
services:
  n8n-worker-1:
    image: n8nio/n8n
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
    depends_on:
      - redis

  redis:
    image: redis:alpine
```

---

## 📊 Dashboard y Reportes

### Crear Workflow de Reportes

**Nuevo Workflow:** Reporte Diario

```yaml
Trigger: Cron (cada día a las 08:00)
  ↓
Query PostgreSQL: Estadísticas del día anterior
  ↓
Construir Email con Resumen:
  - X reservas procesadas
  - Y OC recibidas
  - Z pendientes
  ↓
Enviar a: admin@kontroltravel.com
```

### Query de Estadísticas:

```sql
-- Reservas por agencia (últimos 30 días)
SELECT
  agencia,
  COUNT(*) as total_reservas,
  SUM(CASE WHEN estado_oc = 'RECIBIDA' THEN 1 ELSE 0 END) as oc_recibidas,
  SUM(CASE WHEN estado_oc = 'PENDIENTE' THEN 1 ELSE 0 END) as oc_pendientes,
  SUM(monto_total) as monto_total
FROM reservas
WHERE fecha_creacion > NOW() - INTERVAL '30 days'
GROUP BY agencia
ORDER BY total_reservas DESC;
```

---

## 🚨 Solución de Problemas Comunes

### 1. Workflow no se ejecuta

**Síntomas:** No aparecen ejecuciones nuevas.

**Soluciones:**
- ✅ Verifica que el workflow esté **Active** (toggle en ON)
- ✅ Revisa el trigger (Schedule debe estar bien configurado)
- ✅ Check logs: `docker-compose logs n8n`

### 2. No se detectan correos

**Síntomas:** Ejecuciones exitosas pero sin correos procesados.

**Soluciones:**
- ✅ Verifica credenciales de Gmail (Settings → Credentials)
- ✅ Confirma que hay correos NO LEÍDOS en INBOX
- ✅ Prueba conexión IMAP manualmente
- ✅ Revisa filtros del nodo IMAP ("seen:false")

### 3. Error al guardar en DB

**Síntomas:** Falla en nodo PostgreSQL.

**Soluciones:**
- ✅ Verifica credenciales de PostgreSQL
- ✅ Confirma que la tabla existe
- ✅ Revisa query SQL (sintaxis correcta)
- ✅ Test conexión desde Settings → Credentials

### 4. Correos no se envían

**Síntomas:** Workflow completa pero no llegan correos.

**Soluciones:**
- ✅ Verifica credenciales de Gmail SMTP
- ✅ Revisa carpeta de SPAM del destinatario
- ✅ Confirma que el email_to es válido
- ✅ Test enviando a tu propio email

### 5. PDF no se puede leer

**Síntomas:** Error en nodo "Extraer Texto de PDF".

**Soluciones:**
- ✅ Verifica que el archivo sea realmente un PDF
- ✅ Algunos PDFs escaneados no tienen texto extraíble
- ✅ Prueba con otro PDF
- ✅ Considera usar OCR si es imagen

---

## 📝 Checklist de Configuración Inicial

- [ ] n8n instalado y funcionando
- [ ] PostgreSQL configurado con tablas creadas
- [ ] Credencial: Gmail IMAP OAuth2 configurada y testeada
- [ ] Credencial: Gmail SMTP OAuth2 configurada y testeada
- [ ] Credencial: PostgreSQL configurada y testeada
- [ ] Workflow 1: Monitoreo de Reservas importado
- [ ] Workflow 1: Credenciales asignadas a cada nodo
- [ ] Workflow 1: Lista de agencias con OC actualizada
- [ ] Workflow 1: Patrones regex ajustados a formato de PDFs
- [ ] Workflow 1: Activado ✅
- [ ] Workflow 2: Recordatorios importado
- [ ] Workflow 2: Intervalo ajustado (cada 6-12 horas)
- [ ] Workflow 2: HTML de correos personalizado
- [ ] Workflow 2: Activado ✅
- [ ] Workflow 3: Detección OC importado
- [ ] Workflow 3: Email de recepción OC configurado
- [ ] Workflow 3: Carpeta /oc_files creada con permisos
- [ ] Workflow 3: Activado ✅
- [ ] Test: Envío de correo con PDF de prueba
- [ ] Test: Detección y procesamiento de reserva
- [ ] Test: Envío de solicitud OC
- [ ] Test: Respuesta con OC y detección
- [ ] Monitoreo: Executions revisadas sin errores

---

## 🎓 Recursos de Aprendizaje

### Tutoriales n8n:
- [Primeros pasos con n8n](https://docs.n8n.io/getting-started/)
- [Crear tu primer workflow](https://docs.n8n.io/courses/level-one/)
- [Trabajar con datos](https://docs.n8n.io/data/)

### Nodos Clave para Este Sistema:
- [Email Read IMAP](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.emailreadimap/)
- [Gmail](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
- [PostgreSQL](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.postgres/)
- [PDF](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.pdf/)
- [Code](https://docs.n8n.io/code-examples/methods-variables-reference/)

### Comunidad:
- [Forum n8n](https://community.n8n.io/)
- [Discord n8n](https://discord.gg/n8n)

---

## 📞 Soporte

**Problemas con n8n:**
- Documentación: https://docs.n8n.io
- Community Forum: https://community.n8n.io
- GitHub Issues: https://github.com/n8n-io/n8n/issues

**Problemas con este sistema:**
- Revisa logs de ejecución en n8n
- Verifica base de datos
- Consulta esta guía
- Revisa `TROUBLESHOOTING.md` del proyecto Python

---

**¡Sistema listo para usar! 🚀**

Siguiente paso: [Ejecutar pruebas completas](#verificación-y-pruebas)

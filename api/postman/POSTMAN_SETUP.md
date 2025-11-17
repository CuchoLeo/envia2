# Configuración de Postman para TravelIA - Sistema de OC

## 📥 Importar la Colección

### Opción 1: Importar archivos (Recomendado)

1. **Abrir Postman**

2. **Importar la colección:**
   - Click en el botón **"Import"** (esquina superior izquierda)
   - Arrastra o selecciona el archivo: `TravelIA_OC_API.postman_collection.json`
   - Click en **"Import"**

3. **Importar el environment:**
   - Click en **"Import"** nuevamente
   - Selecciona el archivo: `TravelIA_Development.postman_environment.json`
   - Click en **"Import"**

4. **Activar el environment:**
   - En la esquina superior derecha, busca el dropdown de environments
   - Selecciona **"TravelIA - Development"**

### Opción 2: Configuración Manual

Si prefieres configurar manualmente:

1. **Crear una nueva colección:**
   - Click en **"New"** → **"Collection"**
   - Nombre: `TravelIA - Sistema de OC`

2. **Crear variable de entorno:**
   - Click en el ícono de engranaje (⚙️) en la esquina superior derecha
   - Click en **"Add"**
   - Nombre: `TravelIA - Development`
   - Agregar variable:
     - **Variable**: `base_url`
     - **Initial Value**: `http://localhost:8001`
     - **Current Value**: `http://localhost:8001`

---

## 🧪 Endpoints Disponibles

### 1. Health Check
**GET** `/api/health`

Verifica que el sistema esté funcionando.

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-16T01:00:00"
}
```

---

### 2. Estadísticas del Sistema
**GET** `/api/stats`

Obtiene estadísticas generales.

**Respuesta esperada:**
```json
{
  "total_reservas": 1,
  "pendientes": 0,
  "recibidas": 1,
  "expiradas": 0
}
```

---

### 3. Listar Reservas
**GET** `/api/reservas`

**Query Parameters:**
- `estado_oc` (opcional): `pendiente` | `recibida` | `expirada`
- `skip` (opcional): Número de registros a saltar (default: 0)
- `limit` (opcional): Número máximo de resultados (default: 100)

**Ejemplo:**
```
GET {{base_url}}/api/reservas?estado_oc=pendiente&limit=10
```

---

### 4. Obtener Reserva por ID
**GET** `/api/reservas/{reserva_id}`

**Ejemplo:**
```
GET {{base_url}}/api/reservas/1
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "id_reserva": "45215412",
  "loc_interno": "AAFTTAT",
  "agencia": "WALVIS S.A.",
  "estado_oc": "recibida",
  "orden_compra": {
    "recibida": true,
    "fecha_recepcion": "2025-11-16T01:54:22.193677"
  }
}
```

---

### 5. Marcar OC como Recibida (Manual)
**POST** `/api/reservas/{reserva_id}/marcar-oc-recibida`

**Body (JSON):**
```json
{
  "numero_oc": "OC-2024-001",
  "observaciones": "OC recibida y validada"
}
```

**Ejemplo:**
```
POST {{base_url}}/api/reservas/1/marcar-oc-recibida
Content-Type: application/json

{
  "numero_oc": "OC-2024-001",
  "observaciones": "Recibida por correo"
}
```

---

### 6. Reenviar Correo
**POST** `/api/reservas/{reserva_id}/reenviar-correo`

**Body (JSON):**
```json
{
  "tipo_correo": "solicitud_inicial"
}
```

**Tipos de correo válidos:**
- `solicitud_inicial`: Primera solicitud de OC
- `recordatorio_1`: Primer recordatorio
- `recordatorio_2`: Segundo recordatorio
- `ultimatum`: Correo de urgencia

**Ejemplo:**
```
POST {{base_url}}/api/reservas/1/reenviar-correo
Content-Type: application/json

{
  "tipo_correo": "recordatorio_1"
}
```

---

### 7. Listar Clientes
**GET** `/api/clientes`

Lista todos los clientes/agencias configurados.

---

### 8. Crear Cliente
**POST** `/api/clientes`

**Body (JSON):**
```json
{
  "nombre_agencia": "NUEVA AGENCIA S.A.",
  "email_contacto": "contacto@nueva-agencia.com",
  "telefono_contacto": "+56912345678",
  "requiere_oc": true,
  "dias_recordatorio_1": 3,
  "dias_recordatorio_2": 5,
  "notas": "Cliente nuevo"
}
```

---

### 9. Procesar Ahora (Forzar)
**POST** `/api/process-now`

Fuerza el procesamiento inmediato de correos pendientes sin esperar al scheduler.

---

## 🎯 Casos de Uso Comunes

### Verificar estado del sistema
1. Health Check → Debe retornar `status: "healthy"`
2. Estadísticas → Ver resumen de reservas

### Consultar una reserva
1. Listar Reservas → Obtener ID de la reserva
2. Obtener Reserva por ID → Ver detalles completos

### Marcar OC manualmente
1. Obtener reserva → Verificar que esté en estado "pendiente"
2. Marcar OC como Recibida → Enviar número de OC y observaciones
3. Obtener reserva nuevamente → Verificar que cambió a "recibida"

### Reenviar correos
1. Obtener reserva → Ver qué correos se han enviado
2. Reenviar Correo → Especificar tipo de correo
3. Verificar en `correos_enviados` que se agregó el nuevo envío

---

## 🔧 Variables de Entorno

La colección usa la variable `{{base_url}}` que se define en el environment.

**Valores por defecto:**
- **Development**: `http://localhost:8001`
- **Production**: Cambiar a tu URL de producción cuando despliegues

Para cambiar de entorno:
1. Click en el dropdown de environments (esquina superior derecha)
2. Selecciona el environment deseado

---

## 📊 Pruebas Rápidas

### Test 1: Sistema funcionando
```
GET {{base_url}}/api/health
```
✅ Debe retornar 200 OK

### Test 2: Ver reservas pendientes
```
GET {{base_url}}/api/reservas?estado_oc=pendiente
```
✅ Debe retornar lista de reservas

### Test 3: Ver detalles de reserva
```
GET {{base_url}}/api/reservas/1
```
✅ Debe retornar objeto con todos los detalles

### Test 4: Forzar procesamiento
```
POST {{base_url}}/api/process-now
```
✅ Debe retornar mensaje de éxito

---

## 🐛 Troubleshooting

### Error: "Could not connect to localhost:8001"
- ✅ Verifica que el servidor esté corriendo: `ps aux | grep "python3 app.py"`
- ✅ Inicia el servidor si es necesario: `python3 app.py`

### Error: 404 Not Found
- ✅ Verifica que la URL sea correcta
- ✅ Confirma que el environment esté activo (esquina superior derecha)

### Error: 422 Unprocessable Entity
- ✅ Revisa que el body JSON esté bien formado
- ✅ Verifica que los campos requeridos estén presentes

---

## 📝 Notas Adicionales

- Todos los endpoints retornan JSON
- Las fechas están en formato ISO 8601
- Los IDs son numéricos (integers)
- El servidor corre por defecto en el puerto **8001**

---

## 🔗 Recursos

- **Documentación interactiva (Swagger)**: http://localhost:8001/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8001/redoc
- **Dashboard web**: http://localhost:8001/

¡Listo para probar! 🚀

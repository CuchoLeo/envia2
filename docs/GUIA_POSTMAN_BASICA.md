# 📮 Guía Básica de Postman - Para Principiantes

**Versión**: 1.0
**Fecha**: 9 de Diciembre de 2024
**Audiencia**: Usuarios sin experiencia técnica

---

## 📋 Índice

1. [¿Qué es Postman y para qué sirve?](#qué-es-postman-y-para-qué-sirve)
2. [Instalación de Postman](#instalación-de-postman)
3. [Conceptos básicos que necesitas saber](#conceptos-básicos-que-necesitas-saber)
4. [Tu primera petición en Postman](#tu-primera-petición-en-postman)
5. [Ejemplos prácticos con el Sistema de OC](#ejemplos-prácticos-con-el-sistema-de-oc)
6. [Solución de problemas comunes](#solución-de-problemas-comunes)
7. [Glosario de términos](#glosario-de-términos)

---

## 1. ¿Qué es Postman y para qué sirve?

### 🤔 Imagina que...

Postman es como el **cartero de internet**. Así como un cartero lleva cartas entre tú y otras personas, Postman lleva mensajes entre tu computadora y el sistema de seguimiento de OC.

### 🎯 ¿Para qué lo usarás?

Con Postman podrás:

✅ **Ver información** del sistema (como ver reservas, clientes, estadísticas)
✅ **Modificar datos** (como marcar una OC como recibida)
✅ **Ejecutar acciones** (como forzar el envío de correos inmediatamente)
✅ **Probar que el sistema funciona** correctamente

### 💡 Analogía sencilla:

```
Sistema de OC = Restaurante
Postman = Tú haciendo un pedido por teléfono
API = El mesero que toma tu pedido

Ejemplo:
Tú (Postman): "Quiero ver todas las reservas pendientes"
Mesero (API): "Aquí están, son 5 reservas"
```

---

## 2. Instalación de Postman

### Paso 1: Descargar Postman

1. Abre tu navegador (Chrome, Firefox, Safari)
2. Ve a: **https://www.postman.com/downloads/**
3. Haz clic en **"Download"** (el botón grande naranja)
4. Espera a que descargue (el archivo es ~200 MB)

### Paso 2: Instalar

**En Mac:**
1. Abre el archivo descargado (Postman-osx.zip)
2. Arrastra el ícono de Postman a la carpeta "Aplicaciones"
3. Haz doble clic en Postman en Aplicaciones
4. Si dice "No se puede abrir porque es de un desarrollador no identificado":
   - Ve a Preferencias del Sistema → Seguridad
   - Haz clic en "Abrir de todas formas"

**En Windows:**
1. Abre el archivo descargado (Postman-win64-Setup.exe)
2. Sigue el asistente de instalación (Siguiente → Siguiente → Instalar)
3. Espera a que termine
4. Postman se abrirá automáticamente

### Paso 3: Crear cuenta (Opcional pero recomendado)

1. Cuando Postman se abra, te preguntará si quieres crear una cuenta
2. Puedes:
   - **Opción A**: Crear cuenta gratis (te permite guardar tu trabajo)
   - **Opción B**: Hacer clic en "Skip for now" (saltar por ahora)

**Recomendación**: Crea una cuenta, es gratis y podrás guardar tus peticiones.

---

## 3. Conceptos Básicos que Necesitas Saber

### 🌐 ¿Qué es una API?

**API = Application Programming Interface** (Interfaz de Programación de Aplicaciones)

**En palabras simples**: Es como un menú de restaurante que te dice qué puedes pedir.

```
Menú del Restaurante (API):
├─ Ver estadísticas del sistema
├─ Ver todas las reservas
├─ Ver una reserva específica
├─ Marcar OC como recibida
└─ Forzar envío de correos
```

### 📨 Tipos de Peticiones (Métodos HTTP)

Piensa en ellos como **verbos** (acciones):

| Método | ¿Qué hace? | Ejemplo cotidiano |
|--------|------------|-------------------|
| **GET** | **Obtener** información | Leer un libro |
| **POST** | **Crear** algo nuevo o **ejecutar** una acción | Escribir una carta |
| **PUT** | **Actualizar** algo existente | Editar un documento |
| **DELETE** | **Eliminar** algo | Tirar algo a la basura |

**En este sistema usarás principalmente**:
- **GET** → Ver reservas, estadísticas
- **POST** → Marcar OC recibida, forzar envíos

### 🔗 ¿Qué es una URL de API?

Es la **dirección** a la que envías tu petición.

**Formato**:
```
http://localhost:8001/api/reservas
  │         │       │    └─ Lo que quieres (reservas)
  │         │       └─ Prefijo de la API
  │         └─ Puerto (8001)
  └─ Servidor local (tu computadora)
```

**Comparación**:
```
URL Normal:     www.google.com
URL de API:     http://localhost:8001/api/stats
                ↑                          ↑
                Servidor                   Recurso
```

---

## 4. Tu Primera Petición en Postman

### 🎬 Ejemplo paso a paso: Ver estadísticas del sistema

#### Paso 1: Abrir Postman

1. Abre la aplicación Postman
2. Verás una pantalla con varios paneles

#### Paso 2: Crear una nueva petición

1. Busca el botón **"+"** (más) en la parte superior
2. Haz clic en él
3. Se abrirá una nueva pestaña llamada "Untitled Request"

#### Paso 3: Configurar la petición

Ahora verás varios campos:

```
┌─────────────────────────────────────────────────────────────┐
│  GET  ▼  │  Enter URL or paste text                        │ Send
└─────────────────────────────────────────────────────────────┘
```

**A) Seleccionar el método:**
- El primer campo dice "GET" con una flechita
- Déjalo en **GET** (ya está por defecto)

**B) Escribir la URL:**
- En el campo grande, escribe:
  ```
  http://localhost:8001/api/stats
  ```

**IMPORTANTE**: Asegúrate de que:
- ✅ Empiece con `http://` (no `https://`)
- ✅ Diga `localhost:8001` (no otro número)
- ✅ No tenga espacios

#### Paso 4: Enviar la petición

1. Haz clic en el botón azul **"Send"** (Enviar)
2. Espera 1-2 segundos
3. Abajo aparecerá la respuesta

#### Paso 5: Ver la respuesta

En la parte inferior verás algo como:

```json
{
  "total_reservas": 1,
  "oc_pendientes": 1,
  "oc_recibidas": 0,
  "oc_expiradas": 0,
  "criticas": 0
}
```

**¿Qué significa?**:
- `total_reservas`: Cuántas reservas hay en total
- `oc_pendientes`: Cuántas OC faltan por recibir
- `oc_recibidas`: Cuántas OC ya fueron recibidas
- `oc_expiradas`: Cuántas reservas vencieron sin OC
- `criticas`: Cuántas llevan más de 4 días sin OC

### 🎉 ¡Felicidades!

Acabas de hacer tu primera petición a una API. Ahora vamos con ejemplos más prácticos.

---

## 5. Ejemplos Prácticos con el Sistema de OC

### 📊 Ejemplo 1: Ver Estadísticas del Sistema

**¿Para qué sirve?**: Ver un resumen rápido del estado actual

**Paso a paso:**

1. Método: **GET**
2. URL: `http://localhost:8001/api/stats`
3. Click en **Send**

**Respuesta que verás**:
```json
{
  "total_reservas": 1,
  "oc_pendientes": 1,
  "oc_recibidas": 0,
  "oc_expiradas": 0,
  "criticas": 0
}
```

**¿Qué hacer con esta información?**
- Si `oc_pendientes` es alto → Hay muchas OC sin recibir
- Si `criticas` > 0 → Hay reservas urgentes (más de 4 días)

---

### 📋 Ejemplo 2: Ver Todas las Reservas

**¿Para qué sirve?**: Ver lista completa de todas las reservas

**Paso a paso:**

1. Método: **GET**
2. URL: `http://localhost:8001/api/reservas`
3. Click en **Send**

**Respuesta que verás** (ejemplo con 1 reserva):
```json
[
  {
    "id": 1,
    "id_reserva": "45215412",
    "loc_interno": "AAFTTAT",
    "agencia": "WALVIS S.A.",
    "nombre_hotel": "Hoteles",
    "monto_total": 52870100.0,
    "moneda": "CLP",
    "fecha_checkin": "2025-11-27T00:00:00",
    "fecha_checkout": "2025-11-30T00:00:00",
    "estado_oc": "pendiente",
    "requiere_oc": true,
    "dias_desde_creacion": 0
  }
]
```

**Explicación de campos importantes**:
- `id_reserva`: Número de la reserva (45215412)
- `agencia`: Nombre del cliente (WALVIS S.A.)
- `monto_total`: Valor total ($52,870,100)
- `estado_oc`: Estado de la OC (pendiente/recibida/expirada)
- `dias_desde_creacion`: Cuántos días lleva esperando

---

### 🔍 Ejemplo 3: Ver UNA Reserva Específica

**¿Para qué sirve?**: Ver detalles completos de una sola reserva

**Paso a paso:**

1. Método: **GET**
2. URL: `http://localhost:8001/api/reservas/1`
   - El `1` al final es el **ID** de la reserva
   - Cámbialo por el ID que quieras consultar
3. Click en **Send**

**Variaciones**:
```
Ver reserva ID 1:  http://localhost:8001/api/reservas/1
Ver reserva ID 5:  http://localhost:8001/api/reservas/5
Ver reserva ID 10: http://localhost:8001/api/reservas/10
```

---

### 🎯 Ejemplo 4: Filtrar Solo Reservas Pendientes

**¿Para qué sirve?**: Ver solo las que faltan OC

**Paso a paso:**

1. Método: **GET**
2. URL: `http://localhost:8001/api/reservas?estado=pendiente`
   - Nota el `?estado=pendiente` al final
3. Click en **Send**

**Otros filtros útiles**:
```
Solo pendientes:  ?estado=pendiente
Solo recibidas:   ?estado=recibida
Solo expiradas:   ?estado=expirada
```

---

### ✅ Ejemplo 5: Marcar OC como Recibida (Manualmente)

**¿Para qué sirve?**: Cuando recibiste una OC pero el sistema no la detectó

**Paso a paso:**

1. Método: **POST** ⚠️ (ya no es GET)
2. URL: `http://localhost:8001/api/reservas/1/marcar-oc-recibida`
   - Cambia el `1` por el ID de tu reserva
3. **NUEVO PASO**: Configurar el "Body" (cuerpo del mensaje)

   a) Haz clic en la pestaña **"Body"** (debajo de la URL)

   b) Selecciona **"raw"** (crudo)

   c) En el menú desplegable de la derecha, selecciona **"JSON"**

   d) En el cuadro grande, escribe:
   ```json
   {
     "numero_oc": "OC-12345"
   }
   ```

   e) Cambia `"OC-12345"` por el número real de la OC

4. Click en **Send**

**Respuesta exitosa**:
```json
{
  "message": "OC marcada como recibida exitosamente",
  "reserva": {
    "id": 1,
    "id_reserva": "45215412",
    "estado_oc": "recibida"
  }
}
```

**Si algo salió mal**:
```json
{
  "detail": "Reserva no encontrada"
}
```

---

### 🚀 Ejemplo 6: Forzar Procesamiento Inmediato de Correos

**¿Para qué sirve?**: En lugar de esperar 6 horas, procesar ahora mismo

**Paso a paso:**

1. Método: **POST**
2. URL: `http://localhost:8001/api/process-now`
3. **NO necesitas configurar Body** para esta petición
4. Click en **Send**

**Respuesta que verás**:
```json
{
  "message": "Procesamiento iniciado",
  "correos_enviados": 1,
  "timestamp": "2024-12-09T14:55:00"
}
```

**¿Qué significa?**:
- `correos_enviados`: Cuántos correos se enviaron en este momento
- Si es `0` → No había correos pendientes de enviar

---

### 📧 Ejemplo 7: Reenviar un Correo Específico

**¿Para qué sirve?**: Si un correo falló, reenviarlo manualmente

**Paso a paso:**

1. Método: **POST**
2. URL: `http://localhost:8001/api/reservas/1/reenviar-correo?tipo_correo=solicitud_inicial`
   - Cambia el `1` por el ID de la reserva
3. Click en **Send**

**Tipos de correo disponibles**:
```
Solicitud inicial:  ?tipo_correo=solicitud_inicial
Recordatorio día 2: ?tipo_correo=recordatorio_dia_2
Ultimátum día 4:    ?tipo_correo=ultimatum_dia_4
```

**Ejemplo completo**:
```
Reenviar solicitud inicial para reserva 5:
http://localhost:8001/api/reservas/5/reenviar-correo?tipo_correo=solicitud_inicial
```

---

### 👥 Ejemplo 8: Ver Todos los Clientes Configurados

**¿Para qué sirve?**: Ver lista de agencias y sus configuraciones

**Paso a paso:**

1. Método: **GET**
2. URL: `http://localhost:8001/api/clientes`
3. Click en **Send**

**Respuesta que verás**:
```json
[
  {
    "id": 1,
    "nombre_agencia": "WALVIS S.A.",
    "email_contacto": "victor.rodriguez@outlook.com",
    "requiere_oc": true,
    "activo": true,
    "dias_recordatorio_1": 2,
    "dias_recordatorio_2": 4
  },
  {
    "id": 2,
    "nombre_agencia": "SAVAL",
    "email_contacto": null,
    "requiere_oc": true,
    "activo": true
  }
]
```

**¿Qué revisar?**:
- `email_contacto`: Si es `null` → ⚠️ Falta configurar email
- `requiere_oc`: Si es `true` → Cliente necesita OC
- `activo`: Si es `false` → Cliente desactivado

---

## 6. Solución de Problemas Comunes

### ❌ Error: "Could not get any response"

**¿Qué significa?**: Postman no puede conectarse al sistema

**Soluciones**:

1. **Verificar que el sistema esté corriendo**:
   ```bash
   # En Terminal (Mac) o CMD (Windows):
   ps aux | grep "python.*app.py"
   ```

   Si no hay resultado → El sistema NO está corriendo

   **Solución**: Iniciar el sistema
   ```bash
   cd /ruta/al/proyecto/envia2
   python app.py
   ```

2. **Verificar la URL**:
   - ✅ Debe ser: `http://localhost:8001`
   - ❌ NO: `https://localhost:8001` (sin la "s")
   - ❌ NO: `http://localhost:8000` (puerto equivocado)

3. **Verificar el puerto**:
   - El sistema usa el puerto **8001**
   - Si dice "puerto en uso", cámbialo en el `.env`

---

### ❌ Error: "404 Not Found"

**¿Qué significa?**: La URL está mal escrita

**Ejemplo de URL incorrecta**:
```
❌ http://localhost:8001/reservas        (falta /api/)
✅ http://localhost:8001/api/reservas    (correcto)

❌ http://localhost:8001/api/reserva     (falta la "s")
✅ http://localhost:8001/api/reservas    (correcto)
```

**Solución**: Revisa que la URL esté bien escrita

---

### ❌ Error: "422 Unprocessable Entity"

**¿Qué significa?**: Enviaste datos incorrectos en el Body

**Ejemplo de error común**:

**Incorrecto**:
```json
{
  numero_oc: "OC-123"    ← Falta comillas en la clave
}
```

**Correcto**:
```json
{
  "numero_oc": "OC-123"
}
```

**Reglas importantes del JSON**:
1. Las claves van entre comillas dobles: `"numero_oc"`
2. Los valores de texto van entre comillas: `"OC-123"`
3. Los números NO van entre comillas: `12345`
4. Usa dos puntos `:` entre clave y valor
5. No pongas coma después del último elemento

---

### ❌ Error: "500 Internal Server Error"

**¿Qué significa?**: Hubo un error en el sistema (no es tu culpa)

**Solución**:
1. Revisa los logs del sistema:
   ```bash
   tail -f logs/sistema_*.log
   ```

2. Busca líneas con "ERROR" en rojo

3. Si no entiendes el error, copia el mensaje y pide ayuda

---

### ⚠️ La respuesta dice "detail": "Reserva no encontrada"

**¿Qué significa?**: El ID que usaste no existe

**Ejemplo**:
```
URL: http://localhost:8001/api/reservas/999
Respuesta: {"detail": "Reserva no encontrada"}
```

**Solución**:
1. Primero ve TODAS las reservas:
   ```
   GET http://localhost:8001/api/reservas
   ```

2. Busca el ID correcto en la lista

3. Úsalo en tu petición

---

## 7. Glosario de Términos

| Término | Significado Sencillo |
|---------|---------------------|
| **API** | Menú de acciones que puedes pedirle al sistema |
| **Endpoint** | Una dirección específica de la API (como `/api/stats`) |
| **GET** | Pedir información (leer) |
| **POST** | Enviar información o ejecutar una acción |
| **PUT** | Actualizar algo existente |
| **DELETE** | Borrar algo |
| **Body** | El "contenido" que envías con tu petición (como una carta dentro del sobre) |
| **Header** | Información adicional sobre tu petición (como la dirección en el sobre) |
| **Response** | La respuesta que recibes del sistema |
| **Status Code** | Código que indica si funcionó (200=bien, 404=no encontrado, 500=error) |
| **JSON** | Formato de texto para intercambiar datos (como un idioma común) |
| **localhost** | Tu propia computadora (como decir "mi casa") |
| **Puerto** | Un número que identifica un servicio (como 8001) |

---

## 8. Referencia Rápida de Endpoints

### 📊 Solo Lectura (GET)

| Lo que quiero hacer | Método | URL |
|---------------------|--------|-----|
| Ver estadísticas | GET | `http://localhost:8001/api/stats` |
| Ver todas las reservas | GET | `http://localhost:8001/api/reservas` |
| Ver reservas pendientes | GET | `http://localhost:8001/api/reservas?estado=pendiente` |
| Ver reservas recibidas | GET | `http://localhost:8001/api/reservas?estado=recibida` |
| Ver UNA reserva específica | GET | `http://localhost:8001/api/reservas/{ID}` |
| Ver todos los clientes | GET | `http://localhost:8001/api/clientes` |
| Ver correos enviados | GET | `http://localhost:8001/api/correos` |

### ✏️ Modificar o Ejecutar (POST)

| Lo que quiero hacer | Método | URL | Body necesario |
|---------------------|--------|-----|----------------|
| Marcar OC como recibida | POST | `http://localhost:8001/api/reservas/{ID}/marcar-oc-recibida` | `{"numero_oc": "OC-123"}` |
| Forzar procesamiento ahora | POST | `http://localhost:8001/api/process-now` | No necesita |
| Reenviar correo | POST | `http://localhost:8001/api/reservas/{ID}/reenviar-correo?tipo_correo=solicitud_inicial` | No necesita |

**Nota**: `{ID}` significa que debes reemplazarlo por el número real, ejemplo: `/reservas/1`

---

## 9. Consejos y Mejores Prácticas

### 💡 Tip 1: Guarda tus peticiones favoritas

1. Después de configurar una petición, haz clic en **"Save"** (Guardar)
2. Dale un nombre descriptivo: "Ver estadísticas del sistema"
3. Crea una carpeta: "Sistema de OC"
4. Así podrás reutilizarlas fácilmente

### 💡 Tip 2: Usa variables de entorno

En lugar de escribir siempre `http://localhost:8001`, puedes crear una variable:

1. Haz clic en el ícono de ⚙️ (engranaje) arriba a la derecha
2. Click en "Add" en la sección "Environments"
3. Crea una variable:
   - Variable: `base_url`
   - Initial Value: `http://localhost:8001`
4. Ahora en tus URLs usa: `{{base_url}}/api/stats`

**Ventaja**: Si el puerto cambia, solo actualizas un lugar.

### 💡 Tip 3: Organiza tus peticiones en colecciones

```
📁 Sistema de OC
  ├─ 📊 Consultas
  │   ├─ Ver estadísticas
  │   ├─ Ver todas las reservas
  │   └─ Ver clientes
  ├─ ✏️ Acciones
  │   ├─ Marcar OC recibida
  │   └─ Forzar procesamiento
  └─ 🧪 Pruebas
      └─ Test de conexión
```

### 💡 Tip 4: Revisa el código de estado (Status Code)

En la respuesta, arriba a la derecha verás:

```
Status: 200 OK          ← ✅ Funcionó perfecto
Status: 404 Not Found   ← ❌ No encontró lo que buscabas
Status: 500 Error       ← ❌ Error del servidor
```

**Códigos comunes**:
- **200**: Todo bien ✅
- **201**: Creado exitosamente ✅
- **400**: Enviaste algo mal ⚠️
- **404**: No encontrado ❌
- **500**: Error del servidor ❌

---

## 10. Práctica Guiada Final

Vamos a hacer un ejercicio completo paso a paso:

### 🎯 Objetivo: Ver una reserva pendiente y marcarla como recibida

**Paso 1: Ver todas las reservas pendientes**
```
Método: GET
URL: http://localhost:8001/api/reservas?estado=pendiente
Click: Send
```

**Paso 2: Anotar el ID de una reserva**

De la respuesta, copia el número `"id"`:
```json
{
  "id": 1,          ← Este número
  "id_reserva": "45215412",
  ...
}
```

**Paso 3: Ver detalles completos de esa reserva**
```
Método: GET
URL: http://localhost:8001/api/reservas/1
      (usa el ID que copiaste)        ↑
Click: Send
```

**Paso 4: Marcar la OC como recibida**
```
Método: POST
URL: http://localhost:8001/api/reservas/1/marcar-oc-recibida

Body (pestaña "Body" → "raw" → "JSON"):
{
  "numero_oc": "OC-54321"
}

Click: Send
```

**Paso 5: Verificar que se marcó**
```
Método: GET
URL: http://localhost:8001/api/reservas/1
Click: Send

Busca en la respuesta:
"estado_oc": "recibida"  ← ✅ Éxito!
```

### 🎉 ¡Felicidades!

Completaste un flujo completo usando la API.

---

## 11. Recursos Adicionales

### 📚 Documentación del Sistema

El sistema tiene documentación automática en:
```
http://localhost:8001/docs
```

Abre esa URL en tu navegador y verás:
- Lista completa de endpoints
- Descripción de cada uno
- Puedes probarlos directamente ahí (sin Postman)

### 🎥 Videos Recomendados (YouTube)

Busca en YouTube:
- "Postman tutorial español principiantes"
- "Cómo usar Postman paso a paso"
- "APIs para principiantes"

### 🆘 ¿Necesitas ayuda?

Si tienes dudas:
1. Revisa la sección de troubleshooting (sección 6)
2. Consulta los logs del sistema
3. Pide ayuda al equipo técnico con:
   - Captura de pantalla de Postman
   - El mensaje de error completo
   - Lo que intentabas hacer

---

## 12. Checklist de Verificación

Antes de pedir ayuda, verifica:

- [ ] ¿El sistema está corriendo? (`ps aux | grep python.*app.py`)
- [ ] ¿La URL empieza con `http://` (no `https://`)?
- [ ] ¿La URL tiene el puerto correcto (`:8001`)?
- [ ] ¿El método HTTP es el correcto (GET o POST)?
- [ ] Si es POST, ¿configuraste el Body en formato JSON?
- [ ] ¿El JSON está bien escrito (comillas, comas)?
- [ ] ¿El ID de la reserva existe?
- [ ] ¿Revisaste el Status Code de la respuesta?

---

**Última actualización**: 9 de Diciembre de 2024
**Versión del documento**: 1.0
**Sistema**: Seguimiento de OC v1.3.3

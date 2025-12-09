# 📧 Guía Rápida: Actualización de Emails de Contacto

**Versión**: 1.3.3
**Fecha**: 9 de Diciembre de 2024

---

## 🎯 Objetivo

Configurar los emails de contacto de los 76 clientes cargados en el sistema para que las solicitudes de OC lleguen a las personas correctas.

---

## 📋 Estado Actual

- ✅ **76 clientes cargados** en `configuracion_clientes`
- ✅ **Script de actualización creado**: `scripts/utils/actualizar_emails_clientes.py`
- ✅ **Plantilla CSV creada**: `data/emails_clientes_template.csv`
- ⚠️ **PENDIENTE**: Poblar los emails reales de cada cliente

---

## 🚀 Métodos de Actualización

### Opción 1: Actualización por CSV (Recomendado para múltiples clientes)

**Paso 1**: Editar la plantilla con emails reales

```bash
# Abrir plantilla en tu editor preferido
open data/emails_clientes_template.csv
# o
nano data/emails_clientes_template.csv
```

**Paso 2**: Reemplazar los placeholders con emails reales

```csv
# Antes:
SAVAL,contacto@saval.com

# Después:
SAVAL,compras@saval.cl
```

**Paso 3**: Importar el archivo

```bash
python scripts/utils/actualizar_emails_clientes.py --archivo data/emails_clientes_template.csv
```

**Resultado esperado**:
```
✅ SAVAL                                               -> compras@saval.cl
✅ SPARTA                                              -> adquisiciones@sparta.cl
...

📊 Resumen:
  ✅ Actualizados: 76
  ❌ Errores: 0
```

---

### Opción 2: Actualización Individual (Para pocos clientes)

**Método A: Línea de comandos**

```bash
python scripts/utils/actualizar_emails_clientes.py \
  --cliente "SAVAL" \
  --email "compras@saval.cl"
```

**Método B: Modo interactivo**

```bash
python scripts/utils/actualizar_emails_clientes.py

# Seleccionar opción 3: "Actualizar email de un cliente"
# Seguir las instrucciones en pantalla
```

---

### Opción 3: Actualización desde Python (Programática)

```python
from scripts.utils.actualizar_emails_clientes import actualizar_desde_dict

emails = {
    "SAVAL": "compras@saval.cl",
    "SPARTA": "adquisiciones@sparta.cl",
    "WALVIS S.A.": "oc@walvis.cl"
    # ... más clientes
}

actualizar_desde_dict(emails)
```

---

## 🔍 Verificación

### Ver clientes SIN email configurado

```bash
python scripts/utils/actualizar_emails_clientes.py --sin-email
```

**Salida esperada**:
```
📋 Clientes SIN email configurado: 73

──────────────────────────────────────────────────────────────────────
  • FUNDACION COANIL                                 | NO requiere OC
  • SAVAL                                            | SÍ requiere OC
  • SPARTA                                           | SÍ requiere OC
  ...
```

### Ver TODOS los clientes con sus emails

```bash
python scripts/utils/actualizar_emails_clientes.py --todos
```

**Salida esperada**:
```
📋 Todos los clientes (76):

──────────────────────────────────────────────────────────────────────────────────────
AGENCIA                                            | EMAIL                          | OC
──────────────────────────────────────────────────────────────────────────────────────
FUNDACION COANIL                                   | (sin email)                    | NO
SAVAL                                              | compras@saval.cl               | SÍ
...
```

---

## ⚠️ Consideraciones Importantes

### 1. Prioridad de Emails

**Alta prioridad** (37 clientes):
- Clientes que **requieren OC** deben tener email configurado
- Sin email, el sistema registrará error y NO enviará solicitudes

**Media prioridad** (39 clientes):
- Clientes que **NO requieren OC** pueden dejarse sin email por ahora
- Recomendado configurarlos para futuras necesidades

### 2. Coincidencia Exacta de Nombres

⚠️ **El nombre de la agencia debe coincidir EXACTAMENTE**:

```bash
# ✅ CORRECTO
SAVAL,compras@saval.cl

# ❌ INCORRECTO (mayúsculas diferentes)
saval,compras@saval.cl
Saval,compras@saval.cl
```

**Tip**: Usa la opción `--todos` para copiar los nombres exactos de la BD.

### 3. Validación de Emails

El script valida formato básico:
- Debe contener `@`
- Debe tener dominio con `.`

Ejemplo válidos:
- ✅ `compras@saval.cl`
- ✅ `adquisiciones@empresa.com.ar`
- ❌ `invalido@`
- ❌ `sin-arroba.com`

---

## 📊 Estado del Sistema

### Ver estadísticas actuales

```bash
cd scripts/database
python limpiar_base_datos.py --stats
```

**Salida**:
```
╔════════════════════════════════════════════════════════════════════╗
║              📊 ESTADÍSTICAS DE BASE DE DATOS                      ║
╚════════════════════════════════════════════════════════════════════╝

📦 Reservas totales: X
   ├─ 🔴 Pendientes: X
   ├─ 🟢 Recibidas: X
   └─ ⚪ Otros: X

📧 Correos enviados: X
   ├─ ✅ Exitosos: X
   └─ ❌ Errores: X

👥 Clientes configurados: 76
   ├─ ✅ Requieren OC: 37
   └─ ⚪ No requieren: 39

📄 Órdenes de compra: X
```

---

## 🧪 Probar el Sistema

### 1. Verificar que un cliente tiene email

```bash
PYTHONPATH=. python -c "
from database import init_db, get_db, ConfiguracionCliente
init_db()
db = next(get_db())
cliente = db.query(ConfiguracionCliente).filter_by(nombre_agencia='SAVAL').first()
print(f'SAVAL email: {cliente.email_contacto if cliente else \"NO ENCONTRADO\"}')
"
```

### 2. Probar envío de solicitud (simulado)

Cuando tengas al menos un cliente con email configurado, puedes probar el flujo completo:

1. Procesar un PDF de confirmación con esa agencia
2. El sistema creará la reserva
3. Enviará solicitud de OC al email configurado

**Monitorear logs**:
```bash
tail -f logs/sistema_$(date +%Y%m%d).log
```

Deberías ver:
```
INFO | EmailSender | Enviando correo a compras@saval.cl: Solicitud de Orden de Compra - Reserva ABC123
INFO | EmailSender | ✅ Correo enviado exitosamente a compras@saval.cl
```

---

## 📝 Plantilla de Correo para Solicitar Emails

Si necesitas solicitar los emails a alguien, usa esta plantilla:

```
Asunto: Solicitud de emails de contacto para sistema de OC

Hola [Nombre],

Para configurar correctamente el sistema de seguimiento de órdenes de compra,
necesito los emails de contacto de los siguientes clientes:

CLIENTES QUE REQUIEREN OC (URGENTE):
- SAVAL
- SPARTA
- WALVIS S.A.
- ... [lista completa de 37 clientes]

Por favor, proporcionar en formato:
NOMBRE_CLIENTE,email@dominio.com

Ejemplo:
SAVAL,compras@saval.cl
SPARTA,adquisiciones@sparta.cl

Gracias!
```

---

## 🎯 Checklist de Implementación

- [ ] Obtener emails reales de los 37 clientes que requieren OC
- [ ] Editar `data/emails_clientes_template.csv` con emails reales
- [ ] Importar emails con `--archivo`
- [ ] Verificar con `--todos` que se guardaron correctamente
- [ ] Probar envío con una reserva de prueba
- [ ] Monitorear logs para confirmar envíos exitosos
- [ ] (Opcional) Configurar emails de clientes que NO requieren OC

---

## 🆘 Troubleshooting

### Problema: "No se encontró cliente: NOMBRE"

**Causa**: El nombre no coincide exactamente

**Solución**:
```bash
# Ver nombres exactos en la BD
python scripts/utils/actualizar_emails_clientes.py --todos
```

### Problema: "Email actualizado pero el sistema no envía"

**Causa posible 1**: Nombre de agencia en reserva diferente a configuracion_clientes

**Solución**: Normalizar nombres o implementar búsqueda case-insensitive

**Causa posible 2**: Credenciales SMTP incorrectas

**Solución**:
```bash
python scripts/utils/test_conexion.py
```

### Problema: "Archivo no encontrado"

**Causa**: Ruta incorrecta o ejecutando desde directorio equivocado

**Solución**: Ejecutar desde la raíz del proyecto
```bash
cd /Users/cucho/Library/CloudStorage/OneDrive-Personal/DESARROLLOS/agente-travelIA/envia2
python scripts/utils/actualizar_emails_clientes.py --archivo data/emails_clientes_template.csv
```

---

## 📚 Documentación Relacionada

- `docs/CAMBIO_EMAIL_CONTACTO.md` - Explicación técnica del cambio
- `scripts/README.md` - Documentación completa de scripts
- `CHANGELOG.md` - Historial de versiones

---

**Última actualización**: 9 de Diciembre de 2024
**Versión del sistema**: 1.3.3

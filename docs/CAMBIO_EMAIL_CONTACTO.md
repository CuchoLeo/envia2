# 📧 Cambio: Uso de email_contacto de configuracion_clientes

**Fecha**: 9 de Diciembre de 2024
**Versión**: 1.3.3
**Módulo afectado**: `src/email_sender.py`

---

## 🎯 Objetivo del Cambio

El sistema ahora **envía las solicitudes de OC al email configurado en el campo `email_contacto`** de la tabla `configuracion_clientes`, en lugar de usar un placeholder genérico.

---

## ✅ Qué se Modificó

### Archivo: `src/email_sender.py`

#### 1. **Nuevo método `_get_cliente_email()`**

```python
def _get_cliente_email(self, reserva: Reserva, db: Session) -> Optional[str]:
    """
    Obtiene el email de contacto del cliente desde configuracion_clientes

    Busca en la tabla configuracion_clientes por nombre_agencia
    y retorna el email_contacto configurado.
    """
```

**Comportamiento**:
- Busca el cliente por `nombre_agencia` (debe coincidir exactamente)
- Retorna el `email_contacto` si existe
- Retorna `None` si no encuentra el cliente o no tiene email configurado
- Loguea warning si no encuentra el email

#### 2. **Modificados 3 métodos de envío de correos**

**a) `send_solicitud_inicial()`**

**Antes**:
```python
if not to_email:
    to_email = "contacto@agencia.com"  # Placeholder
```

**Ahora**:
```python
if not to_email:
    to_email = self._get_cliente_email(reserva, db)

    if not to_email:
        error_msg = f"No hay email de contacto configurado para {reserva.agencia}"
        self.logger.error(error_msg)

        # Registra el intento fallido en BD
        correo = CorreoEnviado(
            reserva_id=reserva.id,
            tipo_correo=TipoCorreo.SOLICITUD_INICIAL,
            destinatario="SIN EMAIL",
            estado=EstadoEnvio.ERROR,
            mensaje_error=error_msg,
            ...
        )
        db.add(correo)
        db.commit()
        return False
```

**b) `send_recordatorio_dia2()`** - Mismo cambio

**c) `send_ultimatum_dia4()`** - Mismo cambio

#### 3. **Modificado método `enviar_solicitud_oc()`**

**Antes**:
```python
if not destinatario:
    destinatario = "contacto@agencia.com"  # Placeholder
```

**Ahora**:
```python
if not destinatario:
    # Sin db no podemos buscar el email, retornar error
    error_msg = "No se proporcionó destinatario y no hay sesión de BD para buscarlo"
    self.logger.error(error_msg)
    return False
```

**Nota**: Este método sin `db` requiere que se pase explícitamente el `destinatario`.
Para búsqueda automática, usar los métodos específicos con `db`.

---

## 🔄 Flujo de Envío de Correos

### Antes del Cambio

```
1. Reserva creada con agencia "SAVAL"
2. Sistema intenta enviar solicitud OC
3. No hay to_email especificado
4. Usa "contacto@agencia.com" ❌ (placeholder inválido)
5. Envío falla o va a email incorrecto
```

### Después del Cambio

```
1. Reserva creada con agencia "SAVAL"
2. Sistema intenta enviar solicitud OC
3. No hay to_email especificado
4. Busca en configuracion_clientes WHERE nombre_agencia = "SAVAL"
5. Obtiene email_contacto (ej: "compras@saval.cl") ✅
6. Envío exitoso al email correcto
```

### Si no hay email configurado

```
1. Reserva creada con agencia "NUEVA EMPRESA"
2. Sistema intenta enviar solicitud OC
3. No hay to_email especificado
4. Busca en configuracion_clientes - NO ENCUENTRA
5. Loguea error: "No hay email de contacto configurado para NUEVA EMPRESA"
6. Registra en BD como ERROR con destinatario="SIN EMAIL"
7. Retorna False
```

---

## 📋 Requisitos para que Funcione

### 1. Cliente debe estar en `configuracion_clientes`

```sql
SELECT * FROM configuracion_clientes WHERE nombre_agencia = 'SAVAL';
```

Debe existir un registro con ese nombre **exacto**.

### 2. Campo `email_contacto` debe estar lleno

```sql
UPDATE configuracion_clientes
SET email_contacto = 'compras@saval.cl'
WHERE nombre_agencia = 'SAVAL';
```

### 3. El nombre de agencia en la reserva debe coincidir exactamente

**Funciona** ✅:
- Reserva con `agencia = "SAVAL"`
- Cliente en BD: `nombre_agencia = "SAVAL"`

**NO funciona** ❌:
- Reserva con `agencia = "Saval"` (mayúsculas diferentes)
- Cliente en BD: `nombre_agencia = "SAVAL"`
- **Solución**: Normalizar nombres o usar búsqueda case-insensitive

---

## 🚨 Casos de Error y Manejo

### Error 1: Cliente no existe en configuracion_clientes

**Síntoma**:
```
WARNING | No se encontró email de contacto para agencia: NUEVA EMPRESA
ERROR | No hay email de contacto configurado para NUEVA EMPRESA
```

**Solución**:
```python
# Agregar cliente a la BD
nuevo_cliente = ConfiguracionCliente(
    nombre_agencia='NUEVA EMPRESA',
    email_contacto='contacto@nuevaempresa.com',
    requiere_oc=True,
    activo=True
)
db.add(nuevo_cliente)
db.commit()
```

### Error 2: Cliente existe pero sin email_contacto

**Síntoma**:
```
WARNING | No se encontró email de contacto para agencia: WALVIS S.A.
ERROR | No hay email de contacto configurado para WALVIS S.A.
```

**Solución**:
```sql
UPDATE configuracion_clientes
SET email_contacto = 'compras@walvis.cl'
WHERE nombre_agencia = 'WALVIS S.A.';
```

### Error 3: Nombre de agencia no coincide

**Síntoma**:
- En reserva: `agencia = "Walvis SA"`
- En BD: `nombre_agencia = "WALVIS S.A."`
- No encuentra coincidencia

**Solución opción A** (Normalizar en reserva):
```python
# En pdf_processor.py o email_monitor.py
agencia_normalizada = agencia.upper().strip()
```

**Solución opción B** (Búsqueda case-insensitive):
```python
# En _get_cliente_email()
from sqlalchemy import func

cliente = db.query(ConfiguracionCliente).filter(
    func.lower(ConfiguracionCliente.nombre_agencia) == func.lower(reserva.agencia)
).first()
```

---

## 📊 Logging y Auditoría

### Logs Exitosos

```
INFO | EmailSender | Enviando correo a compras@saval.cl: Solicitud de Orden de Compra - Reserva ABC123
INFO | EmailSender | ✅ Correo enviado exitosamente a compras@saval.cl
```

### Logs de Error (sin email)

```
WARNING | EmailSender | No se encontró email de contacto para agencia: NUEVA EMPRESA
ERROR | EmailSender | No hay email de contacto configurado para NUEVA EMPRESA
```

### Registro en Base de Datos

Cuando falla por falta de email, se registra en `correos_enviados`:

```python
{
    'reserva_id': 123,
    'tipo_correo': TipoCorreo.SOLICITUD_INICIAL,
    'destinatario': 'SIN EMAIL',  # ← Indicador de error
    'estado': EstadoEnvio.ERROR,
    'mensaje_error': 'No hay email de contacto configurado para NUEVA EMPRESA',
    'intentos': 1
}
```

---

## 🧪 Cómo Probar

### 1. Verificar que cliente tiene email

```bash
PYTHONPATH=. python -c "
from database import init_db, get_db, ConfiguracionCliente
init_db()
db = next(get_db())
cliente = db.query(ConfiguracionCliente).filter_by(nombre_agencia='SAVAL').first()
print(f'Email: {cliente.email_contacto if cliente else \"NO ENCONTRADO\"}')
"
```

### 2. Agregar email a cliente

```bash
PYTHONPATH=. python -c "
from database import init_db, get_db, ConfiguracionCliente
init_db()
db = next(get_db())
cliente = db.query(ConfiguracionCliente).filter_by(nombre_agencia='SAVAL').first()
if cliente:
    cliente.email_contacto = 'compras@saval.cl'
    db.commit()
    print('✅ Email actualizado')
else:
    print('❌ Cliente no encontrado')
"
```

### 3. Probar envío (sin enviar realmente)

```bash
# Editar src/email_sender.py temporalmente
# Comentar la línea: server.send_message(msg, ...)
# Agregar: print(f"DEBUG: Enviaría a {to_email}")

PYTHONPATH=. python -c "
from src.email_sender import EmailSender
from database import init_db, get_db, Reserva
init_db()
db = next(get_db())

# Crear reserva de prueba con agencia que tiene email
reserva = Reserva(
    id_reserva='TEST123',
    loc_interno='LOC123',
    agencia='SAVAL',  # Debe existir en configuracion_clientes
    monto_total=100000,
    requiere_oc=True
)
db.add(reserva)
db.commit()

# Intentar enviar
sender = EmailSender()
result = sender.send_solicitud_inicial(reserva, db)
print(f'Resultado: {result}')
"
```

---

## 📝 Checklist de Implementación

- [x] Importar `ConfiguracionCliente` en `email_sender.py`
- [x] Crear método `_get_cliente_email()`
- [x] Modificar `send_solicitud_inicial()` para usar el nuevo método
- [x] Modificar `send_recordatorio_dia2()` para usar el nuevo método
- [x] Modificar `send_ultimatum_dia4()` para usar el nuevo método
- [x] Modificar `enviar_solicitud_oc()` para requerir destinatario sin db
- [x] Agregar logging apropiado (warning y error)
- [x] Registrar intentos fallidos en `correos_enviados`
- [ ] **PENDIENTE**: Poblar campo `email_contacto` en los 76 clientes
- [ ] **PENDIENTE**: Probar con reserva real
- [ ] **PENDIENTE**: Actualizar CHANGELOG
- [ ] **PENDIENTE**: Actualizar documentación principal

---

## 🔜 Próximos Pasos Recomendados

### 1. Poblar emails de contacto en clientes

```sql
-- Actualizar clientes con emails conocidos
UPDATE configuracion_clientes SET email_contacto = 'compras@saval.cl' WHERE nombre_agencia = 'SAVAL';
UPDATE configuracion_clientes SET email_contacto = 'oc@sparta.cl' WHERE nombre_agencia = 'SPARTA';
-- ... etc
```

### 2. Implementar búsqueda case-insensitive (opcional)

Modificar `_get_cliente_email()` para buscar sin importar mayúsculas/minúsculas.

### 3. Agregar endpoint API para configurar emails

Permitir actualizar `email_contacto` desde el dashboard web.

### 4. Normalización automática de nombres

Implementar en `pdf_processor.py` o `email_monitor.py` para normalizar nombres de agencias.

---

## ✅ Impacto del Cambio

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Destinatario de correos** | Placeholder fijo | Email de configuracion_clientes |
| **Cuando falta email** | Envío fallido silencioso | Error registrado en BD + logs |
| **Flexibilidad** | No configurable | Configurable por cliente |
| **Auditoría** | Sin trazabilidad | Completa en logs y BD |
| **Mantenimiento** | Hardcoded | Administrable desde BD/Dashboard |

---

**Última actualización**: 9 de Diciembre de 2024
**Autor**: Sistema actualizado por Claude Code

# Cambio: Lógica de Expiración de Reservas

**Fecha**: 10 de Diciembre de 2024
**Versión**: 1.3.5

## Problema Identificado

La reserva 45215412 fue marcada incorrectamente como **EXPIRADA** por la tarea `cleanup_expired_reservations` que se ejecuta diariamente a las 2 AM.

### ¿Por qué sucedió?

La lógica anterior verificaba:
```python
if Reserva.fecha_checkin < now:
    # Marcar como expirada
```

**Problema**: El campo `fecha_checkin` en el PDF puede contener la **fecha de emisión** del servicio (no la fecha real de check-in al hotel). En este caso:
- PDF tenía "Fecha Emisión: INMEDIATO"
- El campo "Check In: 27 nov 2025" contenía la fecha de emisión
- El sistema extrajo `fecha_checkin = 27 nov 2025`
- El correo llegó el **9 dic 2025** (solo 1 día transcurrido)
- Pero el scheduler marcó como expirada porque `27 nov < 10 dic` ❌

## Solución Implementada

### Cambio en `src/scheduler.py`

**ANTES** (líneas 200-234):
```python
async def cleanup_expired_reservations(self):
    """
    Limpia reservas expiradas (check-in pasado, sin OC)
    """
    # Reservas con check-in pasado y OC pendiente
    expired = db.query(Reserva).filter(
        Reserva.fecha_checkin < now,  # ❌ Usa fecha_checkin
        Reserva.estado_oc == EstadoOC.PENDIENTE,
        Reserva.requiere_oc == True
    ).all()
```

**DESPUÉS**:
```python
async def cleanup_expired_reservations(self):
    """
    Marca como expiradas las reservas que llevan más de 30 días sin OC
    (calculado desde fecha_emision o email_origen_fecha)
    """
    # Obtener todas las reservas pendientes que requieren OC
    pending_reservas = db.query(Reserva).filter(
        Reserva.estado_oc == EstadoOC.PENDIENTE,
        Reserva.requiere_oc == True
    ).all()

    # Usar la propiedad dias_desde_creacion que calcula correctamente
    # desde fecha_emision > email_origen_fecha > fecha_creacion
    for reserva in pending_reservas:
        if reserva.dias_desde_creacion > 30:  # ✅ Usa dias_desde_creacion
            reserva.estado_oc = EstadoOC.EXPIRADA
```

## Lógica Nueva

### Criterio de Expiración

Una reserva se marca como **EXPIRADA** cuando:
- `estado_oc == PENDIENTE`
- `requiere_oc == True`
- `dias_desde_creacion > 30 días`

### Cálculo de `dias_desde_creacion`

La propiedad `dias_desde_creacion` usa la siguiente prioridad:

1. **`fecha_emision`** (del PDF) - si está disponible y no es "INMEDIATO"
2. **`email_origen_fecha`** - fecha en que llegó el correo
3. **`fecha_creacion`** - fecha de creación del registro en BD

```python
@property
def dias_desde_creacion(self) -> int:
    fecha_referencia = self.fecha_emision or self.email_origen_fecha or self.fecha_creacion
    return (datetime.utcnow() - fecha_referencia).days
```

## Ejemplo: Reserva 45215412

| Campo | Valor | Uso |
|-------|-------|-----|
| `fecha_emision` | NULL (PDF dice "INMEDIATO") | - |
| `email_origen_fecha` | 9 dic 2025 21:32 | ✅ **Usado como día 0** |
| `fecha_checkin` | 27 nov 2025 | ❌ Ya NO se usa para expiración |
| `dias_desde_creacion` | 1 día | < 30 días → NO expira |

**Antes**: Marcada como EXPIRADA (porque 27 nov < 10 dic)
**Ahora**: PENDIENTE (porque solo ha pasado 1 día desde el correo)

## Ventajas

1. ✅ **Consistencia**: Usa la misma lógica de fechas que el flujo de seguimiento
2. ✅ **Flexibilidad**: No importa si la fecha de check-in ya pasó
3. ✅ **Control**: 30 días es tiempo suficiente para obtener la OC
4. ✅ **Correcto**: Calcula desde la fecha de emisión real, no del campo check-in

## Configuración

El límite de **30 días** está hardcoded en `scheduler.py` línea 220:

```python
if reserva.dias_desde_creacion > 30:
```

Para cambiar el límite de días, modificar este número.

## Testing

### Verificar que NO expira antes de 30 días

```bash
# Ver reservas pendientes y sus días
sqlite3 data/oc_seguimiento.db "
SELECT
    id_reserva,
    estado_oc,
    fecha_emision,
    email_origen_fecha,
    fecha_checkin
FROM reservas
WHERE estado_oc = 'PENDIENTE';
"
```

### Simular expiración

Para probar la lógica de expiración sin esperar 30 días:

1. Cambiar temporalmente el límite a 1 día en `scheduler.py`:
   ```python
   if reserva.dias_desde_creacion > 1:  # Temporal para testing
   ```

2. Ejecutar manualmente la tarea:
   ```python
   from src.scheduler import OCScheduler
   import asyncio

   scheduler = OCScheduler()
   asyncio.run(scheduler.cleanup_expired_reservations())
   ```

3. Verificar logs:
   ```bash
   tail -f logs/oc_seguimiento_*.log | grep "expirada"
   ```

## Migración de Datos

Las reservas que fueron marcadas incorrectamente como EXPIRADAS necesitan corregirse:

```sql
-- Ver reservas marcadas como expiradas en los últimos 7 días
SELECT id_reserva, agencia, estado_oc, fecha_checkin, email_origen_fecha
FROM reservas
WHERE estado_oc = 'EXPIRADA'
AND fecha_actualizacion >= datetime('now', '-7 days');

-- Corregir manualmente si es necesario
UPDATE reservas
SET estado_oc = 'PENDIENTE'
WHERE id_reserva = '45215412';
```

## Impacto

- ✅ **Reservas antiguas**: Ya no se marcarán como expiradas por fecha de check-in pasada
- ✅ **Nuevas reservas**: Solo expirarán después de 30 días sin OC
- ✅ **Flujo de seguimiento**: No afectado (sigue usando `dias_desde_creacion`)

## Próximas Mejoras

1. **Hacer configurable el límite de días** vía `.env`:
   ```bash
   DAYS_TO_EXPIRE_RESERVATION=30
   ```

2. **Enviar notificación cuando expira** (actualmente solo se loggea)

3. **Dashboard**: Agregar filtro para ver reservas próximas a expirar (> 25 días)

---

**Versión del documento**: 1.0
**Relacionado con**: v1.3.4 (Usar fecha de emisión del PDF)
**Archivo modificado**: `src/scheduler.py` (líneas 200-237)

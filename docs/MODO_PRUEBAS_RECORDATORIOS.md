# Modo Pruebas - Recordatorios Acelerados

**Fecha**: 10 de Diciembre de 2024
**Versión**: 1.3.7 (Modo Pruebas)

## ⚠️ IMPORTANTE: Sistema en Modo Pruebas

El sistema está configurado actualmente en **MODO PRUEBAS** con periodos de recordatorio acelerados para facilitar el testing.

## 📊 Periodos Configurados

### Modo Pruebas (ACTUAL)

#### Recordatorios

| Evento | Tiempo | Estado |
|--------|--------|--------|
| **Solicitud Inicial** | Inmediatamente (día 0) | ✅ Activo |
| **Recordatorio** | 30 minutos después | ✅ Activo |
| **Ultimátum** | 60 minutos (1 hora) después | ✅ Activo |

#### Scheduler

| Tarea | Intervalo Pruebas | Intervalo Producción |
|-------|------------------|---------------------|
| **Procesar correos pendientes** | ✅ Cada 5 minutos | ❌ Cada 6 horas |
| **Reintentar correos fallidos** | ✅ Cada 10 minutos | ❌ Cada 2 horas |
| **Limpieza de expiradas** | Diario 2 AM | Diario 2 AM |
| **Reporte diario** | Diario 8 AM | Diario 8 AM |

### Modo Producción (Comentado)

| Evento | Tiempo | Estado |
|--------|--------|--------|
| Solicitud Inicial | Día 0 | ❌ N/A |
| Recordatorio | Día 2 (48 horas) | ❌ Comentado |
| Ultimátum | Día 4 (96 horas) | ❌ Comentado |
| Scheduler | Cada 6 horas | ❌ Comentado |

## 🔧 Cambios Realizados en `database.py`

### Nueva Propiedad Agregada

**Líneas 129-136**:
```python
@property
def minutos_desde_creacion(self) -> int:
    """
    Calcula minutos transcurridos desde la fecha de emisión del PDF
    Útil para pruebas con periodos cortos
    """
    fecha_referencia = self.fecha_emision or self.email_origen_fecha or self.fecha_creacion
    return int((datetime.utcnow() - fecha_referencia).total_seconds() / 60)
```

### Modo Producción (Comentado)

**Líneas 147-168**:
```python
# ============================================================================
# MODO PRODUCCIÓN - Recordatorios por días (COMENTADOS PARA PRUEBAS)
# ============================================================================
# @property
# def necesita_recordatorio_dia2(self) -> bool:
#     """Verifica si necesita recordatorio día 2"""
#     return (
#         self.requiere_oc
#         and self.estado_oc == EstadoOC.PENDIENTE
#         and self.dias_desde_creacion >= 2
#         and not any(c.tipo_correo == TipoCorreo.RECORDATORIO_DIA_2 for c in self.correos_enviados)
#     )
#
# @property
# def necesita_ultimatum_dia4(self) -> bool:
#     """Verifica si necesita ultimátum día 4"""
#     return (
#         self.requiere_oc
#         and self.estado_oc == EstadoOC.PENDIENTE
#         and self.dias_desde_creacion >= 4
#         and not any(c.tipo_correo == TipoCorreo.ULTIMATUM_DIA_4 for c in self.correos_enviados)
#     )
```

### Modo Pruebas (Activo)

**Líneas 170-197**:
```python
# ============================================================================
# MODO PRUEBAS - Recordatorios por minutos (ACTIVO)
# ============================================================================
@property
def necesita_recordatorio_dia2(self) -> bool:
    """
    MODO PRUEBAS: Verifica si necesita recordatorio después de 30 minutos
    Para producción: cambiar minutos_desde_creacion >= 30 por dias_desde_creacion >= 2
    """
    return (
        self.requiere_oc
        and self.estado_oc == EstadoOC.PENDIENTE
        and self.minutos_desde_creacion >= 30  # 30 minutos para pruebas
        and not any(c.tipo_correo == TipoCorreo.RECORDATORIO_DIA_2 for c in self.correos_enviados)
    )

@property
def necesita_ultimatum_dia4(self) -> bool:
    """
    MODO PRUEBAS: Verifica si necesita ultimátum después de 1 hora
    Para producción: cambiar minutos_desde_creacion >= 60 por dias_desde_creacion >= 4
    """
    return (
        self.requiere_oc
        and self.estado_oc == EstadoOC.PENDIENTE
        and self.minutos_desde_creacion >= 60  # 60 minutos (1 hora) para pruebas
        and not any(c.tipo_correo == TipoCorreo.ULTIMATUM_DIA_4 for c in self.correos_enviados)
    )
```

## 🧪 Cómo Funciona el Modo Pruebas

### Timeline de Prueba

```
Tiempo 0 (T+0min): Llega correo de confirmación
   ↓
   📧 Solicitud inicial enviada inmediatamente
   ↓
Tiempo +30min: Han pasado 30 minutos
   ↓
   📧 Recordatorio enviado
   ↓
Tiempo +60min: Ha pasado 1 hora
   ↓
   📧 Ultimátum enviado
```

### Ejemplo Real

```
10:00 AM - Llega reserva de WALVIS S.A.
10:00 AM - ✅ Solicitud inicial enviada
10:30 AM - ✅ Recordatorio enviado (30 min después)
11:00 AM - ✅ Ultimátum enviado (1 hora después)
```

## 🔍 Testing del Sistema

### Probar el Flujo Completo

```bash
# 1. Enviar correo de prueba
PYTHONPATH=. python scripts/utils/enviar_prueba.py

# 2. Ver reserva creada
sqlite3 data/oc_seguimiento.db "
SELECT
    id_reserva,
    agencia,
    datetime(email_origen_fecha) as fecha_inicio,
    estado_oc
FROM reservas
WHERE estado_oc = 'PENDIENTE'
ORDER BY fecha_creacion DESC
LIMIT 1;
"

# 3. Esperar 30 minutos y verificar logs
tail -f logs/oc_seguimiento_*.log | grep "recordatorio"

# 4. Esperar 60 minutos (total) y verificar logs
tail -f logs/oc_seguimiento_*.log | grep "ultimatum"
```

### Verificar Minutos Transcurridos

```bash
# Script rápido para ver minutos transcurridos
PYTHONPATH=. python -c "
from database import init_db, get_db, Reserva
init_db()
db = next(get_db())
reserva = db.query(Reserva).filter_by(estado_oc='PENDIENTE').first()
if reserva:
    print(f'Reserva: {reserva.id_reserva}')
    print(f'Minutos transcurridos: {reserva.minutos_desde_creacion}')
    print(f'Necesita recordatorio (30min): {reserva.necesita_recordatorio_dia2}')
    print(f'Necesita ultimátum (60min): {reserva.necesita_ultimatum_dia4}')
"
```

### Monitorear Envíos

```bash
# Ver todos los correos enviados de una reserva
sqlite3 data/oc_seguimiento.db "
SELECT
    r.id_reserva,
    c.tipo_correo,
    c.estado,
    datetime(c.fecha_enviado) as enviado,
    (julianday(c.fecha_enviado) - julianday(r.email_origen_fecha)) * 24 * 60 as minutos_desde_inicio
FROM correos_enviados c
JOIN reservas r ON c.reserva_id = r.id
WHERE r.id_reserva = 'TU_ID_RESERVA'
ORDER BY c.fecha_enviado;
"
```

## 🔄 Cómo Volver a Modo Producción

Para cambiar de **Modo Pruebas** a **Modo Producción**, seguir estos pasos:

### Paso 1: Editar `database.py`

**Comentar las propiedades de prueba (líneas 170-197)**:
```python
# ============================================================================
# MODO PRUEBAS - Recordatorios por minutos (COMENTADO)
# ============================================================================
# @property
# def necesita_recordatorio_dia2(self) -> bool:
#     """MODO PRUEBAS: 30 minutos"""
#     return (
#         self.requiere_oc
#         and self.estado_oc == EstadoOC.PENDIENTE
#         and self.minutos_desde_creacion >= 30
#         and not any(c.tipo_correo == TipoCorreo.RECORDATORIO_DIA_2 for c in self.correos_enviados)
#     )
#
# @property
# def necesita_ultimatum_dia4(self) -> bool:
#     """MODO PRUEBAS: 60 minutos"""
#     return (
#         self.requiere_oc
#         and self.estado_oc == EstadoOC.PENDIENTE
#         and self.minutos_desde_creacion >= 60
#         and not any(c.tipo_correo == TipoCorreo.ULTIMATUM_DIA_4 for c in self.correos_enviados)
#     )
```

**Descomentar las propiedades de producción (líneas 147-168)**:
```python
# ============================================================================
# MODO PRODUCCIÓN - Recordatorios por días (ACTIVO)
# ============================================================================
@property
def necesita_recordatorio_dia2(self) -> bool:
    """Verifica si necesita recordatorio día 2"""
    return (
        self.requiere_oc
        and self.estado_oc == EstadoOC.PENDIENTE
        and self.dias_desde_creacion >= 2
        and not any(c.tipo_correo == TipoCorreo.RECORDATORIO_DIA_2 for c in self.correos_enviados)
    )

@property
def necesita_ultimatum_dia4(self) -> bool:
    """Verifica si necesita ultimátum día 4"""
    return (
        self.requiere_oc
        and self.estado_oc == EstadoOC.PENDIENTE
        and self.dias_desde_creacion >= 4
        and not any(c.tipo_correo == TipoCorreo.ULTIMATUM_DIA_4 for c in self.correos_enviados)
    )
```

### Paso 2: Reiniciar el Sistema

```bash
# Detener
./scripts/gestion/gestionar_sistema.sh stop

# Iniciar
./scripts/gestion/gestionar_sistema.sh start
```

### Paso 3: Verificar

```bash
# Ver logs para confirmar modo
tail -f logs/oc_seguimiento_*.log | grep -E "recordatorio|ultimatum"
```

## ⚙️ Personalizar Periodos de Prueba

Si quieres cambiar los periodos de prueba, editar `database.py`:

### Cambiar a 10 minutos y 20 minutos

```python
@property
def necesita_recordatorio_dia2(self) -> bool:
    return (
        self.requiere_oc
        and self.estado_oc == EstadoOC.PENDIENTE
        and self.minutos_desde_creacion >= 10  # Cambiar a 10 minutos
        and not any(c.tipo_correo == TipoCorreo.RECORDATORIO_DIA_2 for c in self.correos_enviados)
    )

@property
def necesita_ultimatum_dia4(self) -> bool:
    return (
        self.requiere_oc
        and self.estado_oc == EstadoOC.PENDIENTE
        and self.minutos_desde_creacion >= 20  # Cambiar a 20 minutos
        and not any(c.tipo_correo == TipoCorreo.ULTIMATUM_DIA_4 for c in self.correos_enviados)
    )
```

### Cambiar a horas

```python
@property
def necesita_recordatorio_dia2(self) -> bool:
    return (
        self.requiere_oc
        and self.estado_oc == EstadoOC.PENDIENTE
        and self.minutos_desde_creacion >= 120  # 2 horas
        and not any(c.tipo_correo == TipoCorreo.RECORDATORIO_DIA_2 for c in self.correos_enviados)
    )
```

## 📊 Dashboard y Visualización

El dashboard mostrará los minutos transcurridos en modo pruebas:

```bash
# Acceder al dashboard
open http://localhost:8001/reservas
```

**Nota**: La columna "Días" seguirá mostrando días (0 o 1 típicamente en pruebas), pero los correos se enviarán según minutos.

## ⚠️ Advertencias

### 1. No Usar en Producción

El modo pruebas NO debe usarse en producción porque:
- ✅ Útil para testing rápido
- ❌ Enviará correos muy frecuentemente
- ❌ Puede molestar a clientes reales
- ❌ No refleja el flujo real del negocio

### 2. Limpiar Datos de Prueba

Después de hacer pruebas, limpiar la BD:

```bash
# Eliminar reservas de prueba
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --test

# O eliminar todas
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --all
```

### 3. Scheduler Activo

El scheduler debe estar corriendo para que los correos se envíen:

```bash
# Verificar que está activo
./scripts/gestion/gestionar_sistema.sh status
```

El scheduler verifica cada cierto tiempo (configurado en `SCHEDULER_CHECKS_PER_DAY` o intervalo de scheduler).

## 📝 Archivo Modificado

```
✏️  database.py (líneas 129-197)
    - Agregada propiedad minutos_desde_creacion
    - Comentadas propiedades de producción
    - Activadas propiedades de prueba con minutos
```

## 🔗 Referencias

- **Scheduler**: `src/scheduler.py`
- **Email Sender**: `src/email_sender.py`
- **Configuración**: `config.py`
- **Dashboard**: http://localhost:8001

---

**Versión del documento**: 1.0
**Modo actual**: PRUEBAS (30min/60min)
**Para producción**: Seguir pasos en sección "Cómo Volver a Modo Producción"

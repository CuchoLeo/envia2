# Resumen de Cambios - Versión 1.3.4

**Fecha**: 9 de Diciembre de 2024
**Desarrollador**: CuchoLeo
**Feature**: Usar Fecha de Emisión del PDF como día 0 del flujo

---

## 🎯 Objetivo del Cambio

Cambiar la lógica del sistema para que el **"Día 0" del flujo de seguimiento de OC** se calcule desde la **Fecha de Emisión** indicada en el PDF de confirmación, en lugar de la fecha en que llegó el correo.

### Beneficio

Si un PDF fue emitido el **5 de diciembre** pero el correo llega el **9 de diciembre**, el sistema ahora considerará que han transcurrido **4 días** en lugar de **0 días**, lo que refleja mejor el tiempo real desde que se emitió la reserva.

---

## ✅ Cambios Implementados

### 1. Base de Datos (`database.py`)

**Archivo**: `database.py`

**Cambio en línea 102**:
```python
# ANTES: Campo de texto
fecha_emision = Column(String(50), nullable=True)

# DESPUÉS: Campo de fecha/hora
fecha_emision = Column(DateTime, nullable=True)  # Fecha de emisión del PDF (día 0 del flujo)
```

**Cambio en propiedad `dias_desde_creacion` (líneas 116-127)**:
```python
@property
def dias_desde_creacion(self) -> int:
    """
    Calcula días desde la fecha de emisión del PDF (día 0 del flujo)
    Fallback: fecha del correo, o fecha de creación en BD
    """
    # NUEVA LÓGICA: Prioridad fecha_emision > email_origen_fecha > fecha_creacion
    fecha_referencia = self.fecha_emision or self.email_origen_fecha or self.fecha_creacion
    return (datetime.utcnow() - fecha_referencia).days
```

### 2. Procesador de PDF (`src/pdf_processor.py`)

**Archivo**: `src/pdf_processor.py`

**Cambio en líneas 133-147**:
- Ahora detecta si el campo dice **"INMEDIATO"** o está vacío → retorna `None`
- Si tiene una fecha válida → la parsea a `datetime`
- Si no puede parsear → retorna `None` (antes usaba `datetime.now()`)
- Logs mejorados para indicar qué fecha se está usando

```python
if fecha_emision_str.upper() == "INMEDIATO" or not fecha_emision_str:
    data['fecha_emision'] = None
    self.logger.info(f"📅 Fecha emisión: INMEDIATO - se usará fecha de llegada del correo")
else:
    data['fecha_emision'] = self._parse_spanish_date(fecha_emision_str)
    if data['fecha_emision']:
        self.logger.info(f"📅 Fecha emisión extraída: {data['fecha_emision']}")
```

### 3. Monitor de Email (`src/email_monitor.py`)

**Archivo**: `src/email_monitor.py`

**Sin cambios** - Ya estaba guardando correctamente el campo `fecha_emision` en línea 279.

### 4. Documentación

**Archivos actualizados**:

1. **`docs/FLUJO_DETALLADO_SISTEMA.md`** (líneas 533-560)
   - Actualizada sección "CÁLCULO DE días_desde_creacion"
   - Agregados ejemplos con fecha de emisión
   - Documentados casos especiales ("INMEDIATO", fecha no parseable, etc.)

2. **`README.md`** (línea 5-11)
   - Actualizado número de versión a 1.3.4
   - Agregado aviso sobre nueva feature

3. **`docs/CHANGELOG_FECHA_EMISION.md`** (NUEVO)
   - Documentación técnica completa del cambio
   - Ejemplos de uso
   - Guía de migración
   - Testing

4. **`RESUMEN_CAMBIOS_v1.3.4.md`** (NUEVO - este archivo)
   - Resumen ejecutivo de todos los cambios

---

## 🔄 Lógica del Sistema (Nueva)

### Prioridad de Fechas

El sistema ahora calcula `dias_desde_creacion` con la siguiente prioridad:

1. **`fecha_emision`** (del PDF) - Si está disponible y no es "INMEDIATO"
2. **`email_origen_fecha`** - Fecha en que llegó el correo
3. **`fecha_creacion`** - Fecha de creación del registro en BD

### Casos de Uso

| Caso | Fecha Emisión PDF | Email Llega | Día 0 Usado | Observación |
|------|-------------------|-------------|-------------|-------------|
| Normal | 5 dic 2024 | 9 dic 2024 | **5 dic** | Usa fecha del PDF |
| INMEDIATO | "INMEDIATO" | 9 dic 2024 | **9 dic** | Usa fecha del email |
| Vacío | (vacío) | 9 dic 2024 | **9 dic** | Usa fecha del email |
| Error formato | "Texto inválido" | 9 dic 2024 | **9 dic** | Usa fecha del email |

---

## 📋 Archivos Modificados

```
✏️  database.py                         (2 cambios)
✏️  src/pdf_processor.py                (1 cambio)
✏️  docs/FLUJO_DETALLADO_SISTEMA.md     (1 sección actualizada)
✏️  README.md                           (versión + aviso)
📄  docs/CHANGELOG_FECHA_EMISION.md     (NUEVO)
📄  RESUMEN_CAMBIOS_v1.3.4.md          (NUEVO - este archivo)
```

**Total**: 4 archivos modificados, 2 archivos nuevos

---

## ⚠️ Consideraciones Importantes

### 1. Base de Datos Existente

**Problema**: Las reservas creadas antes de este cambio tienen `fecha_emision` como String, no DateTime.

**Opciones**:

#### Opción A: Limpiar reservas de prueba (Recomendado para desarrollo)
```bash
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --all
```

#### Opción B: Recrear base de datos (Solo desarrollo)
```bash
rm data/oc_seguimiento.db
PYTHONPATH=. python scripts/database/crear_bd.py
PYTHONPATH=. python scripts/database/cargar_clientes_excel.py
```

#### Opción C: Crear script de migración (Para producción)
- Convertir valores String existentes a DateTime
- O establecer `fecha_emision=None` para registros antiguos

### 2. Sistema Actualmente Activo

**Estado actual**: ✅ Sistema ACTIVO (PIDs: 19165, 86958)

**Antes de probar los cambios**:
```bash
# Detener sistema actual
./scripts/gestion/gestionar_sistema.sh stop

# Limpiar/recrear BD si es necesario (ver opciones arriba)

# Reiniciar sistema con cambios
./scripts/gestion/gestionar_sistema.sh start
```

---

## 🧪 Plan de Testing

### 1. Test con PDF de Prueba

```bash
# 1. Generar PDF con fecha de emisión
PYTHONPATH=. python scripts/testing/generar_pdf_prueba.py

# 2. Enviar correo de prueba
PYTHONPATH=. python scripts/utils/enviar_prueba.py

# 3. Verificar en dashboard
open http://localhost:8001/reservas

# 4. Revisar logs
tail -f logs/sistema.log | grep "📅"
```

### 2. Verificar en Logs

Deberías ver uno de estos mensajes:

```
📅 Fecha emisión extraída: 2024-12-05 00:00:00
```

O:

```
📅 Fecha emisión: INMEDIATO - se usará fecha de llegada del correo
```

### 3. Verificar Cálculo de Días

En el dashboard (`http://localhost:8001/reservas`), la columna **"Días"** debería mostrar:
- Días desde `fecha_emision` (si está disponible)
- Días desde `email_origen_fecha` (si fecha_emision es NULL o INMEDIATO)

### 4. Test Cases

| Test | Fecha Emisión en PDF | Resultado Esperado |
|------|---------------------|-------------------|
| 1 | Fecha válida (5 dic) | `dias_desde_creacion` se calcula desde 5 dic |
| 2 | "INMEDIATO" | `dias_desde_creacion` se calcula desde fecha del email |
| 3 | Campo vacío | `dias_desde_creacion` se calcula desde fecha del email |
| 4 | Formato incorrecto | `dias_desde_creacion` se calcula desde fecha del email |

---

## 📊 Impacto en Flujo de Seguimiento

### Antes (v1.3.3)

```
5 dic: PDF emitido
9 dic: Email llega al sistema
  └─► DÍA 0 = 9 dic  ← Empezaba desde acá
11 dic: DÍA 2 → Recordatorio
13 dic: DÍA 4 → Ultimátum
```

### Después (v1.3.4)

```
5 dic: PDF emitido
  └─► DÍA 0 = 5 dic  ← Ahora empieza desde acá
7 dic: DÍA 2 → Recordatorio
9 dic: DÍA 4 → Ultimátum (mismo día que llega el email)
```

**Ventaja**: El cliente tiene menos tiempo para enviar la OC desde que recibe el email, pero el tiempo total desde la emisión de la reserva es el mismo.

---

## 📝 Próximos Pasos

### 1. Testing (REQUERIDO antes de producción)

- [ ] Detener sistema actual
- [ ] Limpiar/recrear base de datos
- [ ] Reiniciar sistema
- [ ] Enviar PDF de prueba con fecha de emisión
- [ ] Verificar que `dias_desde_creacion` se calcula correctamente
- [ ] Probar caso "INMEDIATO"
- [ ] Verificar logs

### 2. Actualizar Repositorio

```bash
# Agregar archivos modificados
git add database.py src/pdf_processor.py
git add docs/FLUJO_DETALLADO_SISTEMA.md docs/CHANGELOG_FECHA_EMISION.md
git add README.md RESUMEN_CAMBIOS_v1.3.4.md

# Commit
git commit -m "v1.3.4: Usar fecha de emisión del PDF como día 0 del flujo

- database.py: Cambiar fecha_emision de String a DateTime
- database.py: Actualizar dias_desde_creacion para priorizar fecha_emision
- pdf_processor.py: Manejar casos INMEDIATO y fechas inválidas
- docs: Actualizar FLUJO_DETALLADO_SISTEMA.md con nueva lógica
- docs: Agregar CHANGELOG_FECHA_EMISION.md con documentación técnica
- README.md: Actualizar versión a 1.3.4"

# Push
git push origin main
```

### 3. Validación en Producción (Si aplica)

- [ ] Crear backup de base de datos actual
- [ ] Probar en ambiente de staging primero
- [ ] Migrar datos existentes (si es necesario)
- [ ] Deploy a producción
- [ ] Monitorear logs por 24-48 horas

---

## 🔍 Debugging

### Ver qué fecha está usando el sistema

```bash
# Conectar a base de datos
sqlite3 data/oc_seguimiento.db

# Ver fechas de una reserva
SELECT
    id_reserva,
    fecha_emision,
    email_origen_fecha,
    fecha_creacion
FROM reservas
WHERE id_reserva = 'TEST2024001';

# Salir
.quit
```

### Ver logs en tiempo real

```bash
# Todos los logs
./scripts/gestion/gestionar_sistema.sh logs

# Solo logs de fecha de emisión
tail -f logs/sistema.log | grep "📅"

# Solo logs de procesamiento de PDF
tail -f logs/sistema.log | grep "PDFProcessor"
```

---

## 📚 Referencias

- **Documentación técnica completa**: `docs/CHANGELOG_FECHA_EMISION.md`
- **Flujo detallado del sistema**: `docs/FLUJO_DETALLADO_SISTEMA.md`
- **Guía de inicio rápido**: `docs/inicio-rapido/INICIO_RAPIDO.md`
- **Issue original**: "Usar 'Fecha Emisión' del PDF como fecha inicial del flujo"

---

## ✅ Checklist de Implementación

- [x] Cambiar tipo de campo `fecha_emision` en `database.py`
- [x] Actualizar propiedad `dias_desde_creacion`
- [x] Modificar `pdf_processor.py` para manejar "INMEDIATO"
- [x] Actualizar documentación en `FLUJO_DETALLADO_SISTEMA.md`
- [x] Actualizar `README.md` con nueva versión
- [x] Crear `CHANGELOG_FECHA_EMISION.md`
- [x] Crear este resumen
- [ ] **Testing con PDFs de prueba**
- [ ] Commit y push a repositorio
- [ ] Validar en ambiente real

---

**Versión del documento**: 1.0
**Autor**: Claude Code (asistente de CuchoLeo)
**Fecha**: 9 de Diciembre de 2024

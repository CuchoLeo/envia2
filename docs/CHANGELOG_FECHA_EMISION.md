# Cambio: Usar Fecha Emisión del PDF como Día 0 del Flujo

**Fecha**: 9 de Diciembre de 2024
**Versión**: 1.3.4

## Resumen

El sistema ahora utiliza el campo "Fecha Emisión" extraído del PDF de confirmación como punto de partida (día 0) para calcular los días transcurridos en el flujo de seguimiento de OC.

## Cambios Realizados

### 1. Modelo de Base de Datos (`database.py`)

**Cambio en línea 102:**
```python
# ANTES:
fecha_emision = Column(String(50), nullable=True)

# DESPUÉS:
fecha_emision = Column(DateTime, nullable=True)  # Fecha de emisión del PDF (día 0 del flujo)
```

**Cambio en propiedad `dias_desde_creacion` (líneas 116-127):**
```python
@property
def dias_desde_creacion(self) -> int:
    """
    Calcula días desde la fecha de emisión del PDF (día 0 del flujo)
    Fallback: fecha del correo, o fecha de creación en BD
    - Día 0: Fecha de emisión del PDF (o llegada del correo si no está disponible)
    - Día 2: Primer recordatorio
    - Día 4: Ultimátum
    """
    # Prioridad: fecha_emision del PDF > fecha del correo > fecha de creación en BD
    fecha_referencia = self.fecha_emision or self.email_origen_fecha or self.fecha_creacion
    return (datetime.utcnow() - fecha_referencia).days
```

### 2. Procesador de PDF (`src/pdf_processor.py`)

**Cambio en líneas 133-147:**
```python
# Extraer Fecha de Emisión
fecha_emision_match = re.search(r'Fecha\s+Emision:\s*([^\n]+)', text, re.IGNORECASE)
if fecha_emision_match:
    fecha_emision_str = fecha_emision_match.group(1).strip()
    # Si dice "INMEDIATO" o está vacío, usar None (se usará fecha del correo como fallback)
    if fecha_emision_str.upper() == "INMEDIATO" or not fecha_emision_str:
        data['fecha_emision'] = None
        self.logger.info(f"📅 Fecha emisión: INMEDIATO - se usará fecha de llegada del correo")
    else:
        # Intentar parsear la fecha, si falla guardar como None
        data['fecha_emision'] = self._parse_spanish_date(fecha_emision_str)
        if data['fecha_emision']:
            self.logger.info(f"📅 Fecha emisión extraída: {data['fecha_emision']}")
        else:
            self.logger.warning(f"⚠️  No se pudo parsear fecha emisión: {fecha_emision_str}")
```

### 3. Monitor de Email (`src/email_monitor.py`)

**Sin cambios necesarios** - Ya estaba guardando correctamente el campo en línea 279:
```python
fecha_emision=pdf_data.get('fecha_emision'),
```

## Lógica del Sistema

### Prioridad de Fechas para Cálculo de Días

El sistema ahora usa la siguiente jerarquía para determinar el "día 0" del flujo:

1. **`fecha_emision`** (del PDF) - Si está disponible y no es "INMEDIATO"
2. **`email_origen_fecha`** - Fecha en que llegó el correo de confirmación
3. **`fecha_creacion`** - Fecha de creación del registro en BD (último recurso)

### Casos de Uso

#### Caso 1: PDF con Fecha Emisión Válida
```
Fecha Emisión PDF: 5 de Diciembre de 2024
Email llega: 6 de Diciembre de 2024
Día 0 del flujo: 5 de Diciembre ← Se usa fecha del PDF
```

#### Caso 2: PDF con "INMEDIATO"
```
Fecha Emisión PDF: "INMEDIATO"
Email llega: 6 de Diciembre de 2024
Día 0 del flujo: 6 de Diciembre ← Se usa fecha del correo
```

#### Caso 3: PDF sin Fecha Emisión
```
Fecha Emisión PDF: (vacío)
Email llega: 6 de Diciembre de 2024
Día 0 del flujo: 6 de Diciembre ← Se usa fecha del correo
```

#### Caso 4: PDF con Fecha No Parseable
```
Fecha Emisión PDF: "Texto inválido"
Email llega: 6 de Diciembre de 2024
Día 0 del flujo: 6 de Diciembre ← Se usa fecha del correo
```

## Flujo de Seguimiento

Con la nueva lógica, el flujo de recordatorios se calcula desde la fecha de emisión del PDF:

```
DÍA 0  - Fecha Emisión del PDF (o llegada del correo si no disponible)
  ↓
DÍA 2  - Primer recordatorio (si no se ha recibido OC)
  ↓
DÍA 4  - Ultimátum (si aún no se ha recibido OC)
  ↓
DÍA 5+ - Estado EXPIRADA (opcional, según configuración)
```

## Impacto en Reservas Existentes

### ⚠️ Importante: Migración de Datos

Las reservas creadas **antes** de este cambio tienen `fecha_emision` como String. Esto puede causar problemas al actualizar la base de datos.

### Opciones:

1. **Limpiar reservas de prueba** (recomendado para desarrollo):
   ```bash
   PYTHONPATH=. python scripts/database/limpiar_base_datos.py --all
   ```

2. **Migrar datos existentes** (para producción):
   - Crear script de migración que convierta String a DateTime
   - O establecer `fecha_emision=None` para todas las reservas antiguas

3. **Recrear base de datos** (solo desarrollo):
   ```bash
   rm data/oc_seguimiento.db
   PYTHONPATH=. python scripts/database/crear_bd.py
   ```

## Testing

### Probar con PDF de Ejemplo

```bash
# Generar PDF de prueba con fecha de emisión
PYTHONPATH=. python scripts/testing/generar_pdf_prueba.py

# Enviar correo de prueba
PYTHONPATH=. python scripts/utils/enviar_prueba.py
```

### Verificar en Dashboard

1. Acceder a http://localhost:8001/reservas
2. Verificar que la columna "Días" se calcula desde la fecha de emisión del PDF
3. Comprobar logs para ver qué fecha se está usando

### Verificar en Logs

```bash
tail -f logs/sistema.log | grep "📅"
```

Deberías ver:
```
📅 Fecha emisión extraída: 2024-12-05 00:00:00
```

O:
```
📅 Fecha emisión: INMEDIATO - se usará fecha de llegada del correo
```

## Compatibilidad con Versiones Anteriores

- ✅ **Email Monitor**: Compatible - ya guardaba el campo
- ✅ **PDF Processor**: Compatible - ahora maneja mejor los casos especiales
- ⚠️ **Base de Datos**: Requiere migración o limpieza de datos antiguos
- ✅ **Scheduler**: Compatible - usa la propiedad `dias_desde_creacion`
- ✅ **Dashboard**: Compatible - usa la propiedad `dias_desde_creacion`

## Beneficios

1. **Mayor Precisión**: El flujo ahora se basa en la fecha real de emisión del servicio, no en cuándo llegó el correo
2. **Flexibilidad**: Maneja correctamente casos de envíos retrasados
3. **Transparencia**: Los logs muestran claramente qué fecha se está usando
4. **Fallback Robusto**: Si no hay fecha de emisión, el sistema sigue funcionando usando la fecha del correo

## Próximos Pasos

1. ✅ Implementar cambios en código
2. ⏳ Probar con datos de ejemplo
3. ⏳ Actualizar documentación principal
4. ⏳ Crear script de migración (si es necesario)
5. ⏳ Actualizar CHANGELOG.md principal
6. ⏳ Commit y push a repositorio

---

**Nota**: Este documento describe los cambios técnicos. Para la guía de usuario, ver `docs/GUIA_USO.md`.

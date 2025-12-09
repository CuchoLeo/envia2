# Documentación Deprecada

Esta carpeta contiene documentación que ya no es relevante para la versión actual del sistema, pero se mantiene como referencia histórica.

**Fecha de Deprecación**: Diciembre 2025
**Versión Actual del Sistema**: 1.2.0

---

## 📄 Documentos Deprecados

### `COMPARACION_PYTHON_VS_N8N.md`

**Deprecado en**: v1.2.0 (Diciembre 2025)
**Razón**: El sistema ya no ofrece implementación con n8n

**Contenido**: Comparativa entre implementación Python/FastAPI vs n8n (solución visual sin código)

**Por qué se deprecó**:
- El equipo optó por la implementación Python/FastAPI exclusivamente
- n8n requería dependencias adicionales (Node.js, PostgreSQL obligatorio)
- La solución Python/FastAPI demostró ser más flexible y mantenible
- No hay planes de mantener la versión n8n

**Referencia histórica**: Este documento es útil para entender las decisiones de arquitectura iniciales del proyecto.

---

### `MIGRACION_OFFICE365.md`

**Deprecado en**: v1.2.0 (Diciembre 2025)
**Razón**: Se mantuvo Gmail, no se realizó la migración a Office 365

**Contenido**: Guía de migración de Gmail a Office 365 (cuenta controloc@hotelsales.cl)

**Por qué se deprecó**:
- Después de pruebas, se decidió mantener Gmail como proveedor de correo
- La cuenta `seguimientoocx@gmail.com` demostró ser suficiente y estable
- Office 365 requería configuración adicional sin beneficios tangibles
- Gmail App Passwords funcionan perfectamente para el caso de uso

**Estado actual**: El sistema sigue usando Gmail con las siguientes cuentas:
- **Monitoreo**: `seguimientoocx@gmail.com`
- **Envío**: `seguimientoocx@gmail.com`
- **OC Inbox**: `seguimientoocx@gmail.com`

**Nota**: Si en el futuro se requiere migrar a Office 365 u otro proveedor corporativo, este documento puede servir como punto de partida.

---

## ⚠️ Uso de Documentos Deprecados

Estos documentos **NO DEBEN usarse** como referencia para la implementación actual del sistema.

Si necesitas información actualizada, consulta:
- **README.md principal** en la raíz del proyecto
- **docs/** para documentación actualizada
- **CHANGELOG.md** para historial de cambios
- **ALCANCE_PROYECTO.md** para alcance completo

---

## 📚 Documentación Actual Recomendada

Para la versión actual del sistema (v1.2.0), consulta:

| Documento | Ubicación | Propósito |
|-----------|-----------|-----------|
| **README.md** | `/README.md` | Documentación principal del sistema |
| **ALCANCE_PROYECTO.md** | `/ALCANCE_PROYECTO.md` | Alcance completo del proyecto |
| **CHANGELOG.md** | `/CHANGELOG.md` | Historial de cambios versión por versión |
| **DIAGRAMAS.md** | `/DIAGRAMAS.md` | Diagramas de arquitectura |
| **Arquitecturas GCP** | `/docs/COMPARATIVA_ARQUITECTURAS_GCP.md` | Despliegue en la nube |
| **Configuración Gmail** | `/docs/CONFIGURACION_GMAIL.md` | Setup de Gmail actual |
| **Flujo del Sistema** | `/docs/FLUJO_SISTEMA.md` | Flujo completo del sistema |

---

## 🗂️ Historial de Deprecaciones

| Fecha | Documento | Versión | Razón |
|-------|-----------|---------|-------|
| 2025-12-07 | `COMPARACION_PYTHON_VS_N8N.md` | v1.2.0 | No se usa n8n |
| 2025-12-07 | `MIGRACION_OFFICE365.md` | v1.2.0 | Se mantuvo Gmail |

---

**Última Actualización**: Diciembre 2025

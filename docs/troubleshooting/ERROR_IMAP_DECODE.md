# Error: 'int' object has no attribute 'decode'

**Error completo**:
```
ERROR | src.imap_wrapper:fetch_message | Error obteniendo mensaje X: 'int' object has no attribute 'decode'
```

## 🐛 Descripción del Problema

Este error ocurre cuando el sistema intenta obtener un mensaje del servidor IMAP y el servidor retorna datos en un formato inesperado. Típicamente sucede cuando:

1. Un mensaje está corrupto o malformado
2. El mensaje tiene un formato muy antiguo o no estándar
3. Hay problemas de sincronización con el servidor IMAP
4. El mensaje fue eliminado mientras se procesaba

## ✅ Solución (v1.3.1+)

Este error **ya está corregido** en la versión 1.3.1 del sistema.

### Qué se corrigió:

El código ahora valida robustamente los datos antes de procesarlos:

1. **Verifica que `data` no esté vacío**
   ```python
   if not data or len(data) == 0:
       return None
   ```

2. **Valida el formato de datos**
   ```python
   if not isinstance(data[0], tuple) or len(data[0]) < 2:
       return None
   ```

3. **Verifica el tipo de datos**
   ```python
   if not isinstance(raw_email, bytes):
       return None
   ```

4. **Registra información detallada** para debugging

## 🧪 Verificar la Corrección

### 1. Ejecutar Script de Diagnóstico

```bash
python scripts/testing/test_imap_fetch.py
```

Este script:
- Conecta al servidor IMAP
- Busca mensajes no leídos
- Intenta fetch de los primeros 5 mensajes
- Reporta éxitos y errores

### 2. Ver Logs Detallados

```bash
tail -f logs/sistema.log
```

Busca líneas como:
- `FETCH retornó data vacío para mensaje X`
- `FETCH retornó formato inesperado para mensaje X`
- `FETCH retornó tipo inesperado para mensaje X`

## 🔧 Qué Hacer si el Error Persiste

### Si el error ocurre en un mensaje específico:

1. **Identifica el mensaje problemático**
   - Revisa los logs para ver el `message_id`

2. **Marca el mensaje como leído manualmente**
   ```bash
   # Desde Gmail: Abre el correo y márcalo como leído
   ```

3. **O elimínalo si es spam/corrupto**
   ```bash
   # Desde Gmail: Elimina el correo problemático
   ```

### Si el error ocurre con múltiples mensajes:

1. **Verifica la conexión IMAP**
   ```bash
   python scripts/utils/test_conexion.py
   ```

2. **Revisa las credenciales**
   - Verifica `.env`: `IMAP_USERNAME` y `IMAP_PASSWORD`
   - Asegúrate de usar contraseña de aplicación de Gmail

3. **Limpia la bandeja de entrada**
   - Elimina correos muy antiguos o sospechosos
   - Vacía la papelera

## 📋 Logs de Ejemplo

### Antes de la corrección (v1.3.0):

```
2025-12-09 10:00:46 | ERROR | src.imap_wrapper:fetch_message | Error obteniendo mensaje 37: 'int' object has no attribute 'decode'
```

### Después de la corrección (v1.3.1):

```
2025-12-09 10:00:46 | WARNING | src.imap_wrapper:fetch_message | FETCH retornó formato inesperado para mensaje 37: <class 'int'>
2025-12-09 10:00:46 | INFO | src.email_monitor | Saltando mensaje 37 (formato inválido), continuando con siguiente...
```

## 🔍 Información Técnica

### Causa Raíz

El servidor IMAP a veces retorna datos en formatos inesperados:

```python
# Formato esperado:
data = [(flags, b'raw email bytes'), ...]

# Formato que causa error (cuando mensaje es inválido):
data = [(flags, 37), ...]  # <- El número del mensaje en lugar de bytes
```

### Validación Implementada

```python
def fetch_message(self, message_id: int):
    status, data = self.client.fetch(str(message_id), '(BODY.PEEK[])')

    # 1. Validar que data existe
    if not data or len(data) == 0:
        logger.warning(f"FETCH retornó data vacío para mensaje {message_id}")
        return None

    # 2. Validar formato tupla
    if not isinstance(data[0], tuple) or len(data[0]) < 2:
        logger.warning(f"FETCH retornó formato inesperado: {type(data[0])}")
        return None

    # 3. Validar tipo bytes
    raw_email = data[0][1]
    if not isinstance(raw_email, bytes):
        logger.error(f"FETCH retornó tipo inesperado: {type(raw_email)}")
        return None

    # 4. Ahora es seguro parsear
    msg = BytesParser(policy=policy.default).parsebytes(raw_email)
```

## 📚 Referencias

- **Archivo modificado**: `src/imap_wrapper.py` (líneas 157-251)
- **CHANGELOG**: Ver sección v1.3.1
- **Script de prueba**: `scripts/testing/test_imap_fetch.py`
- **Issue relacionado**: Error crítico IMAP fetch

## ✅ Resumen

| Aspecto | Detalle |
|---------|---------|
| **Error** | 'int' object has no attribute 'decode' |
| **Versión afectada** | v1.3.0 y anteriores |
| **Versión corregida** | v1.3.1+ (9 de Diciembre de 2024) |
| **Severidad** | Alta (causaba crashes del monitor) |
| **Estado** | ✅ Resuelto |
| **Acción requerida** | Actualizar a v1.3.1+ |

---

**Última actualización**: 9 de Diciembre de 2024
**Versión del sistema**: 1.3.1

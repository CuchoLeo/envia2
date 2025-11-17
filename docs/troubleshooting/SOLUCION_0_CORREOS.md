# 🔍 Solución: Sistema encuentra 0 correos

## ✅ Correcciones Implementadas

He mejorado el sistema de reconexión IMAP para resolver los errores NONAUTH que aparecían en los logs.

### 1. Mejoras en `imap_wrapper.py`

**Problema anterior:** El cliente IMAP perdía la conexión y no se reconectaba correctamente.

**Solución:**
- ✅ Mejorado `_ensure_connected()` para manejar cuando el cliente es None
- ✅ Agregado limpieza del cliente antes de reconectar
- ✅ Mejorado manejo de errores en `search_unseen()`
- ✅ Agregados más logs de debug para rastrear problemas

### 2. Creado script de diagnóstico completo

**Nuevo archivo:** `diagnose_imap.py`

Este script realiza un diagnóstico completo de tu conexión IMAP y te muestra:
- ✅ Estado de la conexión
- ✅ Todas las carpetas disponibles
- ✅ Estadísticas de INBOX (total, leídos, no leídos)
- ✅ Últimos 5 mensajes recibidos
- ✅ Búsqueda específica de mensajes no leídos
- ✅ Estado de conexión después de operaciones

---

## 🚀 Próximos Pasos

### 1️⃣ Ejecuta el Diagnóstico Completo

```bash
python diagnose_imap.py
```

Este comando te mostrará exactamente qué está pasando con tu cuenta de correo.

### 2️⃣ Interpreta los Resultados

#### ✅ Si el diagnóstico muestra mensajes no leídos:

El problema está en el loop de monitoreo. Verifica:
```bash
# Ver logs en tiempo real
tail -f logs/oc_seguimiento_*.log
```

#### ⚠️ Si muestra 0 mensajes no leídos:

Esto significa que NO hay correos sin leer en INBOX. Necesitas:

**A. Enviar un correo de prueba:**
```bash
python enviar_prueba.py
```

**B. Verificar que el correo llegó a INBOX:**
- Abre Gmail en el navegador
- Ve a INBOX (no Promociones, no Social)
- Verifica que el correo esté marcado como NO LEÍDO (negrita)

**C. Gmail puede estar clasificando los correos automáticamente:**
- Los correos pueden estar yendo a "Promociones" o "Social"
- En Gmail web, arrastra un correo de prueba a INBOX principal
- Crea un filtro para que futuros correos vayan directo a INBOX:
  1. Gmail → Configuración → Filtros y direcciones bloqueadas
  2. Crear filtro nuevo
  3. "De": tu correo de pruebas
  4. "Aplicar etiqueta": INBOX
  5. "No enviarlo nunca a Spam": ✓
  6. Crear filtro

### 3️⃣ Si Sigue Sin Funcionar

#### Revisa tu archivo `.env`:

```bash
cat .env | grep IMAP
```

Debe mostrar algo como:
```
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=tu-cuenta@gmail.com
IMAP_PASSWORD=tu_password_app_16_caracteres
IMAP_USE_SSL=true
```

#### Verifica que IMAP esté habilitado en Gmail:

1. Abre Gmail en navegador
2. Click en ⚙️ (Configuración)
3. "Ver toda la configuración"
4. Pestaña "Reenvío y correo POP/IMAP"
5. "Habilitar IMAP" debe estar seleccionado
6. Guardar cambios

#### Regenera la contraseña de aplicación:

1. Ve a: https://myaccount.google.com/apppasswords
2. Genera nueva contraseña (selecciona "Correo" y "Otro")
3. Copia la contraseña de 16 caracteres (sin espacios)
4. Actualiza `IMAP_PASSWORD` en `.env`
5. Reinicia el sistema: `python app.py`

---

## 📊 Escenarios Comunes

### Escenario 1: "Tengo correos pero todos están leídos"

**Solución:** Marca uno como no leído en Gmail, espera 60 segundos (intervalo de chequeo del sistema).

### Escenario 2: "Los correos van a Promociones"

**Solución:**
1. Arrastra manualmente a INBOX
2. Crea filtro (ver arriba) para que futuros correos vayan directo

### Escenario 3: "El diagnóstico no puede conectar"

**Solución:**
1. Verifica credenciales en `.env`
2. Asegúrate de usar contraseña de aplicación (no tu contraseña normal)
3. Habilita IMAP en Gmail
4. Verifica que la verificación en 2 pasos esté activa

### Escenario 4: "Veo errores NONAUTH en los logs"

**Solución:** Las mejoras implementadas deberían resolver esto. Si persiste:
1. Detén el sistema (Ctrl+C)
2. Borra logs antiguos: `rm logs/*.log`
3. Reinicia: `python app.py`
4. Monitorea: `tail -f logs/oc_seguimiento_*.log`

---

## 🔧 Comandos Útiles

```bash
# Diagnóstico completo (EMPIEZA AQUÍ)
python diagnose_imap.py

# Prueba de conexión simple
python test_imap_simple.py

# Enviar correo de prueba
python enviar_prueba.py

# Ver logs en tiempo real
tail -f logs/oc_seguimiento_*.log

# Ver solo correos encontrados
tail -f logs/oc_seguimiento_*.log | grep "Encontrados"

# Ver solo errores
tail -f logs/oc_seguimiento_*.log | grep ERROR

# Ver conexiones IMAP
tail -f logs/oc_seguimiento_*.log | grep -E "Conectando|✅|❌|reconect"
```

---

## 📝 Reporte de Diagnóstico

Cuando ejecutes `diagnose_imap.py`, guarda la salida completa. Si el problema persiste, ese reporte es clave para identificar la causa.

```bash
python diagnose_imap.py > diagnostico.txt 2>&1
```

Luego revisa el archivo `diagnostico.txt` para ver todos los detalles.

---

## ❓ FAQ

**P: ¿Por qué el sistema solo busca correos NO LEÍDOS?**
R: Para evitar procesar el mismo correo múltiples veces. Una vez procesado, se marca como leído.

**P: ¿Puedo cambiar esto?**
R: Sí, en `imap_wrapper.py` cambia `'UNSEEN'` por `'ALL'` en el método `search_unseen()`, pero deberás implementar otra forma de evitar duplicados.

**P: ¿Cada cuánto chequea el sistema?**
R: Por defecto cada 60 segundos (configurable en `.env` con `IMAP_CHECK_INTERVAL`).

**P: ¿Los correos con PDFs cuentan diferente?**
R: El sistema busca TODOS los correos no leídos, pero solo procesa los que tienen adjuntos PDF. Si no tienen PDF, se registran en los logs pero no se procesan.

---

## ✅ Checklist de Resolución

- [ ] Ejecuté `python diagnose_imap.py`
- [ ] Verifiqué que tengo correos NO LEÍDOS en INBOX
- [ ] Confirmé que IMAP está habilitado en Gmail
- [ ] Uso contraseña de aplicación (no mi contraseña normal)
- [ ] Los correos llegan a INBOX (no a Promociones/Social)
- [ ] Esperé al menos 60 segundos después de recibir un correo nuevo
- [ ] Revisé los logs con `tail -f logs/oc_seguimiento_*.log`
- [ ] No veo errores de autenticación en los logs

---

**Si completaste este checklist y el problema persiste, comparte:**
1. La salida completa de `python diagnose_imap.py`
2. Los últimos 50 líneas de logs: `tail -n 50 logs/oc_seguimiento_*.log`
3. Tu configuración IMAP (sin incluir la contraseña): `cat .env | grep IMAP | grep -v PASSWORD`

---

**Archivos modificados en esta actualización:**
- ✅ `imap_wrapper.py` - Mejor manejo de reconexión
- ✅ `diagnose_imap.py` - Nuevo script de diagnóstico
- ✅ `ERRORES_COMUNES.md` - Actualizado con comando de diagnóstico
- ✅ `SOLUCION_0_CORREOS.md` - Esta guía

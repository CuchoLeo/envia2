# ⚠️ Errores Comunes y Soluciones Rápidas

## Error: "command SEARCH illegal in state NONAUTH"

**Descripción:** El cliente IMAP está intentando buscar sin estar autenticado.

**Causa:** La conexión IMAP se perdió o expiró.

**Solución:**

El sistema ahora reconecta automáticamente. Si ves este error:

1. **Espera 60 segundos** - El sistema se reconectará automáticamente
2. **Verifica los logs** - Busca "✅ Conexión y autenticación exitosa"
3. **Si persiste**, verifica credenciales en `.env`:
   ```bash
   IMAP_USERNAME=tu-cuenta@gmail.com
   IMAP_PASSWORD=abcdefghijklmnop  # Contraseña de aplicación
   ```

**Logs esperados después de la corrección:**
```
⚠️ Cliente no conectado, reconectando...
Conectando a imap.gmail.com:993
✅ Conexión y autenticación exitosa
✅ Conexión IMAP establecida
```

---

## Error: "Authentication failed"

**Causa:** Credenciales incorrectas o no usas contraseña de aplicación.

**Solución:**

1. **Genera contraseña de aplicación** en Gmail:
   - https://myaccount.google.com/apppasswords
   - Requiere verificación en 2 pasos habilitada

2. **Edita .env** con la contraseña generada (sin espacios):
   ```bash
   IMAP_PASSWORD=abcdefghijklmnop
   ```

3. **Reinicia el sistema:**
   ```bash
   # Ctrl+C para detener
   python app.py
   ```

---

## Error: "Connection refused"

**Causa:** IMAP no está habilitado en Gmail o firewall bloqueando.

**Solución:**

1. **Habilita IMAP en Gmail:**
   - Gmail → Configuración → Ver toda la configuración
   - Pestaña "Reenvío y correo POP/IMAP"
   - Habilitar IMAP → Guardar cambios

2. **Verifica firewall:**
   - Puerto 993 debe estar abierto para IMAP SSL

3. **Prueba conexión:**
   ```bash
   python test_imap_simple.py
   ```

---

## Sistema encuentra 0 correos siempre

**Causa:** Los correos están marcados como leídos o en otra carpeta.

**Solución:**

1. **PRIMERO: Ejecuta el diagnóstico completo:**
   ```bash
   python diagnose_imap.py
   ```
   Esto te mostrará:
   - Si hay correos en la cuenta
   - Cuántos están leídos vs no leídos
   - En qué carpetas están
   - Los últimos mensajes recibidos

2. **Verifica que los correos estén en INBOX:**
   - Los correos deben llegar a INBOX
   - Gmail a veces los clasifica en Promociones/Social

3. **Marca un correo como no leído** para probarlo

4. **Envía un correo de prueba:**
   ```bash
   python enviar_prueba.py
   ```

5. **Verifica que tenga adjunto PDF:**
   - El sistema busca correos con PDFs adjuntos

---

## Reconexiones frecuentes

**Síntoma:**
```
⚠️ Conexión perdida, reconectando...
✅ Conexión y autenticación exitosa
```

**Causa:** Timeout de Gmail o conexión inestable.

**Solución:**

1. **Es normal** - Gmail cierra conexiones inactivas después de ~30 minutos
2. El sistema reconecta automáticamente
3. Si es muy frecuente (< 5 minutos), verifica tu conexión a internet

---

## No se detectan adjuntos PDF

**Causa:** El PDF no está correctamente adjunto o tiene otro formato.

**Solución:**

1. **Verifica que el archivo sea PDF:**
   - Extensión debe ser `.pdf`
   - No debe estar corrupto

2. **Revisa logs:**
   ```bash
   tail -f logs/oc_seguimiento_*.log | grep "📎"
   ```

3. **Prueba con el PDF de ejemplo:**
   ```bash
   python test_pdf.py "resumen del servicio.pdf"
   ```

---

## El sistema se detiene inesperadamente

**Causa:** Error no manejado o falta de memoria.

**Solución:**

1. **Revisa logs completos:**
   ```bash
   tail -n 100 logs/oc_seguimiento_*.log
   ```

2. **Reinicia el sistema:**
   ```bash
   python app.py
   ```

3. **Verifica recursos del sistema:**
   ```bash
   # macOS/Linux
   top
   # o
   htop
   ```

---

## Base de datos bloqueada

**Error:** "database is locked"

**Causa:** SQLite tiene limitaciones de concurrencia.

**Solución:**

1. **Cierra todas las instancias:**
   ```bash
   ps aux | grep app.py
   kill <PID>
   ```

2. **Elimina archivos de lock:**
   ```bash
   rm oc_seguimiento.db-journal
   ```

3. **Para producción, usa PostgreSQL:**
   ```bash
   # En .env
   DATABASE_URL=postgresql://user:pass@localhost/oc_seguimiento
   ```

---

## Logs muy grandes

**Causa:** Logging en modo DEBUG genera muchos logs.

**Solución:**

1. **Cambia nivel de log en .env:**
   ```bash
   LOG_LEVEL=INFO  # En vez de DEBUG
   ```

2. **Los logs rotan automáticamente:**
   - Se crean nuevos logs cada día
   - Se retienen por 30 días

3. **Limpia logs antiguos manualmente:**
   ```bash
   rm logs/oc_seguimiento_*.log.old
   ```

---

## 🔧 Comandos de Diagnóstico Rápido

```bash
# 🔍 DIAGNÓSTICO COMPLETO (RECOMENDADO)
python diagnose_imap.py

# Verificar instalación
python verify_install.py

# Probar conexión IMAP
python test_imap_simple.py

# Probar extracción PDF
python test_pdf.py "resumen del servicio.pdf"

# Enviar correo de prueba
python enviar_prueba.py

# Ver logs en tiempo real
tail -f logs/oc_seguimiento_*.log

# Ver solo errores
tail -f logs/oc_seguimiento_*.log | grep ERROR

# Ver solo conexiones IMAP
tail -f logs/oc_seguimiento_*.log | grep -E "Conectando|✅|❌"

# Verificar procesos corriendo
ps aux | grep app.py

# Verificar puerto en uso
lsof -i :8001  # macOS/Linux
netstat -ano | findstr :8001  # Windows
```

---

## 📚 Más Ayuda

- **Guía completa:** `TROUBLESHOOTING.md`
- **Guía de pruebas:** `GUIA_PRUEBA_LOCAL.md`
- **Inicio rápido:** `INICIO_RAPIDO.md`
- **Python 3.14:** `SOLUCION_PYTHON314.txt`

---

**¿Problema no listado aquí?** Revisa `TROUBLESHOOTING.md` para más detalles.

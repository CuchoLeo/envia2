# 🔧 Guía de Solución de Problemas

Soluciones a errores comunes del Sistema de Seguimiento de OC.

---

## ❌ Error: "property 'file' of 'IMAP4_TLS' object has no setter"

**Descripción:** Error de compatibilidad con IMAPClient y SSL.

**Solución Rápida:**

```bash
./fix_imap.sh
```

**O manualmente:**

```bash
# Activar entorno virtual
source venv/bin/activate

# Actualizar IMAPClient
pip uninstall -y imapclient
pip install imapclient==3.0.1

# Reinstalar todas las dependencias
pip install -r requirements.txt

# Probar conexión
python test_imap.py
```

**Causa:** Versión antigua de IMAPClient incompatible con Python 3.10+.

---

## ❌ Error: "Authentication failed" / "Invalid credentials"

**Descripción:** Las credenciales IMAP/SMTP no son correctas.

**Solución:**

### 1. Usa Contraseña de Aplicación (NO tu contraseña normal)

Para Gmail:

1. Ve a https://myaccount.google.com/security
2. Habilita "Verificación en 2 pasos" (requisito obligatorio)
3. Busca "Contraseñas de aplicaciones" al final de la sección
4. Selecciona "Correo" y "Otro (nombre personalizado)"
5. Escribe: "Sistema OC"
6. Copia la contraseña de 16 caracteres
7. Pégala en `.env` **sin espacios**

### 2. Verifica formato en .env

```bash
# ❌ MAL - con espacios
IMAP_PASSWORD=abcd efgh ijkl mnop

# ✅ BIEN - sin espacios
IMAP_PASSWORD=abcdefghijklmnop
```

### 3. Verifica que la cuenta sea correcta

```bash
# Probar conexión
python test_imap.py
```

---

## ❌ Error: "Connection refused" / "Cannot connect"

**Descripción:** No se puede conectar al servidor IMAP/SMTP.

**Solución:**

### 1. Habilita IMAP en Gmail

1. Ve a Gmail → Configuración (⚙️) → Ver toda la configuración
2. Pestaña "Reenvío y correo POP/IMAP"
3. Sección IMAP: **Habilitar IMAP**
4. Guarda cambios

### 2. Verifica puertos

En `.env`:

```bash
# IMAP con SSL
IMAP_PORT=993
IMAP_USE_SSL=True

# SMTP con TLS
SMTP_PORT=587
SMTP_USE_TLS=True
```

### 3. Verifica firewall

- Asegúrate que los puertos 993 (IMAP) y 587 (SMTP) no estén bloqueados
- Desactiva antivirus/firewall temporalmente para probar

### 4. Prueba conexión

```bash
python test_imap.py
```

---

## ❌ Error: "No module named 'pdfplumber'" (o similar)

**Descripción:** Dependencias no instaladas.

**Solución:**

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
python verify_install.py
```

---

## ❌ Error: "No se detectan correos nuevos"

**Descripción:** El sistema no encuentra correos en la casilla.

**Solución:**

### 1. Verifica que el correo llegó a INBOX

- Revisa que el correo esté en INBOX (no en spam/promociones)
- Gmail a veces clasifica correos automáticamente

### 2. Verifica credenciales IMAP

```bash
python test_imap.py
```

### 3. Revisa logs

```bash
tail -f logs/oc_seguimiento_*.log
```

Busca líneas como:
```
✅ Conexión IMAP establecida
📧 Encontrados X correos no leídos
```

### 4. Verifica intervalo de verificación

En `.env`:

```bash
# Verificar cada 60 segundos
IMAP_CHECK_INTERVAL=60
```

### 5. Marca el correo como no leído

Si el sistema ya lo procesó una vez, márcalo como no leído en Gmail.

---

## ❌ Error: "No se envían correos"

**Descripción:** Los correos no se envían desde el sistema.

**Solución:**

### 1. Verifica credenciales SMTP

En `.env`:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=tu-cuenta@gmail.com
SMTP_PASSWORD=tu_password_app
SMTP_USE_TLS=True
```

### 2. Usa contraseña de aplicación

Igual que IMAP, necesitas contraseña de aplicación para SMTP.

### 3. Prueba envío manual

```bash
python enviar_prueba.py
```

### 4. Revisa límites de Gmail

Gmail limita envíos:
- Cuentas gratuitas: ~500 correos/día
- Google Workspace: ~2000 correos/día

### 5. Verifica logs

```bash
tail -f logs/oc_seguimiento_*.log | grep "SMTP"
```

---

## ❌ Error: "No se extrae información del PDF"

**Descripción:** El procesador no puede leer el PDF.

**Solución:**

### 1. Verifica que pdfplumber esté instalado

```bash
pip install pdfplumber
```

### 2. Prueba extracción manual

```bash
python test_pdf.py "resumen del servicio.pdf"
```

### 3. Verifica formato del PDF

- El PDF debe ser texto (no imagen escaneada)
- El formato debe coincidir con el ejemplo
- Si es escaneado, necesitarás OCR (Tesseract)

### 4. Verifica el contenido

```bash
python -c "
import pdfplumber
with pdfplumber.open('resumen del servicio.pdf') as pdf:
    print(pdf.pages[0].extract_text())
"
```

---

## ❌ Error: "No se detecta la OC enviada"

**Descripción:** Sistema no asocia el correo con OC a la reserva.

**Solución:**

### 1. Incluye ID o LOC en el asunto

El asunto debe contener:
- ID de reserva: `ID 45215412`
- O LOC Interno: `LOC AAFTTAT`

Ejemplo:
```
Asunto: OC para Reserva ID 45215412 - LOC AAFTTAT
```

### 2. Envía a la casilla correcta

```bash
# En .env
OC_INBOX_USERNAME=cuenta-oc@gmail.com
```

Envía tu correo con OC a esa cuenta.

### 3. Adjunta un PDF

El sistema busca adjuntos PDF. Sin PDF adjunto, no detectará la OC.

### 4. Verifica logs

```bash
tail -f logs/oc_seguimiento_*.log | grep "OC"
```

### 5. Marca manualmente (alternativa)

En el dashboard:
- Ve a la reserva
- Click en "Marcar OC como recibida"

O vía API:
```bash
curl -X POST http://localhost:8001/api/reservas/1/marcar-oc-recibida \
  -H "Content-Type: application/json" \
  -d '{"numero_oc": "OC-12345"}'
```

---

## ❌ Error: "La agencia no requiere OC"

**Descripción:** Sistema no inicia seguimiento para una reserva.

**Solución:**

### 1. Verifica nombre exacto en .env

El nombre de la agencia debe coincidir EXACTAMENTE con el PDF:

```bash
# En .env - nombre debe ser idéntico
AGENCIES_REQUIRING_OC=WALVIS S.A.,EMPRESA CORPORATIVA LTDA

# ❌ MAL
AGENCIES_REQUIRING_OC=Walvis S.A.         # Minúsculas
AGENCIES_REQUIRING_OC=WALVIS S A          # Sin punto
AGENCIES_REQUIRING_OC=WALVIS              # Incompleto

# ✅ BIEN
AGENCIES_REQUIRING_OC=WALVIS S.A.         # Exacto como aparece en PDF
```

### 2. Extrae el nombre del PDF

```bash
python test_pdf.py "resumen del servicio.pdf" | grep "Agencia"
```

Copia el nombre exacto y pégalo en `.env`.

### 3. Reinicia el sistema

```bash
# Ctrl+C para detener
python app.py
```

---

## ❌ Error: "Database is locked"

**Descripción:** Base de datos SQLite bloqueada.

**Solución:**

### 1. Cierra otras conexiones

Asegúrate de que solo haya una instancia de `app.py` ejecutándose:

```bash
ps aux | grep app.py
# Mata procesos duplicados si existen
kill <PID>
```

### 2. Elimina archivo de lock

```bash
rm oc_seguimiento.db-journal
```

### 3. Considera PostgreSQL para producción

Si tienes mucho tráfico, migra a PostgreSQL:

```bash
# En .env
DATABASE_URL=postgresql://user:pass@localhost:5432/oc_seguimiento
```

---

## 🔍 Comandos de Diagnóstico Útiles

### Verificar instalación completa
```bash
python verify_install.py
```

### Verificar configuración
```bash
python config.py
```

### Probar conexión IMAP
```bash
python test_imap.py
```

### Probar extracción PDF
```bash
python test_pdf.py "resumen del servicio.pdf"
```

### Ver logs en tiempo real
```bash
tail -f logs/oc_seguimiento_*.log
```

### Ver solo errores
```bash
tail -f logs/oc_seguimiento_*.log | grep -E "❌|ERROR"
```

### Ver solo éxitos
```bash
tail -f logs/oc_seguimiento_*.log | grep -E "✅|INFO"
```

### Verificar base de datos
```bash
sqlite3 oc_seguimiento.db "SELECT id_reserva, agencia, estado_oc FROM reservas;"
```

### Reiniciar base de datos
```bash
rm oc_seguimiento.db
python database.py
```

---

## 📝 Checklist de Depuración

Cuando algo no funciona, sigue este orden:

- [ ] Verificar que el entorno virtual esté activo: `source venv/bin/activate`
- [ ] Verificar instalación: `python verify_install.py`
- [ ] Verificar configuración: `python config.py`
- [ ] Verificar .env: Revisar credenciales y formato
- [ ] Probar IMAP: `python test_imap.py`
- [ ] Probar PDF: `python test_pdf.py "archivo.pdf"`
- [ ] Revisar logs: `tail -f logs/oc_seguimiento_*.log`
- [ ] Verificar que IMAP esté habilitado en Gmail
- [ ] Verificar que uses contraseña de aplicación
- [ ] Reiniciar el sistema: Ctrl+C y `python app.py`

---

## 🆘 Si Nada Funciona

1. **Reinstala desde cero:**

```bash
# Detener sistema
# Ctrl+C

# Eliminar entorno virtual
rm -rf venv

# Eliminar base de datos
rm oc_seguimiento.db

# Reinstalar
./setup.sh

# Reconfigurar
nano .env

# Reiniciar
python app.py
```

2. **Verifica versiones:**

```bash
python --version        # Debe ser 3.10+
pip --version
```

3. **Revisa logs completos:**

```bash
cat logs/oc_seguimiento_*.log
```

4. **Ejecuta en modo debug:**

En `.env`:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

---

## 📚 Más Ayuda

- **Guía de Inicio:** `INICIO_RAPIDO.md`
- **Guía de Pruebas:** `GUIA_PRUEBA_LOCAL.md`
- **Documentación:** `README.md`
- **Referencias:** `LEEME_PRIMERO.txt`

---

¿Encontraste un error no listado aquí? Agrégalo a esta guía! 🚀

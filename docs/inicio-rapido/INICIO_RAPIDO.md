# 🚀 Inicio Rápido - Prueba Local con Gmail

Guía rápida para probar el sistema en 10 minutos con 2 cuentas Gmail.

## ⚡ Setup en 3 Pasos

### 1️⃣ Instalar

```bash
cd envia2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Configurar Gmail

**Para CADA cuenta Gmail que uses:**

1. Ve a https://myaccount.google.com/security
2. Habilita "Verificación en 2 pasos"
3. Ve a "Contraseñas de aplicaciones"
4. Genera una contraseña para "Correo"
5. Guarda la contraseña (16 caracteres)

### 3️⃣ Configurar `.env`

```bash
cp .env.example .env
nano .env
```

**Configuración mínima:**

```bash
# Cuenta Gmail #1 (recibe confirmaciones)
IMAP_USERNAME=tu-cuenta1@gmail.com
IMAP_PASSWORD=abcdefghijklmnop    # ← Contraseña de aplicación (sin espacios)

# Cuenta Gmail #2 (envía solicitudes)
SMTP_USERNAME=tu-cuenta2@gmail.com
SMTP_PASSWORD=wxyzabcdefghijkl    # ← Contraseña de aplicación

# Cuenta para recibir OC (puede ser la misma #1)
OC_INBOX_USERNAME=tu-cuenta1@gmail.com
OC_INBOX_PASSWORD=abcdefghijklmnop

# Clientes que requieren OC
AGENCIES_REQUIRING_OC=WALVIS S.A.

# Tiempos acelerados para pruebas
DAYS_FOR_REMINDER_1=0
DAYS_FOR_REMINDER_2=0
IMAP_CHECK_INTERVAL=60
```

---

## 🧪 Probar

### Verificar instalación
```bash
python verify_install.py
```

### Iniciar sistema
```bash
python app.py
```

Abre: **http://localhost:8001**

---

## 📧 Enviar Correos de Prueba

### Opción A: Script Automático (FÁCIL)

```bash
python enviar_prueba.py
```

Selecciona:
- **1** = Enviar confirmación de reserva
- **2** = Enviar orden de compra

### Opción B: Manual desde Gmail

**1. Enviar Confirmación:**
- **Para:** tu-cuenta1@gmail.com
- **Asunto:** Confirmación Reserva
- **Adjunto:** `resumen del servicio.pdf`

**2. Enviar OC:**
- **Para:** tu-cuenta1@gmail.com
- **Asunto:** OC para Reserva ID 45215412
- **Adjunto:** Cualquier PDF

---

## ✅ Qué Debería Pasar

1. ✅ Sistema detecta correo con PDF (en 60 segundos)
2. ✅ Extrae datos del PDF
3. ✅ Crea reserva en base de datos
4. ✅ Envía solicitud de OC automáticamente
5. ✅ Detecta OC cuando la envías
6. ✅ Marca como "Recibida" y detiene recordatorios

**Ver en:**
- 🌐 Dashboard: http://localhost:8001
- 📊 API: http://localhost:8001/api/stats
- 📝 Logs: `tail -f logs/oc_seguimiento_*.log`

---

## 🐛 Problemas Comunes

### "Error de autenticación Gmail"
→ Usa contraseña de aplicación, no tu contraseña normal

### "No se detectan correos"
→ Verifica que IMAP esté habilitado en Gmail
→ Revisa el log: `tail -f logs/oc_seguimiento_*.log`

### "No se envían correos"
→ Verifica puerto SMTP: 587
→ Verifica `SMTP_USE_TLS=True`

---

## 📚 Más Información

- **Guía Completa:** Ver `GUIA_PRUEBA_LOCAL.md`
- **Documentación:** Ver `README.md`
- **API REST:** http://localhost:8001/docs

---

## 🎯 Flujo de Prueba Completo

```bash
# 1. Instalar y configurar
./setup.sh
nano .env

# 2. Iniciar sistema
python app.py

# 3. En otra terminal: Enviar correo de prueba
python enviar_prueba.py

# 4. Ver dashboard
open http://localhost:8001

# 5. Ver logs
tail -f logs/oc_seguimiento_*.log
```

---

¡Listo! En menos de 10 minutos tendrás el sistema funcionando. 🚀

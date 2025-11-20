# 📧 Configuración de Gmail para el Sistema

**Sistema de Seguimiento de Órdenes de Compra**

---

## 🎯 Resumen Rápido

El sistema usa **IMAP** para leer correos y **SMTP** para enviarlos. Gmail soporta ambos protocolos de forma nativa.

### Servidores a usar:
- **IMAP:** imap.gmail.com:993 (SSL)
- **SMTP:** smtp.gmail.com:587 (STARTTLS)

---

## ✅ Paso 1: Habilitar Verificación en 2 Pasos

Gmail **REQUIERE** verificación en 2 pasos para generar contraseñas de aplicación.

### Pasos:

1. Ir a: https://myaccount.google.com/security
2. En "Cómo accedes a Google", hacer click en "Verificación en 2 pasos"
3. Click en "Empezar"
4. Seguir las instrucciones para configurar:
   - **Opción A:** Usar teléfono (SMS o llamada)
   - **Opción B:** Usar app Google Authenticator (recomendado)
   - **Opción C:** Usar llave de seguridad física

5. Completar el proceso de verificación

> ⏰ **Tiempo estimado:** 5-10 minutos

---

## 🔐 Paso 2: Generar Contraseña de Aplicación

Una vez habilitada la verificación en 2 pasos:

### Pasos:

1. Ir a: https://myaccount.google.com/apppasswords
2. Iniciar sesión con tu cuenta de Gmail
3. Si te pide verificación en 2 pasos, compléta
4. En "Seleccionar app", elegir **"Correo"**
5. En "Seleccionar dispositivo", elegir **"Otro (nombre personalizado)"**
6. Escribir: `Sistema OC Kontrol Travel`
7. Click en **"Generar"**
8. Google mostrará una contraseña de 16 caracteres en formato:
   ```
   xxxx xxxx xxxx xxxx
   ```
9. **¡IMPORTANTE!** Copiar la contraseña **SIN ESPACIOS**:
   ```
   xxxxxxxxxxxxxxxx
   ```
10. Guardar en un lugar seguro (administrador de contraseñas)
11. Click en "Listo"

> ⚠️ **CRÍTICO:** Esta contraseña solo se muestra UNA VEZ. Si la pierdes, debes generar una nueva.

### Formato de la Contraseña:

**Correcto:**
```
abcdefghijklmnop
```

**Incorrecto:**
```
abcd efgh ijkl mnop  ❌ (con espacios)
```

---

## 🧪 Paso 3: Probar la Conexión

### Test IMAP (Recepción):

```bash
python3 -c "
import imaplib
import ssl

# Configuración
host = 'imap.gmail.com'
port = 993
username = 'tu_email@gmail.com'
password = 'tu_contraseña_de_aplicacion'

# Conectar
context = ssl.create_default_context()
imap = imaplib.IMAP4_SSL(host, port, ssl_context=context)
imap.login(username, password)

# Listar buzones
status, mailboxes = imap.list()
print('✅ Conexión IMAP exitosa!')
print(f'Buzones: {len(mailboxes)}')

imap.logout()
"
```

### Test SMTP (Envío):

```bash
python3 -c "
import smtplib

# Configuración
host = 'smtp.gmail.com'
port = 587
username = 'tu_email@gmail.com'
password = 'tu_contraseña_de_aplicacion'

# Conectar
server = smtplib.SMTP(host, port)
server.starttls()
server.login(username, password)

print('✅ Conexión SMTP exitosa!')
server.quit()
"
```

---

## 🐛 Troubleshooting

### Error: "Application-specific password required"

**Solución:**
1. Verificar que tienes verificación en 2 pasos habilitada
2. Generar una nueva contraseña de aplicación
3. Usar esa contraseña (no la contraseña normal de Gmail)

### Error: "Username and Password not accepted"

**Causas posibles:**

1. **Contraseña incorrecta**
   - Verificar que no haya espacios
   - Copiar sin el formato `xxxx xxxx xxxx xxxx`
   - Debe ser 16 caracteres sin espacios

2. **Usando contraseña normal en lugar de contraseña de aplicación**
   - Gmail NO acepta la contraseña normal para IMAP/SMTP
   - DEBES usar contraseña de aplicación

3. **Verificación en 2 pasos no habilitada**
   - No puedes generar contraseñas de aplicación sin 2FA
   - Habilitar primero verificación en 2 pasos

4. **Contraseña de aplicación revocada**
   - La contraseña pudo haber sido eliminada
   - Generar una nueva

### Error: "IMAP access disabled"

**Solución:**
1. Ir a: https://mail.google.com/mail/u/0/#settings/fwdandpop
2. En "Acceso IMAP", seleccionar "Habilitar IMAP"
3. Click en "Guardar cambios"
4. Esperar 5-10 minutos
5. Intentar nuevamente

### Error: "Connection timed out"

**Causas posibles:**

1. **Firewall bloqueando puertos**
   - Verificar que puertos 993 (IMAP) y 587 (SMTP) estén abiertos
   - Consultar con IT/Redes

2. **Servidor incorrecto**
   - Verificar: `imap.gmail.com` (NO `gmail.com`)
   - Verificar: `smtp.gmail.com` (NO `smtp.google.com`)

3. **Red empresarial con restricciones**
   - Algunas redes corporativas bloquean IMAP/SMTP
   - Probar desde otra red (casa, datos móviles)

### Error: "Too many login attempts"

**Solución:**
- Gmail tiene límite de intentos de login fallidos
- Esperar 15-30 minutos
- Intentar nuevamente con credenciales correctas

### Error: "Less secure app access"

**Contexto:**
- Google eliminó la opción "Permitir apps menos seguras" en mayo 2022
- Ya NO es posible usar contraseñas normales
- DEBES usar contraseñas de aplicación

**Solución:**
1. Habilitar verificación en 2 pasos
2. Generar contraseña de aplicación
3. Usar esa contraseña

---

## 🔒 Seguridad

### Recomendaciones:

1. ✅ **Usar contraseñas de aplicación únicas**
   - Una contraseña diferente por servicio/dispositivo
   - Facilita revocación si hay problemas

2. ✅ **No compartir** contraseñas de aplicación
   - Son equivalentes a tu contraseña real
   - Darían acceso completo a tu correo

3. ✅ **Revocar** contraseñas de aplicación que ya no uses
   - Ir a: https://myaccount.google.com/apppasswords
   - Click en icono de basura junto a la contraseña

4. ✅ **Usar cuentas de servicio** dedicadas
   - Crear cuenta Gmail específica para el sistema
   - Ejemplo: `oc.kontroltravel@gmail.com`
   - No usar cuenta personal

5. ✅ **Monitorear actividad**
   - Gmail muestra dispositivos conectados
   - Revisar periódicamente: https://myaccount.google.com/device-activity

### Buenas Prácticas:

```
✅ HACER:
- Crear cuenta Gmail específica para el sistema
- Usar contraseña de aplicación única para este sistema
- Guardar contraseña en administrador de contraseñas (1Password, Bitwarden)
- Revisar logs de acceso periódicamente

❌ NO HACER:
- Usar cuenta personal Gmail del administrador
- Compartir contraseñas de aplicación entre sistemas
- Deshabilitar verificación en 2 pasos
- Guardar contraseña en texto plano
```

---

## 📋 Checklist de Configuración

Antes de usar el sistema con Gmail:

- [ ] Cuenta de Gmail creada
- [ ] Verificación en 2 pasos habilitada
- [ ] Contraseña de aplicación generada
- [ ] Contraseña guardada en lugar seguro (sin espacios)
- [ ] IMAP habilitado en Gmail
- [ ] Test de conexión IMAP pasó ✅
- [ ] Test de conexión SMTP pasó ✅
- [ ] Cuenta no tiene problemas de seguridad

---

## 🔧 Configuración en el Sistema

### Archivo .env

```bash
# IMAP - Recepción de confirmaciones
IMAP_HOST="imap.gmail.com"
IMAP_PORT=993
IMAP_USERNAME="tu_email@gmail.com"
IMAP_PASSWORD="tu_contraseña_de_aplicacion_aqui"
IMAP_USE_SSL=true

# SMTP - Envío de solicitudes
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USERNAME="tu_email@gmail.com"
SMTP_PASSWORD="tu_contraseña_de_aplicacion_aqui"
SMTP_USE_TLS=true

# IMAP - Recepción de OC
OC_INBOX_HOST="imap.gmail.com"
OC_INBOX_PORT=993
OC_INBOX_USERNAME="tu_email@gmail.com"
OC_INBOX_PASSWORD="tu_contraseña_de_aplicacion_aqui"
OC_INBOX_USE_SSL=true
```

---

## 🆘 Soporte de Google

Si los problemas persisten:

1. **Ayuda de Gmail:**
   - https://support.google.com/mail/
   - Buscar "IMAP settings" o "App passwords"

2. **Estado del Servicio:**
   - https://www.google.com/appsstatus
   - Verificar si hay interrupciones de Gmail

3. **Comunidad de Google:**
   - https://support.google.com/mail/community
   - Hacer preguntas a la comunidad

---

## 💡 Tips Adicionales

### Configurar Etiquetas/Carpetas en Gmail:

1. Crear etiqueta "OC-Sistema" para organizar
2. Configurar filtro automático:
   - De: (emails de agencias)
   - Aplicar etiqueta: "OC-Sistema"
   - Marcar como importante

### Limitaciones de Gmail:

- **Límite de envío:** 500 emails/día (cuenta normal)
- **Límite de envío (Google Workspace):** 2,000 emails/día
- **Límite de IMAP:** ~15 conexiones simultáneas
- **Límite de SMTP:** ~100 mensajes/hora (ráfagas)

> Para este sistema, estos límites son MÁS QUE SUFICIENTES.

### Migrar de Gmail Personal a Google Workspace:

Si el volumen de emails crece, considerar Google Workspace:
- Mayor límite de envío (2,000/día)
- Soporte empresarial
- Email personalizado (@tuempresa.com)
- Costo: ~$6 USD/usuario/mes

---

## 📱 Verificación en 2 Pasos con App Authenticator

### Opción Recomendada (más segura):

1. Descargar Google Authenticator:
   - iOS: https://apps.apple.com/app/google-authenticator/id388497605
   - Android: https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2

2. En https://myaccount.google.com/security → Verificación en 2 pasos
3. Click en "Añadir más segundos pasos"
4. Seleccionar "App Authenticator"
5. Escanear código QR con la app
6. Ingresar código de 6 dígitos

**Ventajas:**
- ✅ No depende de SMS/llamadas
- ✅ Funciona sin internet
- ✅ Más seguro que SMS
- ✅ Más rápido

---

## ✅ Verificación Final

Ejecutar el script de verificación completo:

```bash
python3 scripts/test_conexion.py
```

Debe mostrar:
```
✅ PASS  IMAP Confirmaciones
✅ PASS  IMAP OC
✅ PASS  SMTP
✅ PASS  Base de Datos
✅ PASS  Templates
✅ PASS  Configuración

Total: 6/6 tests pasados
✅ TODOS LOS TESTS PASARON - SISTEMA LISTO
```

---

**Si todos los tests pasan, estás listo para empezar! 🚀**

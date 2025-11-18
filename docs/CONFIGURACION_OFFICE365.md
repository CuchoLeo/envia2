# 📧 Configuración de Office 365 para el Sistema

**Sistema de Seguimiento de Órdenes de Compra**

---

## 🎯 Resumen Rápido

El sistema usa **IMAP** para leer correos y **SMTP** para enviarlos. Office 365 (Microsoft 365) soporta ambos protocolos.

### Servidores a usar:
- **IMAP:** outlook.office365.com:993 (SSL)
- **SMTP:** smtp.office365.com:587 (STARTTLS)

---

## ✅ Paso 1: Verificar que IMAP está Habilitado

### Opción A: Para Usuarios Finales

1. Ir a https://outlook.office.com
2. Iniciar sesión con la cuenta
3. Click en ⚙️ → "Ver toda la configuración"
4. Buscar "Correo" → "Sincronizar correo electrónico"
5. Verificar que "IMAP" aparece como habilitado

Si NO está habilitado, contactar al administrador.

### Opción B: Para Administradores de Office 365 (Recomendado)

1. Ir a https://admin.microsoft.com
2. Iniciar sesión como administrador
3. Ir a "Usuarios" → "Usuarios activos"
4. Buscar y seleccionar el usuario
5. Click en la pestaña "Correo"
6. Click en "Administrar configuración de correo electrónico"
7. Asegurarse que:
   - ✅ IMAP está habilitado
   - ✅ Autenticación está permitida

**Nota:** Los cambios pueden tardar hasta 24 horas en aplicarse.

---

## 🔐 Paso 2: Obtener Contraseña

### Si la cuenta tiene Autenticación Multifactor (MFA/2FA):

**Usar Contraseñas de Aplicación:**

1. Ir a: https://account.activedirectory.windowsazure.com/AppPasswords.aspx
2. Iniciar sesión con la cuenta
3. Click en "Crear"
4. Nombre: "Sistema OC Kontrol Travel"
5. Copiar la contraseña generada (aparece sin espacios)
6. Guardar en un lugar seguro

**Formato:**
```
Ejemplo: abcdefghijklmnop
(16 caracteres sin espacios)
```

### Si la cuenta NO tiene MFA:

**Usar la contraseña normal** de la cuenta de Office 365.

> ⚠️ **IMPORTANTE:** Si tienen políticas de seguridad empresariales, es posible que REQUIERAN usar contraseñas de aplicación incluso sin MFA. Consultar con el administrador.

---

## 🧪 Paso 3: Probar la Conexión

### Test IMAP (Recepción):

```bash
python3 -c "
import imaplib
import ssl

# Configuración
host = 'outlook.office365.com'
port = 993
username = 'tu_email@tuempresa.com'
password = 'tu_contraseña'

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
host = 'smtp.office365.com'
port = 587
username = 'tu_email@tuempresa.com'
password = 'tu_contraseña'

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

### Error: "IMAP is disabled for this account"

**Solución:**
1. El administrador debe habilitar IMAP en el Centro de Administración
2. Esperar 24 horas para que el cambio se aplique
3. Intentar nuevamente

### Error: "Authentication failed"

**Causas posibles:**

1. **Contraseña incorrecta**
   - Verificar que no haya espacios
   - Si es contraseña de aplicación, copiar sin espacios

2. **MFA activo pero usando contraseña normal**
   - Generar contraseña de aplicación
   - Usar esa contraseña en lugar de la normal

3. **Autenticación básica deshabilitada**
   - El admin debe habilitar "Autenticación básica" para IMAP/SMTP
   - O configurar OAuth2 (más complejo)

4. **Cuenta bloqueada/suspendida**
   - Verificar que la cuenta esté activa en Office 365

### Error: "Connection timed out"

**Causas posibles:**

1. **Firewall bloqueando puertos**
   - Verificar que puertos 993 (IMAP) y 587 (SMTP) estén abiertos
   - Consultar con IT/Redes

2. **Servidor incorrecto**
   - Verificar: outlook.office365.com (NO outlook.com)
   - Verificar: smtp.office365.com

### Error: "SSL certificate verification failed"

**Solución:**
```python
# En config.py, temporalmente para testing:
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

> ⚠️ **NO usar en producción**, solo para diagnosticar.

---

## 🔒 Seguridad

### Recomendaciones:

1. ✅ **Usar contraseñas de aplicación** si tienen MFA
2. ✅ **No compartir** contraseñas de aplicación
3. ✅ **Revocar** contraseñas de aplicación si ya no se usan
4. ✅ **Usar cuentas de servicio** dedicadas si es posible
5. ✅ **Habilitar logs** de auditoría en Office 365

### Buenas Prácticas:

```
✅ HACER:
- Crear cuenta específica para el sistema (ej: oc-sistema@empresa.com)
- Usar contraseñas de aplicación únicas
- Revisar logs de acceso periódicamente

❌ NO HACER:
- Usar cuenta personal del administrador
- Compartir contraseñas entre sistemas
- Deshabilitar MFA solo por este sistema
```

---

## 📋 Checklist de Configuración

Antes de usar el sistema con Office 365:

- [ ] IMAP está habilitado en la cuenta
- [ ] SMTP está habilitado en la cuenta
- [ ] Contraseña obtenida (normal o de aplicación)
- [ ] Test de conexión IMAP pasó ✅
- [ ] Test de conexión SMTP pasó ✅
- [ ] Buzón INBOX existe y es accesible
- [ ] Cuenta no está bloqueada/suspendida
- [ ] Firewall permite puertos 993 y 587

---

## 🔧 Configuración en el Sistema

### Archivo .env

```bash
# IMAP - Recepción de confirmaciones
IMAP_HOST="outlook.office365.com"
IMAP_PORT=993
IMAP_USERNAME="administracion@kontroltravel.com"
IMAP_PASSWORD="tu_contraseña_aqui"
IMAP_USE_SSL=true

# SMTP - Envío de solicitudes
SMTP_HOST="smtp.office365.com"
SMTP_PORT=587
SMTP_USERNAME="administracion@kontroltravel.com"
SMTP_PASSWORD="tu_contraseña_aqui"
SMTP_USE_TLS=true

# IMAP - Recepción de OC
OC_INBOX_HOST="outlook.office365.com"
OC_INBOX_PORT=993
OC_INBOX_USERNAME="administracion@kontroltravel.com"
OC_INBOX_PASSWORD="tu_contraseña_aqui"
OC_INBOX_USE_SSL=true
```

---

## 🆘 Soporte de Microsoft

Si los problemas persisten:

1. **Soporte de Microsoft 365:**
   - https://admin.microsoft.com/AdminPortal/Home#/support
   - Crear ticket de soporte técnico

2. **Documentación Oficial:**
   - IMAP: https://support.microsoft.com/en-us/office/imap-settings-93697465-0408-4df8-9977-4e8c14f9f001
   - SMTP: https://support.microsoft.com/en-us/office/smtp-settings-8361e398-8af4-4e97-b147-6c6c4ac95353

3. **Estado del Servicio:**
   - https://status.office365.com
   - Verificar si hay interrupciones

---

## 💡 Tips Adicionales

### Para Administradores:

1. **Crear cuenta de servicio dedicada:**
   ```
   Nombre: Sistema OC
   Email: oc-sistema@tuempresa.com
   Licencia: Exchange Online Plan 1 (suficiente)
   ```

2. **Configurar reenvío automático** (opcional):
   - Si quieren que las confirmaciones lleguen a otra cuenta
   - Configurar regla de reenvío en Outlook

3. **Monitorear uso:**
   - Centro de Administración → Informes
   - Ver actividad de la cuenta
   - Detectar problemas temprano

### Limitaciones de Office 365:

- **Límite de envío:** ~10,000 emails/día por cuenta
- **Límite de IMAP:** ~20 conexiones simultáneas
- **Límite de SMTP:** ~30 mensajes/minuto

> Para este sistema, estos límites son MÁS QUE SUFICIENTES.

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

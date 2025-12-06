# Migración a Office 365 - Cuenta del Dominio controloc.hotelsales.cl

**Objetivo**: Reemplazar `seguimientoocx@gmail.com` por cuenta corporativa de Office 365
**Cuenta propuesta**: `controloc@hotelsales.cl`
**Fecha**: Diciembre 2025

---

## 📋 Resumen de Cambios

### Cuentas Actuales (Gmail)
```
MONITOREO:  seguimientoocx@gmail.com  → Recibe confirmaciones
ENVÍO:      seguimientoocx@gmail.com  → Envía solicitudes de OC
OC INBOX:   seguimientoocx@gmail.com  → Recibe OC de clientes
```

### Cuentas Nuevas (Office 365)
```
MONITOREO:  controloc@hotelsales.cl   → Recibe confirmaciones
ENVÍO:      controloc@hotelsales.cl   → Envía solicitudes de OC
OC INBOX:   controloc@hotelsales.cl   → Recibe OC de clientes
```

**Beneficios**:
- ✅ Imagen corporativa profesional
- ✅ Mayor confiabilidad empresarial
- ✅ Integración con ecosistema Microsoft
- ✅ Mejor soporte técnico
- ✅ Mayor seguridad y compliance

---

## 🔧 Configuración de Office 365

### 1. Requisitos Previos

#### 1.1. Licencia de Office 365
**Planes compatibles**:
- ✅ **Office 365 Business Basic** (USD $6/usuario/mes) - RECOMENDADO
- ✅ Office 365 Business Standard (USD $12.50/usuario/mes)
- ✅ Microsoft 365 Business Premium (USD $22/usuario/mes)
- ❌ Office 365 E1/E3/E5 (empresarial, más caro)

**Licencia mínima requerida**: Business Basic
- Incluye Exchange Online (50 GB mailbox)
- IMAP/POP3/SMTP habilitado
- Seguridad anti-spam/malware
- Autenticación multi-factor (MFA) opcional

#### 1.2. Dominio Verificado
**Dominio**: `hotelsales.cl`
**Subdominios posibles**:
- `controloc@hotelsales.cl` (RECOMENDADO - corto y claro)
- `oc@hotelsales.cl` (muy corto, puede confundirse)
- `seguimiento@hotelsales.cl` (descriptivo)
- `reservas@hotelsales.cl` (genérico)

**Estado del dominio**: Debe estar verificado en Office 365 Admin Center

---

### 2. Configuración del Buzón de Correo

#### 2.1. Crear Usuario en Office 365

**Pasos en Admin Center**:
1. Ir a **Admin Center** → **Users** → **Active users**
2. Click **Add a user**
3. Configurar:
   ```
   First name: Control
   Last name: OC Sistema
   Display name: Control OC Sistema
   Username: controloc
   Domain: hotelsales.cl

   Email: controloc@hotelsales.cl
   ```
4. Asignar licencia: **Office 365 Business Basic**
5. **NO** marcar "Send password in email" (guardar contraseña segura)
6. Configurar contraseña fuerte (mínimo 12 caracteres)

**Contraseña recomendada**: Generar con gestor de contraseñas (ej: LastPass, 1Password)
```
Ejemplo: K0ntr0l!OC#2025$Sys
```

#### 2.2. Configuración del Buzón

**En Exchange Admin Center**:
1. Ir a **Recipients** → **Mailboxes**
2. Seleccionar `controloc@hotelsales.cl`
3. Configurar:
   - **Mailbox size**: 50 GB (incluido en licencia)
   - **Retention policy**: 30 días (o personalizado)
   - **Litigation hold**: OFF (a menos que requiera compliance)
   - **Archiving**: OFF (no necesario para este caso)

---

### 3. Habilitar IMAP/SMTP en Office 365

**IMPORTANTE**: Por defecto, Office 365 tiene IMAP/SMTP deshabilitado para nuevos usuarios.

#### 3.1. Habilitar Protocolos

**Método 1: PowerShell (RECOMENDADO - más rápido)**

```powershell
# Conectar a Exchange Online
Install-Module -Name ExchangeOnlineManagement
Connect-ExchangeOnline -UserPrincipalName admin@hotelsales.cl

# Habilitar IMAP para el usuario
Set-CASMailbox -Identity controloc@hotelsales.cl -ImapEnabled $true

# Habilitar POP3 (opcional, no usado pero no afecta)
Set-CASMailbox -Identity controloc@hotelsales.cl -PopEnabled $true

# Verificar configuración
Get-CASMailbox -Identity controloc@hotelsales.cl | Select-Object ImapEnabled,PopEnabled

# Desconectar
Disconnect-ExchangeOnline
```

**Método 2: Admin Center (GUI)**

1. Ir a **Exchange Admin Center** → **Recipients** → **Mailboxes**
2. Seleccionar `controloc@hotelsales.cl`
3. Click en **Manage email apps settings**
4. Marcar:
   - ✅ **IMAP**
   - ✅ **POP** (opcional)
   - ✅ **SMTP AUTH** (crítico para envío)
5. Click **Save**

#### 3.2. Habilitar SMTP AUTH (Autenticación SMTP)

**IMPORTANTE**: Office 365 requiere habilitar explícitamente SMTP AUTH

**PowerShell**:
```powershell
Set-CASMailbox -Identity controloc@hotelsales.cl -SmtpClientAuthenticationDisabled $false
```

**O en Exchange Admin Center**:
1. **Settings** → **Mail flow** → **Remote domains**
2. Verificar que SMTP AUTH esté habilitado globalmente

---

### 4. Configuración IMAP/SMTP - Parámetros

#### 4.1. Configuración IMAP (Recepción de Correos)

**Servidor IMAP de Office 365**:
```
Host:       outlook.office365.com
Port:       993
Security:   SSL/TLS
Username:   controloc@hotelsales.cl  (correo completo)
Password:   [contraseña del usuario]
```

**Carpetas especiales**:
- INBOX: Bandeja de entrada
- Sent: Elementos enviados
- Drafts: Borradores
- Trash: Elementos eliminados

#### 4.2. Configuración SMTP (Envío de Correos)

**Servidor SMTP de Office 365**:
```
Host:       smtp.office365.com
Port:       587 (RECOMENDADO - TLS)
            465 (alternativo - SSL)
Security:   STARTTLS (port 587) o SSL (port 465)
Username:   controloc@hotelsales.cl  (correo completo)
Password:   [contraseña del usuario]
```

**Limitaciones de envío**:
- Máximo 10,000 destinatarios/día
- Máximo 500 destinatarios por mensaje
- Máximo 30 mensajes/minuto

**Para este sistema**: No hay problema, envía ~10-20 correos/día

---

### 5. Autenticación: Contraseña de Aplicación vs. MFA

#### 5.1. Opción 1: Usuario/Contraseña Normal (MÁS SIMPLE)

**Ventajas**:
- ✅ Configuración directa
- ✅ No requiere pasos adicionales
- ✅ Compatible con código actual

**Desventajas**:
- ⚠️ Menos seguro (contraseña en texto plano en `.env`)
- ⚠️ Si se habilita MFA después, deja de funcionar

**Configuración en .env**:
```bash
IMAP_USERNAME=controloc@hotelsales.cl
IMAP_PASSWORD=K0ntr0l!OC#2025$Sys
```

#### 5.2. Opción 2: Contraseña de Aplicación (SI SE USA MFA)

Si Office 365 tiene **Multi-Factor Authentication (MFA)** habilitado:

**Pasos**:
1. Ir a https://account.microsoft.com/security
2. Login con `controloc@hotelsales.cl`
3. Click en **Security** → **Advanced security options**
4. Buscar **App passwords**
5. Click **Create a new app password**
6. Nombre: "Sistema Seguimiento OC"
7. **Copiar contraseña generada** (solo se muestra una vez)

Ejemplo: `abcd efgh ijkl mnop`

**Configuración en .env**:
```bash
IMAP_USERNAME=controloc@hotelsales.cl
IMAP_PASSWORD=abcdefghijklmnop  # Sin espacios
```

#### 5.3. Opción 3: OAuth 2.0 (MÁS SEGURO - FUTURO)

**NO implementado actualmente en el sistema**

Requiere:
- Registro de app en Azure AD
- Implementación de flujo OAuth en código
- Tokens con expiración y refresh

**Beneficios**:
- ✅ Mayor seguridad (no contraseñas en `.env`)
- ✅ Permisos granulares
- ✅ Revocación remota

**Para Fase 3 del proyecto** (según roadmap)

---

### 6. Configuración DNS del Dominio

#### 6.1. Registros MX (Mail Exchange)

**IMPORTANTE**: Estos registros ya deben estar configurados si el dominio usa Office 365

Verificar en registrador de dominio (`hotelsales.cl`):

```
Tipo    Nombre              Prioridad   Valor
MX      hotelsales.cl       0           hotelsales-cl.mail.protection.outlook.com
```

Si no está configurado, **NO MODIFICAR** sin consultar con administrador del dominio.

#### 6.2. Registros SPF (Sender Policy Framework)

**Verificar registro TXT en DNS**:
```
Tipo    Nombre              Valor
TXT     hotelsales.cl       v=spf1 include:spf.protection.outlook.com -all
```

**Propósito**: Autoriza a Office 365 a enviar correos en nombre de `@hotelsales.cl`

**Si falta**: Correos pueden marcarse como spam

#### 6.3. Registros DKIM (DomainKeys Identified Mail)

**En Exchange Admin Center**:
1. **Protection** → **DKIM**
2. Seleccionar `hotelsales.cl`
3. Click **Enable**
4. Copiar registros CNAME generados
5. Agregarlos al DNS del dominio

**Ejemplo**:
```
Tipo    Nombre                              Valor
CNAME   selector1._domainkey.hotelsales.cl  selector1-hotelsales-cl._domainkey.contoso.onmicrosoft.com
CNAME   selector2._domainkey.hotelsales.cl  selector2-hotelsales-cl._domainkey.contoso.onmicrosoft.com
```

**Propósito**: Firma digital de correos enviados

#### 6.4. Registros DMARC (Domain-based Message Authentication)

**Registro TXT recomendado**:
```
Tipo    Nombre              Valor
TXT     _dmarc.hotelsales.cl    v=DMARC1; p=quarantine; rua=mailto:dmarc@hotelsales.cl
```

**Propósito**: Política de manejo de correos no autenticados

---

## 🔒 Seguridad y Permisos

### 1. Permisos de la Cuenta de Servicio

**La cuenta `controloc@hotelsales.cl` es una cuenta de servicio**, no un usuario humano.

#### Configuración Recomendada:

**En Office 365 Admin Center**:
1. **Users** → **Active users** → `controloc@hotelsales.cl`
2. **Sign-in status**:
   - ✅ Permitir inicio de sesión
   - ⚠️ **NO** marcar "User must change password at next sign-in"
3. **Password**:
   - ❌ NO caducar contraseña (o configurar expiración muy larga)
   - Click en **Edit** → Desmarcar "Require this user to change their password..."

**Permisos mínimos**:
- ✅ Leer correos (IMAP)
- ✅ Enviar correos (SMTP)
- ✅ Crear/modificar carpetas
- ❌ NO necesita acceso a SharePoint
- ❌ NO necesita acceso a Teams
- ❌ NO necesita acceso a OneDrive

### 2. Configuración de Seguridad

#### 2.1. Anti-Spam y Anti-Malware

**Exchange Admin Center** → **Protection** → **Anti-spam**

**Para evitar que correos legítimos vayan a spam**:
1. Agregar remitentes autorizados a **Safe Senders**:
   ```
   kontroltravel@ideasfractal.com
   v.rodriguezy@gmail.com
   cuchohbk@gmail.com
   ```

2. Agregar dominios confiables:
   ```
   @ideasfractal.com
   ```

#### 2.2. Políticas de Retención

**Configuración recomendada**:
- **INBOX**: Retener 90 días
- **Sent Items**: Retener indefinidamente (importante para auditoría)
- **Deleted Items**: Vaciar automáticamente después de 30 días

#### 2.3. Acceso Condicional (Opcional - Licencias Premium)

Si la organización tiene Azure AD Premium:
- Restringir acceso por IP (solo desde servidor del sistema)
- Requerir MFA solo para acceso humano (no para aplicaciones)

---

## 💻 Cambios en el Código

### 1. Archivo `.env`

**Cambios necesarios**:

```bash
# ==================== CORREO DE MONITOREO (IMAP) ====================
# Casilla donde llegan las confirmaciones
IMAP_HOST=outlook.office365.com        # Cambio: era imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=controloc@hotelsales.cl  # Cambio: era seguimientoocx@gmail.com
IMAP_PASSWORD=[CONTRASEÑA_SEGURA]      # Cambio: nueva contraseña
IMAP_MAILBOX=INBOX
IMAP_USE_SSL=True

# ==================== CORREO DE ENVÍO (SMTP) ====================
# Casilla desde la cual se envían las solicitudes de OC
SMTP_HOST=smtp.office365.com           # Cambio: era smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=controloc@hotelsales.cl  # Cambio: era seguimientoocx@gmail.com
SMTP_PASSWORD=[CONTRASEÑA_SEGURA]      # Cambio: nueva contraseña
SMTP_FROM_EMAIL=controloc@hotelsales.cl  # Cambio
SMTP_FROM_NAME=Kontrol Travel - Administración
SMTP_USE_TLS=True

# ==================== CORREO DE RECEPCIÓN DE OC ====================
# Casilla donde las agencias envían las órdenes de compra
OC_INBOX_HOST=outlook.office365.com    # Cambio: era imap.gmail.com
OC_INBOX_PORT=993
OC_INBOX_USERNAME=controloc@hotelsales.cl  # Cambio
OC_INBOX_PASSWORD=[CONTRASEÑA_SEGURA]  # Cambio
OC_INBOX_MAILBOX=INBOX
OC_INBOX_USE_SSL=True
```

### 2. NO Requiere Cambios en Código Python

El sistema usa las librerías estándar:
- `imaplib` - Compatible con Office 365 IMAP
- `smtplib` - Compatible con Office 365 SMTP

**Verificación**:
```python
# El código actual en src/email_monitor.py y src/email_sender.py
# NO requiere cambios, solo actualizar .env
```

---

## 🧪 Plan de Pruebas

### Fase 1: Configuración de Office 365 (1-2 días)

**Checklist**:
- [ ] Crear cuenta `controloc@hotelsales.cl`
- [ ] Asignar licencia Office 365 Business Basic
- [ ] Habilitar IMAP/SMTP para la cuenta
- [ ] Habilitar SMTP AUTH
- [ ] Configurar contraseña fuerte
- [ ] Desactivar expiración de contraseña
- [ ] Verificar registros DNS (SPF, DKIM, DMARC)

### Fase 2: Pruebas de Conexión (1 día)

#### Test 1: Conexión IMAP

**Script de prueba**:
```python
import imaplib

host = "outlook.office365.com"
port = 993
username = "controloc@hotelsales.cl"
password = "[PASSWORD]"

try:
    mail = imaplib.IMAP4_SSL(host, port)
    mail.login(username, password)
    print("✅ Conexión IMAP exitosa")

    status, folders = mail.list()
    print(f"📁 Carpetas disponibles: {len(folders)}")

    mail.select("INBOX")
    status, messages = mail.search(None, 'ALL')
    print(f"📧 Correos en INBOX: {len(messages[0].split())}")

    mail.logout()
except Exception as e:
    print(f"❌ Error: {e}")
```

#### Test 2: Conexión SMTP

**Script de prueba**:
```python
import smtplib
from email.mime.text import MIMEText

host = "smtp.office365.com"
port = 587
username = "controloc@hotelsales.cl"
password = "[PASSWORD]"

try:
    # Conectar
    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(username, password)
    print("✅ Conexión SMTP exitosa")

    # Enviar correo de prueba
    msg = MIMEText("Test de conexión SMTP desde sistema de OC")
    msg['Subject'] = "Test - Sistema OC"
    msg['From'] = username
    msg['To'] = "tu_email_personal@ejemplo.com"

    server.send_message(msg)
    print("✅ Correo de prueba enviado")

    server.quit()
except Exception as e:
    print(f"❌ Error: {e}")
```

#### Test 3: Prueba End-to-End

1. **Enviar correo de confirmación** (desde cuenta autorizada):
   - De: `kontroltravel@ideasfractal.com`
   - A: `controloc@hotelsales.cl`
   - Asunto: "Confirmación de Reserva - Hotel Plaza"
   - Adjunto: PDF de confirmación

2. **Verificar detección automática**:
   - Sistema debe procesar PDF
   - Crear reserva en BD
   - Enviar solicitud inicial de OC

3. **Enviar respuesta de OC**:
   - De: Cliente (ej: `agencia@ejemplo.com`)
   - A: `controloc@hotelsales.cl`
   - Asunto: "Orden de Compra - Reserva XXXXXX"

4. **Verificar asociación automática**:
   - Sistema debe detectar OC
   - Actualizar estado a RECIBIDA
   - Detener flujo de recordatorios

### Fase 3: Migración en Producción (1 día)

#### Opción A: Migración Directa (RECOMENDADO si no hay reservas activas)

1. Detener sistema actual
2. Actualizar `.env` con nuevas credenciales
3. Reiniciar sistema
4. Monitorear logs durante 24 horas

#### Opción B: Migración Gradual (si hay reservas pendientes)

1. **Día 1**: Configurar Office 365, mantener Gmail activo
2. **Día 2-7**: Duplicar monitoreo (ambas cuentas)
3. **Día 8**: Actualizar `.env` a Office 365
4. **Día 9-14**: Monitorear, mantener Gmail como respaldo
5. **Día 15+**: Desactivar Gmail

---

## ⚠️ Consideraciones Importantes

### 1. Diferencias Office 365 vs. Gmail

| Aspecto | Gmail | Office 365 |
|---------|-------|------------|
| **Límite IMAP** | ~100 conexiones/día | Sin límite específico |
| **Límite SMTP** | 500 correos/día (cuentas gratuitas), 2000/día (Workspace) | 10,000 destinatarios/día |
| **Velocidad IMAP** | Rápido | Similar o ligeramente más lento |
| **Confiabilidad** | 99.9% uptime | 99.9% uptime (SLA) |
| **Detección de Spam** | Muy agresiva | Configurable |
| **Soporte** | Limitado (gratuito) | Email + teléfono (licencia pagada) |

### 2. Configuración Anti-Spam

**Office 365 puede marcar correos legítimos como spam**

**Solución**:
1. Agregar remitentes autorizados a lista blanca
2. Crear regla de flujo de correo (Mail Flow Rule):
   ```
   Si: Remitente es kontroltravel@ideasfractal.com
   Entonces: Establecer SCL (Spam Confidence Level) = -1 (bypass spam)
   ```

### 3. Costo Mensual

**Office 365 Business Basic**: USD $6/mes/usuario
- 1 usuario: `controloc@hotelsales.cl`
- **Costo total**: USD $6/mes = USD $72/año

**Comparación**:
- Gmail Workspace: USD $6/mes (similar)
- Gmail gratuito: $0 pero límites estrictos

### 4. Backup y Continuidad

**Office 365 NO incluye backup completo**

**Recomendaciones**:
1. **Exportar correos críticos** periódicamente
2. **Habilitar Litigation Hold** para compliance (si se requiere)
3. **Considerar servicio de backup** (ej: Veeam for Office 365) - Opcional

### 5. Monitoreo de Salud del Servicio

**Microsoft 365 Admin Center** → **Health** → **Service health**

Verificar:
- Estado de Exchange Online
- Incidentes activos
- Mantenimientos programados

---

## 📊 Checklist de Migración Completo

### Pre-Migración
- [ ] Adquirir licencia Office 365 Business Basic
- [ ] Verificar dominio `hotelsales.cl` en Office 365
- [ ] Crear cuenta `controloc@hotelsales.cl`
- [ ] Configurar contraseña segura
- [ ] Habilitar IMAP en la cuenta
- [ ] Habilitar SMTP AUTH en la cuenta
- [ ] Desactivar expiración de contraseña
- [ ] Verificar registros DNS (SPF, DKIM, DMARC)
- [ ] Agregar remitentes autorizados a lista blanca
- [ ] Crear reglas anti-spam

### Pruebas
- [ ] Test de conexión IMAP exitoso
- [ ] Test de conexión SMTP exitoso
- [ ] Test de recepción de correo
- [ ] Test de envío de correo
- [ ] Test end-to-end con PDF de confirmación
- [ ] Test de detección de OC
- [ ] Verificar que correos NO vayan a spam

### Migración
- [ ] Actualizar archivo `.env` con nuevas credenciales
- [ ] Encriptar `.env` o usar gestor de secretos
- [ ] Reiniciar sistema
- [ ] Verificar logs de conexión exitosa
- [ ] Monitorear durante 24 horas
- [ ] Notificar a stakeholders del cambio de email

### Post-Migración
- [ ] Actualizar documentación (README, .env.example)
- [ ] Comunicar nueva dirección a clientes: `controloc@hotelsales.cl`
- [ ] Actualizar firma de correos (si aplica)
- [ ] Configurar redirección temporal desde Gmail (opcional)
- [ ] Monitorear métricas durante 1 semana
- [ ] Desactivar cuenta Gmail (después de 30 días sin uso)

---

## 🆘 Troubleshooting Común

### Problema 1: "Authentication failed" en IMAP/SMTP

**Causas posibles**:
1. IMAP/SMTP no habilitado para el usuario
2. SMTP AUTH deshabilitado
3. Contraseña incorrecta
4. Usuario/contraseña con espacios extra

**Solución**:
```powershell
# Verificar configuración
Get-CASMailbox -Identity controloc@hotelsales.cl | Select-Object ImapEnabled,SmtpClientAuthenticationDisabled

# Debe retornar:
# ImapEnabled: True
# SmtpClientAuthenticationDisabled: False
```

### Problema 2: Correos van a spam

**Solución**:
1. Verificar SPF, DKIM, DMARC en https://mxtoolbox.com
2. Agregar IP del servidor a SPF (si usa servidor propio)
3. Crear regla anti-spam en Exchange Admin Center

### Problema 3: "Too many connections" (IMAP)

**Causa**: Office 365 limita conexiones simultáneas por IP

**Solución**:
- Aumentar `IMAP_CHECK_INTERVAL` en `.env` (de 60s a 120s)
- Cerrar conexiones correctamente después de cada verificación

### Problema 4: Lentitud en verificación de correos

**Causa**: Office 365 IMAP puede ser más lento que Gmail

**Solución**:
- Implementar caché de IDs de correos ya procesados
- Usar `IDLE` command de IMAP (push notifications) - Requiere cambio en código

---

## 📞 Soporte y Contactos

### Microsoft Support
- **Portal**: https://admin.microsoft.com/AdminPortal/Home#/support
- **Teléfono**: 1-800-865-9408 (USA) o desde Chile: 800-226-066
- **Chat**: Disponible en Admin Center

### Recursos Útiles
- **Configuración IMAP/SMTP**: https://support.microsoft.com/en-us/office/pop-imap-and-smtp-settings-8361e398-8af4-4e97-b147-6c6c4ac95353
- **Límites de Exchange Online**: https://docs.microsoft.com/en-us/office365/servicedescriptions/exchange-online-service-description/exchange-online-limits
- **DNS Records**: https://docs.microsoft.com/en-us/microsoft-365/admin/get-help-with-domains/create-dns-records-at-any-dns-hosting-provider

---

**Última actualización**: Diciembre 2025
**Próxima revisión**: Después de migración exitosa

# Habilitar IMAP en Office 365

## Problema Actual

```
❌ Error IMAP: b'LOGIN failed.'
✅ SMTP: Funcionando correctamente
```

**IMAP está deshabilitado** para el mailbox `recordatorio.oc@hotelsales.cl` en Office 365.

---

## Solución: Habilitar IMAP

### Opción 1: Microsoft 365 Admin Center (Más Fácil)

1. **Acceder al Admin Center**
   - Ve a **https://admin.microsoft.com**
   - Inicia sesión con cuenta de administrador

2. **Ir a Usuarios**
   - En el menú lateral: **Users** > **Active users**
   - Busca: `recordatorio.oc@hotelsales.cl`
   - Click en el usuario

3. **Habilitar IMAP**
   - Pestaña **Mail** o **Email apps**
   - Click en **Manage email apps**
   - **Activa** la casilla de **IMAP**
   - Click en **Save changes**

4. **Esperar propagación**
   - Espera **5-10 minutos** para que los cambios se apliquen

### Opción 2: Exchange Admin Center

1. **Acceder a Exchange Admin Center**
   - Ve a **https://admin.exchange.microsoft.com**
   - Inicia sesión con cuenta de administrador

2. **Configurar el Mailbox**
   - **Recipients** > **Mailboxes**
   - Busca y selecciona: `recordatorio.oc@hotelsales.cl`
   - Click en la pestaña **Mailbox**

3. **Email apps**
   - Click en **Manage email apps settings**
   - **Activa** IMAP
   - **Guarda** los cambios

### Opción 3: PowerShell (Más Rápido)

```powershell
# 1. Instalar módulo (solo primera vez)
Install-Module -Name ExchangeOnlineManagement

# 2. Conectar a Exchange Online
Connect-ExchangeOnline -UserPrincipalName admin@hotelsales.cl

# 3. Habilitar IMAP
Set-CASMailbox -Identity recordatorio.oc@hotelsales.cl -ImapEnabled $true

# 4. Verificar
Get-CASMailbox -Identity recordatorio.oc@hotelsales.cl | Select-Object ImapEnabled

# Debería devolver: ImapEnabled : True
```

---

## Verificar que Funciona

Después de habilitar IMAP, espera 5-10 minutos y ejecuta:

```bash
python test_office365_connection.py
```

Deberías ver:
```
✅ IMAP: Autenticación exitosa
✅ Mailbox 'INBOX' seleccionado correctamente
✅ SMTP: Autenticación exitosa
```

---

## Troubleshooting

### Si sigue fallando después de 10 minutos:

#### 1. Verificar que IMAP esté habilitado

```powershell
Connect-ExchangeOnline -UserPrincipalName admin@hotelsales.cl
Get-CASMailbox -Identity recordatorio.oc@hotelsales.cl | Format-List Imap*
```

Debe mostrar:
```
ImapEnabled                        : True
ImapUseProtocolDefaults            : True
ImapMessagesRetrievalMimeFormat    : BestBodyFormat
ImapEnableExactRFC822Size          : False
ImapProtocolLoggingEnabled         : False
ImapSuppressReadReceipt            : False
ImapForceICalForCalendarRetrievalOption : False
```

#### 2. Verificar App Password

Si usas autenticación multifactor (MFA), necesitas un **App Password**:

1. Ve a **https://account.microsoft.com/security**
2. **Security** > **Advanced security options**
3. **App passwords** > **Create a new app password**
4. Usa ese password en `.env` en lugar de la contraseña normal

#### 3. Verificar Seguridad de la Cuenta

Office 365 puede bloquear IMAP si detecta actividad sospechosa:

1. Ve a **https://protection.office.com**
2. **Threat management** > **Review**
3. Busca alertas del usuario `recordatorio.oc@hotelsales.cl`
4. Si hay bloqueos, desbloquea la cuenta

#### 4. Verificar Políticas de Autenticación

```powershell
# Ver política de autenticación del mailbox
Get-CASMailbox -Identity recordatorio.oc@hotelsales.cl | Select-Object AuthenticationPolicy

# Ver todas las políticas de autenticación
Get-AuthenticationPolicy
```

Si hay una política que bloquea protocolos legacy:

```powershell
# Crear política que permita IMAP
New-AuthenticationPolicy -Name "PermitirIMAP" -AllowBasicAuthImap

# Asignar al mailbox
Set-User -Identity recordatorio.oc@hotelsales.cl -AuthenticationPolicy "PermitirIMAP"
```

---

## Configuración Actual del Sistema

El sistema está configurado para usar **IMAP** (no Graph API):

```bash
# .env
USE_GRAPH_API=false
IMAP_HOST=outlook.office365.com
IMAP_PORT=993
IMAP_USERNAME=recordatorio.oc@hotelsales.cl
IMAP_PASSWORD=tzdmhtfczcgsdvkn
```

---

## Notas de Seguridad

### ⚠️ IMAP vs Graph API

| Aspecto | IMAP | Graph API |
|---------|------|-----------|
| **Seguridad** | ⚠️ Contraseña de app | ✅ OAuth 2.0 |
| **Microsoft recomienda** | ❌ Deprecado | ✅ Sí |
| **Requiere Azure** | ❌ No | ✅ Sí |
| **Fácil de configurar** | ✅ Sí | ⚠️ Complejo |

### Recomendación Actual

1. **Corto plazo**: Usar IMAP (funciona sin Azure)
2. **Largo plazo**: Migrar a Graph API cuando tengan tenant de Azure

El código ya está preparado para Graph API. Solo necesitas:
- Obtener suscripción de Azure
- Seguir: `docs/CONFIGURAR_AZURE_AD_GRAPH_API.md`
- Cambiar `USE_GRAPH_API=true` en `.env`

---

## Referencias

- [Configure IMAP access for a mailbox](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/pop3-and-imap4/enable-or-disable-pop3-or-imap4-access)
- [Exchange Online PowerShell](https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell)
- [App Passwords](https://support.microsoft.com/en-us/account-billing/manage-app-passwords-d6dc8c6d-4bf7-4851-ad95-6d07799387e9)

---

**Última actualización**: 12 de diciembre de 2025

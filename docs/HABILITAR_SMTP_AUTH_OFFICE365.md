# Habilitar SMTP AUTH en Office 365

## Problema

Error al conectar con Office 365:
```
SMTP Error: SmtpClientAuthentication is disabled for the Tenant
IMAP Error: LOGIN failed
```

## Causa

Microsoft 365 tiene deshabilitada la autenticación básica (SMTP AUTH) por defecto como medida de seguridad.

## Solución

### Opción 1: Habilitar SMTP AUTH para un Usuario Específico (Recomendado)

1. **Acceder al Exchange Admin Center**
   - Ve a https://admin.exchange.microsoft.com
   - Inicia sesión con credenciales de administrador

2. **Ir a Recipients > Mailboxes**
   - Busca el mailbox: `recordatorio.oc@hotelsales.cl`
   - Click en el mailbox para abrirlo

3. **Habilitar SMTP AUTH**
   - Ve a la pestaña **Mail Flow Settings** o **Configuración de flujo de correo**
   - Busca **Authenticated SMTP** o **SMTP autenticado**
   - **Activa** la casilla que dice "Enable Authenticated SMTP"
   - Click en **Save** o **Guardar**

4. **Verificar App Password**
   - Ve a https://account.microsoft.com/security
   - Genera un nuevo **App Password** para "Mail" o "IMAP/SMTP"
   - Usa este password en el `.env`

### Opción 2: Habilitar SMTP AUTH a Nivel de Tenant (Menos Seguro)

1. **PowerShell de Exchange Online**
   ```powershell
   # Conectar a Exchange Online
   Install-Module -Name ExchangeOnlineManagement
   Connect-ExchangeOnline -UserPrincipalName admin@hotelsales.cl

   # Habilitar SMTP AUTH para el usuario específico
   Set-CASMailbox -Identity recordatorio.oc@hotelsales.cl -SmtpClientAuthenticationDisabled $false

   # Verificar
   Get-CASMailbox -Identity recordatorio.oc@hotelsales.cl | Select-Object SmtpClientAuthenticationDisabled
   ```

2. **O habilitar para todo el tenant** (No recomendado)
   ```powershell
   # Habilitar SMTP AUTH para toda la organización
   Set-TransportConfig -SmtpClientAuthenticationDisabled $false
   ```

### Opción 3: Usar OAuth 2.0 (Más Seguro, Más Complejo)

Si la organización requiere OAuth 2.0 en lugar de autenticación básica:

1. **Registrar aplicación en Azure AD**
   - Ve a https://portal.azure.com
   - Azure Active Directory > App registrations
   - New registration
   - Configura permisos: `IMAP.AccessAsUser.All`, `SMTP.Send`

2. **Modificar el código para usar OAuth 2.0**
   - Implementar flujo de autenticación OAuth
   - Más complejo, pero más seguro

## Verificación

Después de habilitar SMTP AUTH, espera **5-10 minutos** para que los cambios se propaguen.

Luego ejecuta:
```bash
python test_office365_connection.py
```

## Troubleshooting

### Si sigue fallando:

1. **Verificar que el App Password sea correcto**
   ```bash
   # Editar .env y regenerar app password
   nano .env
   ```

2. **Verificar configuración del mailbox**
   ```powershell
   Get-CASMailbox -Identity recordatorio.oc@hotelsales.cl | Format-List
   ```

3. **Revisar logs de auditoría**
   - Exchange Admin Center > Mail flow > Message trace
   - Buscar intentos de autenticación fallidos

## Configuración IMAP

Si IMAP también está deshabilitado:

```powershell
# Habilitar IMAP para el usuario
Set-CASMailbox -Identity recordatorio.oc@hotelsales.cl -ImapEnabled $true

# Verificar
Get-CASMailbox -Identity recordatorio.oc@hotelsales.cl | Select-Object ImapEnabled
```

## Referencias

- [Habilitar SMTP AUTH en Exchange Online](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/authenticated-client-smtp-submission)
- [Autenticación básica en Exchange Online](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/enable-or-disable-modern-authentication-in-exchange-online)
- [App Passwords en Microsoft 365](https://support.microsoft.com/en-us/account-billing/manage-app-passwords-for-two-step-verification-d6dc8c6d-4bf7-4851-ad95-6d07799387e9)

## Notas de Seguridad

- **Recomendación**: Habilitar SMTP AUTH **solo** para el mailbox `recordatorio.oc@hotelsales.cl`
- **NO** habilitar para todo el tenant a menos que sea absolutamente necesario
- Usar **App Passwords** en lugar de contraseña principal
- Considerar migrar a **OAuth 2.0** para mayor seguridad en el futuro

---

**Última actualización**: 12 de diciembre de 2025

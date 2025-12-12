# Configurar Azure AD para Microsoft Graph API

## Descripción

Esta guía te ayudará a registrar una aplicación en Azure Active Directory para que el sistema pueda acceder a los correos de Office 365 usando Microsoft Graph API en lugar de IMAP/SMTP.

## Ventajas de Graph API vs IMAP

| Característica | Graph API | IMAP |
|----------------|-----------|------|
| **Seguridad** | OAuth 2.0, tokens de corta duración | Contraseña de app |
| **Permisos granulares** | ✅ Sí | ❌ No |
| **Recomendado por Microsoft** | ✅ Sí | ❌ Deprecado |
| **Funcionalidades avanzadas** | ✅ Muchas | ❌ Limitadas |
| **Requiere habilitar IMAP** | ❌ No | ✅ Sí |

---

## Paso 1: Registrar Aplicación en Azure AD

### 1.1 Acceder al Portal de Azure

1. Ve a **https://portal.azure.com**
2. Inicia sesión con tu cuenta de administrador de Microsoft 365

### 1.2 Navegar a Azure Active Directory

1. En el menú lateral, busca **Azure Active Directory**
2. O usa el buscador superior: escribe "Azure Active Directory"

### 1.3 Registrar Nueva Aplicación

1. En el menú de Azure AD, ve a:
   ```
   Azure Active Directory > App registrations > New registration
   ```

2. Completa el formulario:
   - **Name**: `Sistema Seguimiento OC` (o el nombre que prefieras)
   - **Supported account types**:
     - Selecciona: **Accounts in this organizational directory only (Single tenant)**
   - **Redirect URI**:
     - Deja en blanco por ahora (no lo necesitamos para daemon apps)

3. Click en **Register**

### 1.4 Copiar IDs Importantes

Después de registrar, verás la página de **Overview**. Copia estos valores:

```
Application (client) ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Directory (tenant) ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**Guarda estos valores**, los necesitarás para el `.env`

---

## Paso 2: Crear Client Secret

### 2.1 Navegar a Certificates & secrets

1. En tu aplicación registrada, ve a:
   ```
   Certificates & secrets > Client secrets > New client secret
   ```

2. Completa:
   - **Description**: `OC System Secret`
   - **Expires**:
     - Recomendado: **24 months** (2 años)
     - Para producción: considera usar certificados en lugar de secrets

3. Click en **Add**

### 2.2 Copiar el Secret

⚠️ **IMPORTANTE**: El **Value** del secret solo se muestra UNA VEZ.

```
Secret Value: xxxx~xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Cópialo inmediatamente** y guárdalo en un lugar seguro (lo usarás en `.env`)

---

## Paso 3: Configurar Permisos de API

### 3.1 Agregar Permisos de Microsoft Graph

1. Ve a:
   ```
   API permissions > Add a permission > Microsoft Graph
   ```

2. Selecciona **Application permissions** (no Delegated)

3. Busca y agrega estos permisos:

   | Permiso | Descripción |
   |---------|-------------|
   | **Mail.Read** | Leer correos de todos los buzones |
   | **Mail.ReadWrite** | Leer y marcar correos como leídos |
   | **Mail.Send** | Enviar correos |

4. Click en **Add permissions**

### 3.2 Grant Admin Consent

⚠️ **CRÍTICO**: Los permisos de aplicación requieren consentimiento de administrador.

1. Click en el botón:
   ```
   Grant admin consent for [Tu Organización]
   ```

2. Confirma en el popup

3. Verifica que todos los permisos muestren un **✓ verde** en la columna "Status"

---

## Paso 4: Configurar Acceso al Mailbox Específico

Por seguridad, vamos a restringir el acceso solo al mailbox `recordatorio.oc@hotelsales.cl`.

### 4.1 Conectar a Exchange Online PowerShell

```powershell
# Instalar módulo (solo primera vez)
Install-Module -Name ExchangeOnlineManagement

# Conectar
Connect-ExchangeOnline -UserPrincipalName admin@hotelsales.cl
```

### 4.2 Crear Application Access Policy

```powershell
# Restringir acceso solo al mailbox específico
New-ApplicationAccessPolicy `
    -AppId "TU_CLIENT_ID_AQUI" `
    -PolicyScopeGroupId recordatorio.oc@hotelsales.cl `
    -AccessRight RestrictAccess `
    -Description "Restringir acceso del sistema OC solo a recordatorio.oc"
```

Reemplaza `TU_CLIENT_ID_AQUI` con el **Application (client) ID** que copiaste en el Paso 1.4.

### 4.3 Verificar la Política

```powershell
# Ver todas las políticas
Get-ApplicationAccessPolicy

# Probar acceso (debe devolver "Granted")
Test-ApplicationAccessPolicy `
    -Identity recordatorio.oc@hotelsales.cl `
    -AppId "TU_CLIENT_ID_AQUI"
```

---

## Paso 5: Configurar el Sistema

### 5.1 Actualizar el archivo `.env`

Edita `/Users/cucho/.../envia2/.env`:

```bash
# ==================== MICROSOFT GRAPH API ====================
# Credenciales de Azure AD App Registration
AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_CLIENT_SECRET=xxxx~xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Mailbox a monitorear
GRAPH_MAILBOX_EMAIL=recordatorio.oc@hotelsales.cl

# ==================== SMTP (sigue usando Office 365) ====================
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USERNAME=recordatorio.oc@hotelsales.cl
SMTP_PASSWORD=tzdmhtfczcgsdvkn
SMTP_FROM_EMAIL=recordatorio.oc@hotelsales.cl
SMTP_FROM_NAME=Kontrol Travel - Administración
SMTP_USE_TLS=True
```

### 5.2 Probar la Conexión

```bash
# Ejecutar script de prueba
python test_graph_connection.py
```

Deberías ver:
```
✅ Autenticación Graph API exitosa
✅ Acceso al mailbox recordatorio.oc@hotelsales.cl: OK
✅ Lectura de correos: OK
✅ SMTP: OK
```

---

## Paso 6: Instalar Dependencias

```bash
pip install msal msgraph-sdk
```

O actualiza `requirements.txt` y ejecuta:
```bash
pip install -r requirements.txt
```

---

## Troubleshooting

### Error: "Insufficient privileges to complete the operation"

**Causa**: Falta el "Grant admin consent" para los permisos.

**Solución**: Ve a Paso 3.2 y otorga el consentimiento de administrador.

### Error: "Application is not authorized to access this mailbox"

**Causa**: No se configuró la Application Access Policy.

**Solución**: Ejecuta los comandos del Paso 4.2.

### Error: "AADSTS700016: Application with identifier was not found"

**Causa**: El Client ID o Tenant ID son incorrectos.

**Solución**: Verifica los valores en Azure Portal > App registrations.

### Error: "Invalid client secret provided"

**Causa**: El Client Secret expiró o es incorrecto.

**Solución**:
1. Azure Portal > App registrations > Tu app > Certificates & secrets
2. Genera un nuevo secret
3. Actualiza `.env` con el nuevo valor

---

## Seguridad

### Mejores Prácticas

1. **Usar Certificados en Producción**
   - En lugar de Client Secret, usa certificados X.509
   - Más seguro y recomendado para producción

2. **Rotar Secrets Regularmente**
   - Crea nuevos secrets cada 6-12 meses
   - Antes de que expiren los actuales

3. **Application Access Policy**
   - ✅ Siempre restringe el acceso a mailboxes específicos
   - ❌ Nunca des acceso global a todos los buzones

4. **Auditar Acceso**
   ```powershell
   # Ver logs de acceso de la aplicación
   Search-UnifiedAuditLog -StartDate (Get-Date).AddDays(-7) -EndDate (Get-Date) | Where-Object {$_.Operations -like "*ApplicationAccess*"}
   ```

---

## Referencias Oficiales

- [Register an application with Azure AD](https://learn.microsoft.com/en-us/graph/auth-register-app-v2)
- [Get access without a user](https://learn.microsoft.com/en-us/graph/auth-v2-service)
- [Use application access policy](https://learn.microsoft.com/en-us/graph/auth-limit-mailbox-access)
- [Microsoft Graph API - Mail](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview)

---

## Resumen de Valores Necesarios

Al final de esta guía, debes tener estos 3 valores para configurar el `.env`:

```bash
AZURE_CLIENT_ID=........  # Application (client) ID
AZURE_CLIENT_SECRET=....  # Client secret value
AZURE_TENANT_ID=........  # Directory (tenant) ID
```

**Siguiente paso**: Una vez tengas estos valores, ejecuta:
```bash
python test_graph_connection.py
```

---

**Última actualización**: 12 de diciembre de 2025

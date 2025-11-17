# 🚀 Instalación y Configuración del Sistema de OC en n8n

## 📋 Tabla de Contenidos

1. [¿Qué es n8n?](#qué-es-n8n)
2. [Ventajas de usar n8n](#ventajas-de-usar-n8n)
3. [Requisitos Previos](#requisitos-previos)
4. [Instalación de n8n](#instalación-de-n8n)
5. [Configuración de Base de Datos](#configuración-de-base-de-datos)
6. [Importar Workflows](#importar-workflows)
7. [Configurar Credenciales](#configurar-credenciales)
8. [Activar Workflows](#activar-workflows)
9. [Verificación y Pruebas](#verificación-y-pruebas)
10. [Despliegue en Producción](#despliegue-en-producción)

---

## ¿Qué es n8n?

n8n es una plataforma de automatización de flujos de trabajo **gratuita y de código abierto** que permite:
- Crear automaciones visuales sin escribir código
- Conectar múltiples servicios y APIs
- Ejecutar workflows programados
- Procesar datos en tiempo real
- Auto-hospedarse (self-hosted) sin límites

**Sitio oficial:** https://n8n.io

---

## Ventajas de usar n8n

✅ **vs Sistema Python actual:**

| Característica | Python/FastAPI | n8n |
|----------------|----------------|-----|
| **Facilidad de configuración** | Requiere código | Visual, sin código |
| **Modificaciones** | Editar código Python | Arrastrar y soltar nodos |
| **Monitoreo** | Logs en archivos | Dashboard visual en tiempo real |
| **Debugging** | Revisar logs | Ver datos en cada paso |
| **Escalabilidad** | Manual | Automática con workers |
| **Costo** | Gratis | Gratis (self-hosted) |
| **Mantenimiento** | Alto (código) | Bajo (visual) |

✅ **Ideal para:**
- Equipos no técnicos que necesiten modificar flujos
- Visualizar el estado de cada ejecución
- Probar cambios sin riesgo de romper código
- Escalar fácilmente agregando más workers

---

## Requisitos Previos

### 1. Sistema Operativo
- **Linux** (Ubuntu 20.04+ recomendado)
- **macOS** (para desarrollo local)
- **Windows** (con WSL2)

### 2. Software Necesario

```bash
# Node.js 18+ (requerido)
node --version  # Debe ser v18.0.0 o superior

# PostgreSQL 12+ (recomendado para producción)
psql --version

# Docker (opcional, método alternativo de instalación)
docker --version
```

### 3. Cuentas y Servicios

- ✅ Cuenta de Gmail (2 cuentas para pruebas)
- ✅ Base de datos PostgreSQL (puede ser local o cloud)
- ✅ Servidor con mínimo 2GB RAM (para producción)

---

## Instalación de n8n

### Método 1: Instalación con npm (Recomendado para desarrollo)

```bash
# Instalar n8n globalmente
npm install -g n8n

# Verificar instalación
n8n --version

# Iniciar n8n
n8n start
```

n8n se iniciará en: **http://localhost:5678**

### Método 2: Docker (Recomendado para producción)

```bash
# Crear directorio para datos
mkdir -p ~/.n8n

# Iniciar n8n con Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Método 3: Docker Compose (Mejor para producción con PostgreSQL)

Crear archivo `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: n8n_password
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -h localhost -U n8n']
      interval: 5s
      timeout: 5s
      retries: 10

  n8n:
    image: n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=n8n_password
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin123
      - WEBHOOK_URL=https://tu-dominio.com/
    volumes:
      - n8n_data:/home/node/.n8n
      - ./oc_files:/home/node/oc_files
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
  n8n_data:
```

Iniciar:
```bash
docker-compose up -d
```

---

## Configuración de Base de Datos

### 1. Crear Base de Datos para Reservas

```sql
-- Conectar a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE reservas_oc;

-- Conectar a la base de datos
\c reservas_oc

-- Crear tablas (usar el schema de database.py)
```

Ejecutar el script de creación de tablas:

```bash
# Desde el directorio del proyecto Python
python -c "from database import init_db; init_db()"
```

O manualmente ejecutar SQL:

```sql
CREATE TYPE estado_oc AS ENUM ('PENDIENTE', 'RECIBIDA', 'EXPIRADA', 'CANCELADA');
CREATE TYPE tipo_correo AS ENUM ('SOLICITUD_INICIAL', 'RECORDATORIO_DIA2', 'ULTIMATUM_DIA4');

CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    id_reserva VARCHAR(50) UNIQUE NOT NULL,
    loc_interno VARCHAR(50) NOT NULL,
    localizador VARCHAR(50),
    agencia VARCHAR(200) NOT NULL,
    nombre_hotel VARCHAR(300),
    direccion_hotel TEXT,
    telefono_hotel VARCHAR(50),
    fecha_checkin DATE,
    fecha_checkout DATE,
    hora_llegada VARCHAR(20),
    hora_salida VARCHAR(20),
    numero_noches INTEGER,
    numero_habitaciones INTEGER,
    monto_total DECIMAL(12, 2),
    moneda VARCHAR(3) DEFAULT 'CLP',
    fecha_emision TIMESTAMP,
    requiere_oc BOOLEAN DEFAULT FALSE,
    estado_oc estado_oc,
    fecha_oc_recibida TIMESTAMP,
    email_origen_id VARCHAR(100),
    email_origen_fecha TIMESTAMP,
    pdf_filename VARCHAR(300),
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP DEFAULT NOW()
);

CREATE TABLE correos_enviados (
    id SERIAL PRIMARY KEY,
    reserva_id INTEGER REFERENCES reservas(id) ON DELETE CASCADE,
    tipo_correo tipo_correo NOT NULL,
    destinatario VARCHAR(200) NOT NULL,
    asunto TEXT,
    enviado_exitosamente BOOLEAN DEFAULT FALSE,
    error_mensaje TEXT,
    fecha_envio TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ordenes_compra (
    id SERIAL PRIMARY KEY,
    reserva_id INTEGER UNIQUE REFERENCES reservas(id) ON DELETE CASCADE,
    email_remitente VARCHAR(200),
    email_asunto TEXT,
    email_fecha TIMESTAMP,
    email_id VARCHAR(100),
    archivo_nombre VARCHAR(300),
    archivo_tamano INTEGER,
    archivo_ruta TEXT,
    fecha_recepcion TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reservas_estado ON reservas(estado_oc);
CREATE INDEX idx_reservas_agencia ON reservas(agencia);
CREATE INDEX idx_reservas_fecha_checkin ON reservas(fecha_checkin);
```

---

## Importar Workflows

### 1. Acceder a n8n

Abre tu navegador y ve a: **http://localhost:5678**

Primera vez:
- Crea una cuenta (usuario y contraseña)
- Completa el onboarding

### 2. Importar cada Workflow

Para cada archivo JSON en la carpeta `n8n/`:

1. **Click en "+" (agregar workflow)**
2. **Click en "..." (menú) → Import from File**
3. **Selecciona el archivo JSON:**
   - `workflow_monitoreo_reservas.json`
   - `workflow_recordatorios.json`
   - `workflow_deteccion_oc.json`

4. **Click en "Save"**

Repite para los 3 workflows.

---

## Configurar Credenciales

### 1. Gmail OAuth2 (IMAP)

En n8n:
1. Ve a **Settings** (⚙️) → **Credentials**
2. Click en **"+ New Credential"**
3. Busca: **"Gmail OAuth2 API"**
4. Completa:
   - **Name**: `Gmail IMAP OAuth2`
   - **Client ID**: (obtener de Google Cloud Console)
   - **Client Secret**: (obtener de Google Cloud Console)
5. Click en **"Connect my account"**
6. Autoriza en Google

**Obtener Client ID y Secret:**
1. Ve a: https://console.cloud.google.com
2. Crea nuevo proyecto o selecciona existente
3. **APIs & Services** → **Credentials**
4. **Create Credentials** → **OAuth 2.0 Client ID**
5. Tipo: **Web application**
6. **Authorized redirect URIs**: `http://localhost:5678/rest/oauth2-credential/callback`
7. Copia Client ID y Client Secret

### 2. Gmail OAuth2 (SMTP)

Repetir proceso anterior con nombre: `Gmail SMTP OAuth2`

### 3. Gmail OC Inbox OAuth2

Si usas una cuenta separada para recibir OC:
- Repetir proceso con nombre: `Gmail OC Inbox OAuth2`
- Usar credenciales de la segunda cuenta Gmail

### 4. PostgreSQL

1. **Settings** → **Credentials**
2. **New Credential** → **Postgres**
3. Completar:
   - **Name**: `PostgreSQL Reservas`
   - **Host**: `localhost` (o tu host de DB)
   - **Database**: `reservas_oc`
   - **User**: `n8n` (o tu usuario)
   - **Password**: (tu contraseña)
   - **Port**: `5432`
   - **SSL**: activar si es remoto
4. **Test** → **Save**

---

## Activar Workflows

### 1. Workflow: Monitoreo de Reservas

1. Abre el workflow `Monitoreo de Reservas - Detección de PDFs`
2. Verifica que todos los nodos estén correctamente configurados
3. En cada nodo que use credenciales, selecciona la credencial correspondiente
4. Click en **"Active"** (toggle arriba a la derecha)

Estado: **Active** ✅

### 2. Workflow: Recordatorios

1. Abre `Recordatorios de OC Pendientes`
2. Configura credenciales en nodos
3. **Ajustar intervalo** (actualmente cada 6 horas):
   - Click en nodo "Cada 6 Horas"
   - Cambiar a tu preferencia (ej: cada 12 horas, cada día)
4. Activar: **Active** ✅

### 3. Workflow: Detección de OC

1. Abre `Detección de OC Recibidas`
2. Configura credenciales
3. Verificar email de recepción en el nodo "Leer Correos OC":
   - Por defecto: `to:oc@kontroltravel.com`
   - Cambiar si usas otro email
4. Activar: **Active** ✅

---

## Verificación y Pruebas

### Test 1: Enviar Correo de Prueba con PDF

```bash
# Desde el directorio del proyecto Python
python enviar_prueba.py
```

Selecciona opción 1 (Confirmación de reserva) y adjunta un PDF de prueba.

### Test 2: Monitorear Ejecución en n8n

1. Ve a **Executions** (lado izquierdo)
2. Deberías ver ejecuciones del workflow "Monitoreo de Reservas"
3. Click en una ejecución para ver detalles
4. Verificar que:
   - ✅ Correo fue leído
   - ✅ PDF fue detectado
   - ✅ Datos fueron extraídos
   - ✅ Se guardó en base de datos
   - ✅ Se envió correo de solicitud OC

### Test 3: Verificar Base de Datos

```sql
-- Ver reservas creadas
SELECT * FROM reservas ORDER BY fecha_creacion DESC LIMIT 5;

-- Ver correos enviados
SELECT * FROM correos_enviados ORDER BY fecha_envio DESC LIMIT 5;
```

### Test 4: Probar Detección de OC

1. Responde al correo de solicitud con un PDF adjunto
2. Incluye en el asunto o cuerpo: "ID: [el_id_de_reserva]" o "LOC: [el_loc_interno]"
3. Envía a la cuenta configurada para OC
4. Espera 2 minutos (intervalo del workflow)
5. Verifica en **Executions** que se ejecutó "Detección de OC"
6. Verifica en DB:

```sql
SELECT * FROM reservas WHERE estado_oc = 'RECIBIDA';
SELECT * FROM ordenes_compra;
```

---

## Despliegue en Producción

### Opción 1: Servidor Linux con Docker Compose

```bash
# En tu servidor (ej: GCP VM, AWS EC2, DigitalOcean)

# 1. Instalar Docker y Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 2. Clonar configuración
mkdir ~/n8n-oc-system
cd ~/n8n-oc-system

# 3. Crear docker-compose.yml (copiar el de arriba)
nano docker-compose.yml

# 4. Configurar variables de entorno
nano .env

# Contenido de .env:
POSTGRES_PASSWORD=tu_password_seguro
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=password_seguro
WEBHOOK_URL=https://tu-dominio.com

# 5. Iniciar servicios
docker-compose up -d

# 6. Ver logs
docker-compose logs -f n8n
```

### Opción 2: n8n Cloud (Pago)

Si prefieres no mantener infraestructura:
1. Crea cuenta en: https://n8n.cloud
2. Planes desde $20/mes
3. Importa los workflows
4. Configura credenciales
5. Activa workflows

**Ventajas:**
- Sin mantenimiento de servidores
- Backups automáticos
- SSL incluido
- Soporte oficial

### Configurar HTTPS (Producción)

Si usas tu propio servidor:

```bash
# 1. Instalar Nginx
sudo apt install nginx

# 2. Configurar reverse proxy
sudo nano /etc/nginx/sites-available/n8n

# Contenido:
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:5678;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# 3. Activar sitio
sudo ln -s /etc/nginx/sites-available/n8n /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 4. Instalar SSL con Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

### Monitoreo en Producción

```bash
# Ver ejecuciones fallidas
docker-compose exec n8n n8n execute --workflow="Monitoreo de Reservas"

# Ver logs en tiempo real
docker-compose logs -f n8n

# Verificar estado de contenedores
docker-compose ps

# Reiniciar servicio
docker-compose restart n8n
```

---

## 🔧 Mantenimiento

### Backups

```bash
# Backup de base de datos PostgreSQL
docker-compose exec postgres pg_dump -U n8n n8n > backup_n8n_$(date +%Y%m%d).sql
docker-compose exec postgres pg_dump -U n8n reservas_oc > backup_reservas_$(date +%Y%m%d).sql

# Backup de workflows (exportar desde UI)
# Settings → Import/Export → Export all workflows
```

### Actualización de n8n

```bash
# Método Docker Compose
docker-compose pull
docker-compose up -d

# Método npm
npm update -g n8n
```

---

## ❓ FAQ

**P: ¿Puedo modificar los workflows sin conocimientos de programación?**
R: Sí, n8n es 100% visual. Puedes arrastrar, soltar y configurar nodos sin escribir código.

**P: ¿Cuánto cuesta n8n?**
R: n8n es gratis si lo auto-hospedas (self-hosted). Solo pagas por el servidor donde lo ejecutas.

**P: ¿Qué pasa si un workflow falla?**
R: n8n guarda el historial de ejecuciones. Puedes ver exactamente dónde falló, qué datos tenía, y re-ejecutarlo.

**P: ¿Puedo usar n8n con mi sistema Python actual?**
R: Sí, puedes usar ambos en paralelo o migrar gradualmente.

**P: ¿Es seguro para datos sensibles?**
R: Sí, al auto-hospedar tienes control total. Las credenciales se encriptan en la base de datos.

---

## 📚 Recursos Adicionales

- **Documentación oficial n8n**: https://docs.n8n.io
- **Comunidad n8n**: https://community.n8n.io
- **Workflows de ejemplo**: https://n8n.io/workflows
- **API Reference**: https://docs.n8n.io/api/

---

**¿Necesitas ayuda?** Revisa los workflows de ejemplo en la carpeta `n8n/` y consulta la guía de configuración.

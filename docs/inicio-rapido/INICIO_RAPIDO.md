# 🚀 Inicio Rápido - Prueba Local con Gmail

Guía rápida para probar el sistema en 10 minutos con cuentas Gmail.

**Versión**: 1.3.2 | **Última actualización**: 9 de Diciembre de 2024

> **⚠️ Nota Importante**: Todos los comandos de scripts Python requieren `PYTHONPATH=.` para funcionar correctamente.
> **💡 Tip**: Usa el script wrapper `./run_script.sh` para ejecutar scripts de forma más fácil.

---

## ⚡ Setup en 4 Pasos

### 1️⃣ Instalar Dependencias

```bash
cd envia2
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Configurar Gmail

**Para CADA cuenta Gmail que uses:**

1. Ve a https://myaccount.google.com/security
2. Habilita "Verificación en 2 pasos"
3. Ve a "Contraseñas de aplicaciones"
4. Genera una contraseña para "Correo"
5. Guarda la contraseña (16 caracteres, sin espacios)

📘 **Guía detallada**: `docs/configuracion/CONFIGURACION_GMAIL.md`

### 3️⃣ Configurar `.env`

```bash
cp .env.example .env
nano .env  # o usa tu editor preferido
```

**Configuración mínima:**

```bash
# Cuenta Gmail que recibe confirmaciones de reservas
IMAP_HOST=imap.gmail.com
IMAP_USERNAME=seguimientoocx@gmail.com
IMAP_PASSWORD=abcd efgh ijkl mnop    # ← Contraseña de aplicación (SIN espacios)

# Cuenta Gmail que envía solicitudes de OC
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=reservasonline@hotelsales.cl
SMTP_PASSWORD=wxyz abcd efgh ijkl    # ← Contraseña de aplicación (SIN espacios)
SMTP_FROM_EMAIL=reservasonline@hotelsales.cl

# Cuenta para recibir OC (puede ser la misma que IMAP)
OC_INBOX_HOST=imap.gmail.com
OC_INBOX_USERNAME=seguimientoocx@gmail.com
OC_INBOX_PASSWORD=abcd efgh ijkl mnop

# Base de datos (ya configurada)
DATABASE_URL=sqlite:///./data/oc_seguimiento.db

# Remitentes autorizados para confirmaciones
ALLOWED_CONFIRMATION_SENDERS=reservasonline@hotelsales.cl,v.rodriguezy@gmail.com,cuchohbk@gmail.com

# Clientes que requieren OC (opcional si cargas desde Excel)
AGENCIES_REQUIRING_OC=WALVIS S.A.,EMPRESA CORPORATIVA LTDA

# ⚡ Tiempos acelerados para pruebas (opcional)
DAYS_FOR_REMINDER_1=0         # Enviar recordatorio inmediatamente
DAYS_FOR_REMINDER_2=0         # Enviar ultimátum inmediatamente
IMAP_CHECK_INTERVAL=60        # Verificar correos cada 60 segundos
```

### 4️⃣ Inicializar Base de Datos

```bash
# Crear tablas y configuración inicial
PYTHONPATH=. python scripts/database/crear_bd.py

# (Opcional) Cargar 79 clientes desde Excel
PYTHONPATH=. python scripts/database/cargar_clientes_excel.py
```

**💡 Tip**: También puedes usar el wrapper para no escribir `PYTHONPATH=.` cada vez:
```bash
./run_script.sh scripts/database/crear_bd.py
./run_script.sh scripts/database/cargar_clientes_excel.py
```

---

## 🚀 Iniciar el Sistema

### Opción A: Script de Gestión (Recomendado)

```bash
./scripts/gestion/gestionar_sistema.sh start
```

El sistema iniciará en segundo plano.

### Opción B: Inicio Manual

```bash
python app.py
```

El sistema iniciará en primer plano (verás los logs en consola).

### Verificar que está corriendo

```bash
./scripts/gestion/gestionar_sistema.sh status
```

### Acceder al Dashboard

Abre en tu navegador:
- **Dashboard principal**: http://localhost:8001
- **Todas las reservas**: http://localhost:8001/reservas
- **Gestión de clientes**: http://localhost:8001/clientes
- **API REST docs**: http://localhost:8001/docs

---

## 📧 Enviar Correos de Prueba

### Opción A: Script Automático (FÁCIL) ⭐

```bash
PYTHONPATH=. python scripts/utils/enviar_prueba.py
# O con el wrapper
./run_script.sh scripts/utils/enviar_prueba.py
```

Selecciona:
- **1** = Enviar confirmación de reserva con PDF
- **2** = Enviar orden de compra

### Opción B: Generar PDF de Prueba

```bash
PYTHONPATH=. python scripts/testing/generar_pdf_prueba.py
# O con el wrapper
./run_script.sh scripts/testing/generar_pdf_prueba.py
```

Esto genera un PDF de prueba que puedes adjuntar manualmente.

### Opción C: Manual desde Gmail

**1. Enviar Confirmación de Reserva:**
- **Para:** seguimientoocx@gmail.com (tu casilla de monitoreo)
- **Asunto:** Confirmación de Reserva Hotel
  - O: "Resumen del Servicio"
  - O: "Reserva confirmada"
- **Adjunto:** PDF con datos de reserva (ver `data/reservas_prueba/`)
- **Importante**: El PDF debe contener:
  - ID de reserva o LOC Interno
  - Nombre de agencia (debe estar en BD)
  - Monto total (13+ formatos soportados)

**2. Enviar Orden de Compra (después de recibir solicitud):**
- **Para:** seguimientoocx@gmail.com
- **Asunto:**
  - "OC para Reserva AAFVDUA"
  - O: "Orden de Compra - Reserva AAFVDUA"
  - O: "OC AAFVDUA"
  - O: "LOC TEST2024001 - Adjunto OC"
- **Adjunto:** Cualquier PDF

---

## ✅ Qué Debería Pasar

### Flujo Completo de Prueba:

1. ✅ **Envías confirmación** con PDF adjunto
2. ✅ **Sistema detecta correo** (en ~60 segundos)
3. ✅ **Extrae datos del PDF** (id_reserva, agencia, monto, etc.)
4. ✅ **Verifica si requiere OC** (consulta BD de clientes)
5. ✅ **Crea reserva en BD** con estado PENDIENTE
6. ✅ **Envía solicitud de OC automáticamente** (día 0)
7. ✅ **Envías OC** con código de reserva en asunto
8. ✅ **Sistema detecta OC** (múltiples patrones)
9. ✅ **Marca como RECIBIDA** y detiene recordatorios

### Ver Resultados:

- 🌐 **Dashboard**: http://localhost:8001
  - Estadísticas en tiempo real
  - Reservas pendientes
  - OC recibidas recientemente

- 📋 **Vista de Reservas**: http://localhost:8001/reservas
  - Todas las reservas con filtros
  - Búsqueda en tiempo real
  - Días transcurridos desde solicitud

- 👥 **Gestión de Clientes**: http://localhost:8001/clientes
  - 79 clientes configurados
  - Filtros por requiere/no requiere OC

- 📊 **API REST**: http://localhost:8001/api/stats
  ```bash
  curl http://localhost:8001/api/stats
  ```

- 📝 **Logs del Sistema**:
  ```bash
  ./scripts/gestion/gestionar_sistema.sh logs
  # O directamente:
  tail -f logs/sistema.log
  ```

---

## 🔍 Verificar el Sistema

### Ver Estado del Sistema

```bash
./scripts/gestion/gestionar_sistema.sh status
```

### Verificar Correos en Inbox

```bash
PYTHONPATH=. python scripts/testing/check_inbox.py
```

### Verificar Configuración

```bash
python config.py
```

### Verificar Base de Datos

```bash
# Ver estadísticas
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --stats

# Listar todas las reservas
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --list
```

### Probar Conexión IMAP/SMTP

```bash
PYTHONPATH=. python scripts/utils/test_conexion.py
```

**💡 Tip**: Usa `./run_script.sh` para no escribir `PYTHONPATH=.` en cada comando.

---

## 🐛 Problemas Comunes

### ❌ "Error de autenticación Gmail"

**Causa**: Usando contraseña normal en lugar de contraseña de aplicación

**Solución**:
1. Ve a https://myaccount.google.com/security
2. Habilita "Verificación en 2 pasos" (si no está)
3. Ve a "Contraseñas de aplicaciones"
4. Genera nueva contraseña para "Correo"
5. Úsala en `.env` (16 caracteres, SIN espacios)

### ❌ "No se detectan correos"

**Posibles causas y soluciones**:

1. **IMAP no habilitado**:
   - Ve a Gmail → Configuración → Ver todos los ajustes → Reenvío y correo POP/IMAP
   - Habilita IMAP

2. **Remitente no autorizado**:
   - Verifica que el remitente esté en `ALLOWED_CONFIRMATION_SENDERS` en `.env`
   - Por defecto: reservasonline@hotelsales.cl, v.rodriguezy@gmail.com, cuchohbk@gmail.com

3. **Asunto no reconocido**:
   - Usa palabras clave: "confirmación", "reserva", "resumen", "servicio", "hotel"

4. **PDF sin datos requeridos**:
   - El PDF debe tener: id_reserva, loc_interno, agencia, monto_total
   - Ver logs para ver qué campos faltan

### ❌ "No se envían correos"

**Verificar**:
```bash
# Verificar configuración SMTP
grep SMTP .env

# Debe tener:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=True
```

### ❌ "ModuleNotFoundError"

**Causa**: Falta configurar PYTHONPATH para encontrar los módulos

**Solución**:
```bash
# ✅ Correcto - desde la raíz con PYTHONPATH
cd /ruta/al/proyecto/envia2
PYTHONPATH=. python scripts/database/crear_bd.py

# ✅ O usando el wrapper
./run_script.sh scripts/database/crear_bd.py

# ❌ Incorrecto - sin PYTHONPATH
python scripts/database/crear_bd.py  # Esto fallará

# ❌ Incorrecto - desde subdirectorio
cd scripts/database
python crear_bd.py  # Esto fallará
```

### ❌ "El sistema no guarda reservas"

**Verificar**:
1. El PDF contiene todos los campos requeridos
2. El nombre de agencia coincide exactamente con la BD
3. Los logs para ver errores: `tail -f logs/sistema.log`

---

## 🧪 Limpiar Datos de Prueba

### Menú Interactivo

```bash
PYTHONPATH=. python scripts/database/limpiar_base_datos.py
```

Opciones:
- Ver estadísticas
- Listar reservas
- Eliminar reserva específica
- Eliminar solo TEST*
- Eliminar todas las OC
- Eliminar TODO

### Comandos Directos

```bash
# Ver estadísticas
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --stats

# Eliminar solo reservas de prueba (TEST*)
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --test

# Eliminar todas las órdenes de compra
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --oc

# Eliminar TODO (requiere confirmación)
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --all
```

---

## 🛑 Detener el Sistema

### Script de Gestión

```bash
./scripts/gestion/gestionar_sistema.sh stop
```

### Alternativas

```bash
# Python con confirmación
python scripts/gestion/detener_sistema.py

# Python sin confirmación
python scripts/gestion/detener_sistema.py --force

# Bash rápido
./scripts/gestion/detener_sistema.sh
```

---

## 📚 Más Información

- **Guía Completa de Pruebas**: `docs/inicio-rapido/GUIA_PRUEBA_LOCAL.md`
- **Documentación Principal**: `README.md`
- **Estructura del Proyecto**: `ESTRUCTURA_PROYECTO.md`
- **Documentación de Scripts**: `scripts/README.md`
- **Índice de Docs**: `docs/README.md`
- **Troubleshooting**: `docs/troubleshooting/TROUBLESHOOTING.md`
- **Diagramas del Sistema**: `docs/DIAGRAMAS.md`
- **API REST**: http://localhost:8001/docs

---

## 🎯 Flujo de Prueba Completo (Comando por Comando)

```bash
# 1. Clonar y preparar entorno
cd envia2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configurar
cp .env.example .env
nano .env  # Editar con tus credenciales Gmail

# 3. Inicializar base de datos
python scripts/database/crear_bd.py

# 4. (Opcional) Cargar clientes desde Excel
python scripts/database/cargar_clientes_excel.py

# 5. Iniciar sistema
./scripts/gestion/gestionar_sistema.sh start

# 6. Ver estado
./scripts/gestion/gestionar_sistema.sh status

# 7. En otra terminal: Enviar correo de prueba
python scripts/utils/enviar_prueba.py

# 8. Ver dashboard
open http://localhost:8001
# O en Linux: xdg-open http://localhost:8001
# O en Windows: start http://localhost:8001

# 9. Ver logs en tiempo real
./scripts/gestion/gestionar_sistema.sh logs

# 10. Cuando termines: Detener sistema
./scripts/gestion/gestionar_sistema.sh stop
```

---

## 🆕 Novedades v1.3.0

- ✨ **Sistema de gestión integrado**: `gestionar_sistema.sh` (start/stop/restart/status/logs)
- ✨ **Scripts organizados por categoría**: gestion/, database/, testing/, utils/
- ✨ **Nueva vista /reservas**: Completa con filtros y búsqueda
- ✨ **Nueva vista /clientes**: Gestión de 79 clientes
- ✨ **Base de datos en data/**: Centralización de archivos de datos
- ✨ **Documentación reorganizada**: Por categorías temáticas

---

¡Listo! En menos de 10 minutos tendrás el sistema funcionando. 🚀

**¿Problemas?** → `docs/troubleshooting/TROUBLESHOOTING.md`

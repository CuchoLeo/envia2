# Scripts del Sistema de Seguimiento OC

Esta carpeta contiene todos los scripts utilitarios del sistema, organizados por categoría.

## 📁 Estructura

```
scripts/
├── gestion/          # Scripts para gestionar el sistema (iniciar/detener/monitorear)
├── database/         # Scripts relacionados con la base de datos
├── testing/          # Scripts para pruebas y diagnóstico
└── utils/            # Utilidades generales
```

---

## 🔧 Cómo Ejecutar los Scripts

### IMPORTANTE: Todos los scripts deben ejecutarse desde la raíz del proyecto

**Los scripts Python requieren que el directorio actual esté en el PYTHONPATH para encontrar los módulos.**

```bash
# ✅ Correcto - desde la raíz del proyecto con PYTHONPATH
cd /ruta/al/proyecto/envia2
PYTHONPATH=. python scripts/database/crear_bd.py

# ✅ Alternativa - usando el wrapper (recomendado)
./run_script.sh scripts/database/crear_bd.py

# ❌ Incorrecto - sin PYTHONPATH
python scripts/database/crear_bd.py  # Fallará: ModuleNotFoundError

# ❌ Incorrecto - desde dentro de scripts/
cd scripts/database
python crear_bd.py  # Fallará con import errors
```

### Script Wrapper (Recomendado)

Para facilitar la ejecución, usa el script wrapper `run_script.sh`:

```bash
# El wrapper automáticamente configura PYTHONPATH
./run_script.sh scripts/database/limpiar_base_datos.py
./run_script.sh scripts/testing/check_inbox.py
./run_script.sh scripts/utils/test_conexion.py
```

---

## 📂 Categorías de Scripts

### 1. Gestión del Sistema (`gestion/`)

Scripts para controlar el sistema (iniciar, detener, monitorear):

```bash
# Gestión completa del sistema
./scripts/gestion/gestionar_sistema.sh start     # Iniciar el sistema
./scripts/gestion/gestionar_sistema.sh stop      # Detener el sistema
./scripts/gestion/gestionar_sistema.sh restart   # Reiniciar el sistema
./scripts/gestion/gestionar_sistema.sh status    # Ver estado
./scripts/gestion/gestionar_sistema.sh logs      # Ver logs

# Detención del sistema (alternativas)
python scripts/gestion/detener_sistema.py         # Modo interactivo
python scripts/gestion/detener_sistema.py --force # Sin confirmación
./scripts/gestion/detener_sistema.sh              # Versión Bash
```

### 2. Base de Datos (`database/`)

Scripts para gestionar la base de datos:

```bash
# Crear/inicializar base de datos
PYTHONPATH=. python scripts/database/crear_bd.py

# Limpiar datos de la base de datos
PYTHONPATH=. python scripts/database/limpiar_base_datos.py           # Modo interactivo
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --all     # Eliminar todo
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --test    # Solo reservas TEST*
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --oc      # Solo órdenes de compra
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --stats   # Ver estadísticas
PYTHONPATH=. python scripts/database/limpiar_base_datos.py --list    # Listar reservas

# Cargar clientes desde Excel
PYTHONPATH=. python scripts/database/cargar_clientes_excel.py
```

### 3. Testing y Diagnóstico (`testing/`)

Scripts para pruebas y diagnóstico del sistema:

```bash
# Verificar correos en el inbox
PYTHONPATH=. python scripts/testing/check_inbox.py

# 🆕 Probar fetch de mensajes IMAP (v1.3.1)
PYTHONPATH=. python scripts/testing/test_imap_fetch.py

# Generar PDF de prueba
PYTHONPATH=. python scripts/testing/generar_pdf_prueba.py

# Marcar correos como no leídos (para reprocesar)
PYTHONPATH=. python scripts/testing/marcar_correos_no_leidos.py
PYTHONPATH=. python scripts/testing/marcar_no_leido.py
PYTHONPATH=. python scripts/testing/marcar_oc_no_leido.py

# Verificar configuración de correos
PYTHONPATH=. python scripts/testing/verificar_correos.py

# Verificar reservas en la base de datos
PYTHONPATH=. python scripts/testing/verificar_reservas.py
```

### 4. Utilidades (`utils/`)

Scripts utilitarios generales:

```bash
# Configurar cliente nuevo
PYTHONPATH=. python scripts/utils/configurar_cliente.py

# Enviar correo de prueba
PYTHONPATH=. python scripts/utils/enviar_prueba.py

# Enviar solicitud de OC manualmente
PYTHONPATH=. python scripts/utils/enviar_solicitud_oc.py

# Probar conexión IMAP/SMTP
PYTHONPATH=. python scripts/utils/test_conexion.py

# Verificar configuración de emails
PYTHONPATH=. python scripts/utils/verificar_emails.py
```

---

## 🐍 Uso como Módulos Python

También puedes ejecutar los scripts como módulos de Python:

```bash
# Desde la raíz del proyecto
python -m scripts.database.crear_bd
python -m scripts.gestion.detener_sistema
python -m scripts.testing.check_inbox
```

---

## 📝 Notas Importantes

1. **Entorno Virtual**: Asegúrate de activar el entorno virtual antes de ejecutar cualquier script:
   ```bash
   source venv/bin/activate  # Linux/Mac
   # o
   .\venv\Scripts\activate   # Windows
   ```

2. **Variables de Entorno**: Los scripts requieren que el archivo `.env` esté configurado correctamente.

3. **Permisos**: Los scripts `.sh` requieren permisos de ejecución:
   ```bash
   chmod +x scripts/gestion/*.sh
   ```

4. **Rutas Relativas**: Todos los scripts están diseñados para ejecutarse desde la raíz del proyecto.

---

## 🆘 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'database'`

**Causa**: Falta configurar el PYTHONPATH para que Python encuentre los módulos del proyecto.

**Soluciones**:

1. **Usar PYTHONPATH** (recomendado para ejecuciones manuales):
```bash
cd /ruta/al/proyecto/envia2
PYTHONPATH=. python scripts/database/crear_bd.py
```

2. **Usar el script wrapper** (más fácil):
```bash
cd /ruta/al/proyecto/envia2
./run_script.sh scripts/database/crear_bd.py
```

3. **Crear alias permanente** (agregar a `~/.zshrc` o `~/.bashrc`):
```bash
# Agregar esta línea al archivo
alias pyrun='PYTHONPATH=. python'

# Recargar configuración
source ~/.zshrc  # o source ~/.bashrc

# Ahora puedes usar
pyrun scripts/database/crear_bd.py
```

### Error: `FileNotFoundError: [Errno 2] No such file or directory: 'data/oc_seguimiento.db'`

**Causa**: La carpeta `data/` no existe o no tienes permisos.

**Solución**:
```bash
mkdir -p data
python scripts/database/crear_bd.py
```

### Los scripts Bash no se ejecutan

**Causa**: Falta permiso de ejecución.

**Solución**:
```bash
chmod +x scripts/gestion/*.sh
```

---

## 📚 Más Información

- **Documentación completa**: Ver `docs/`
- **Guía de inicio rápido**: `docs/inicio-rapido/INICIO_RAPIDO.md`
- **Gestión del sistema**: `docs/SCRIPTS_GESTION.md`
- **Troubleshooting**: `docs/troubleshooting/TROUBLESHOOTING.md`

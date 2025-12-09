# Scripts de Gestión del Sistema

Este documento describe los scripts disponibles para gestionar el sistema de seguimiento de OC.

---

## 📋 Scripts Disponibles

### 1. `gestionar_sistema.sh` - Script Principal de Gestión

Script completo para iniciar, detener y monitorear el sistema.

**Comandos:**

```bash
# Iniciar el sistema
./gestionar_sistema.sh start

# Detener el sistema
./gestionar_sistema.sh stop

# Reiniciar el sistema
./gestionar_sistema.sh restart

# Ver estado actual
./gestionar_sistema.sh status

# Ver logs en tiempo real
./gestionar_sistema.sh logs

# Mostrar ayuda
./gestionar_sistema.sh help
```

---

### 2. `detener_sistema.py` - Script de Detención (Python)

Detiene todos los procesos del sistema de forma ordenada.

**Uso:**

```bash
# Modo interactivo (pide confirmación)
python detener_sistema.py

# Modo forzado (sin confirmación)
python detener_sistema.py --force
python detener_sistema.py -f
```

**Características:**
- Busca archivos PID si existen
- Identifica procesos activos relacionados con el sistema
- Detención ordenada con SIGTERM
- Fuerza detención con SIGKILL si es necesario
- Verificación final del estado

---

### 3. `detener_sistema.sh` - Script de Detención (Bash)

Versión Bash del script de detención, más rápida y ligera.

**Uso:**

```bash
# Ejecutar directamente
./detener_sistema.sh
```

**Características:**
- Detiene app.py, email_monitor, scheduler y uvicorn
- Usa SIGTERM primero, luego SIGKILL si es necesario
- Muestra resumen de procesos detenidos
- Verificación final

---

## 🚀 Inicio Rápido

### Iniciar el Sistema

```bash
./gestionar_sistema.sh start
```

El sistema iniciará en segundo plano. Verás:
- PID del proceso principal
- URL del dashboard: http://localhost:8000
- Ubicación de los logs

### Verificar Estado

```bash
./gestionar_sistema.sh status
```

Muestra:
- Si el sistema está activo o detenido
- PIDs de procesos en ejecución
- URL del dashboard si está disponible

### Ver Logs en Tiempo Real

```bash
./gestionar_sistema.sh logs
```

Muestra los logs del sistema en tiempo real. Presiona `Ctrl+C` para salir.

### Detener el Sistema

```bash
# Con confirmación
./gestionar_sistema.sh stop

# Sin confirmación (recomendado para scripts)
python detener_sistema.py --force
```

### Reiniciar el Sistema

```bash
./gestionar_sistema.sh restart
```

Detiene y reinicia el sistema automáticamente.

---

## 📁 Estructura de Archivos

```
envia2/
├── gestionar_sistema.sh      # Script principal de gestión
├── detener_sistema.py         # Script de detención (Python)
├── detener_sistema.sh         # Script de detención (Bash)
├── app.py                     # Aplicación principal
├── logs/
│   └── sistema.log           # Logs del sistema
└── ...
```

---

## 🔧 Solución de Problemas

### El sistema no inicia

1. Verifica que no haya procesos corriendo:
   ```bash
   ./gestionar_sistema.sh status
   ```

2. Revisa los logs:
   ```bash
   tail -n 50 logs/sistema.log
   ```

3. Verifica que el puerto 8000 esté libre:
   ```bash
   lsof -i :8000
   ```

### El sistema no se detiene

1. Usa el modo forzado:
   ```bash
   python detener_sistema.py --force
   ```

2. O detén manualmente los procesos:
   ```bash
   pkill -f "python.*app.py"
   ```

### Ver procesos activos

```bash
ps aux | grep -E "(app\.py|email_monitor|scheduler)" | grep -v grep
```

---

## 💡 Tips

- **Logs automáticos**: El sistema guarda logs en `logs/sistema.log`
- **Puerto por defecto**: 8000 (configurable en `.env`)
- **Modo daemon**: El sistema corre en segundo plano con `nohup`
- **Auto-restart**: No implementado aún (usar `systemd` o `supervisord` para producción)

---

## 📝 Notas

- Los scripts requieren permisos de ejecución (`chmod +x`)
- El sistema debe ejecutarse desde el directorio raíz del proyecto
- Asegúrate de tener activado el entorno virtual correcto
- Los archivos PID se crean automáticamente si se implementa esa funcionalidad

---

## 🆘 Ayuda Adicional

Para más información sobre cualquier script:

```bash
./gestionar_sistema.sh help
python detener_sistema.py  # Sigue las instrucciones interactivas
```

# 📚 Índice de Documentación del Proyecto

**Sistema de Seguimiento de Órdenes de Compra (OC)**

---

## 🎯 Por Dónde Empezar

### Si eres nuevo en el proyecto:
1. 📖 **[README.md](README.md)** - Visión general del proyecto
2. 📂 **[ESTRUCTURA.md](ESTRUCTURA.md)** - Organización del repositorio
3. 🚀 **[docs/inicio-rapido/INICIO_RAPIDO.md](docs/inicio-rapido/INICIO_RAPIDO.md)** - Guía de inicio

### Si estás retomando el trabajo:
1. 🧠 **[CONTEXTO_PROYECTO.md](CONTEXTO_PROYECTO.md)** - Estado completo del proyecto
2. 📝 **[SESION_2025-11-16.md](SESION_2025-11-16.md)** - Último trabajo realizado
3. 🤖 **[.claude/project_context.md](.claude/project_context.md)** - Contexto rápido para IA

---

## 📁 Documentación por Categoría

### 🚀 Inicio Rápido

| Archivo | Descripción | Cuándo Usar |
|---------|-------------|-------------|
| [INICIO_RAPIDO.md](docs/inicio-rapido/INICIO_RAPIDO.md) | Guía rápida de 5 minutos | Primera vez usando el sistema |
| [LEEME_PRIMERO.txt](docs/inicio-rapido/LEEME_PRIMERO.txt) | Instrucciones iniciales | Antes de cualquier cosa |
| [GUIA_PRUEBA_LOCAL.md](docs/inicio-rapido/GUIA_PRUEBA_LOCAL.md) | Cómo probar localmente | Testing en desarrollo |

### 🐛 Resolución de Problemas

| Archivo | Descripción | Cuándo Usar |
|---------|-------------|-------------|
| [TROUBLESHOOTING.md](docs/troubleshooting/TROUBLESHOOTING.md) | Guía general de problemas | Cualquier error |
| [ERRORES_COMUNES.md](docs/troubleshooting/ERRORES_COMUNES.md) | Errores frecuentes | Problemas conocidos |
| [SOLUCION_0_CORREOS.md](docs/troubleshooting/SOLUCION_0_CORREOS.md) | Fix: 0 correos detectados | Email no se detecta |
| [SOLUCION_PYTHON314.txt](docs/troubleshooting/SOLUCION_PYTHON314.txt) | Fix: Python 3.14+ | Problemas de compatibilidad |

### 🏗️ Arquitectura y Estructura

| Archivo | Descripción | Cuándo Usar |
|---------|-------------|-------------|
| [ESTRUCTURA.md](ESTRUCTURA.md) | Organización completa | Navegar el proyecto |
| [CONTEXTO_PROYECTO.md](CONTEXTO_PROYECTO.md) | Estado y decisiones técnicas | Entender el sistema completo |
| [COMPARACION_PYTHON_VS_N8N.md](docs/COMPARACION_PYTHON_VS_N8N.md) | Python vs N8N | Decidir arquitectura |

### 🌐 API y Testing

| Archivo | Descripción | Cuándo Usar |
|---------|-------------|-------------|
| [POSTMAN_SETUP.md](api/postman/POSTMAN_SETUP.md) | Configuración de Postman | Probar API endpoints |
| [TravelIA_OC_API.postman_collection.json](api/postman/TravelIA_OC_API.postman_collection.json) | Colección Postman | Importar en Postman |
| [TravelIA_Development.postman_environment.json](api/postman/TravelIA_Development.postman_environment.json) | Environment Postman | Variables de entorno |

### 🔄 Workflows N8N

| Archivo | Descripción | Cuándo Usar |
|---------|-------------|-------------|
| [n8n/README.md](n8n/README.md) | Documentación N8N | Implementación alternativa |
| [n8n/README_INSTALACION_N8N.md](n8n/README_INSTALACION_N8N.md) | Instalación N8N | Configurar N8N |
| [n8n/workflows/](n8n/workflows/) | JSON de workflows | Importar workflows |

### 📅 Sesiones de Trabajo

| Archivo | Descripción | Cuándo Usar |
|---------|-------------|-------------|
| [SESION_2025-11-16.md](SESION_2025-11-16.md) | Sesión del 16 Nov 2025 | Ver trabajo reciente |
| *(futuras sesiones)* | Logs de trabajo | Historial de cambios |

### 🤖 Contexto para IA

| Archivo | Descripción | Cuándo Usar |
|---------|-------------|-------------|
| [.claude/project_context.md](.claude/project_context.md) | Contexto compacto | Prompt para Claude |

---

## 🗂️ Documentación Técnica (Inline)

### Código Fuente Documentado

| Archivo | Descripción |
|---------|-------------|
| [src/email_monitor.py](src/email_monitor.py) | Monitoreo IMAP - Docstrings completos |
| [src/email_sender.py](src/email_sender.py) | Envío SMTP - Templates Jinja2 |
| [src/imap_wrapper.py](src/imap_wrapper.py) | Cliente IMAP - BODY.PEEK[] crítico |
| [src/pdf_processor.py](src/pdf_processor.py) | Extracción PDF - Regex patterns |
| [src/scheduler.py](src/scheduler.py) | Tareas programadas - APScheduler |
| [config.py](config.py) | Configuración - Pydantic Settings |
| [database.py](database.py) | Modelos DB - SQLAlchemy ORM |
| [app.py](app.py) | API REST - FastAPI endpoints |

---

## 📊 Diagramas y Visualizaciones

### Flujo del Sistema

Ver: [CONTEXTO_PROYECTO.md - Sección "Flujo del Sistema"](CONTEXTO_PROYECTO.md#-flujo-del-sistema)

```
Confirmación → Detección → Extracción PDF → BD → Solicitud OC →
Respuesta OC → Detección → Validación → Cierre
```

### Arquitectura

Ver: [.claude/project_context.md - Sección "System Architecture"](.claude/project_context.md#system-architecture)

```
Gmail IMAP → Monitores → Base de Datos → Scheduler → SMTP
```

---

## 🔍 Buscar Información

### Por Tema

| Tema | Dónde Buscar |
|------|--------------|
| **Instalación** | `docs/inicio-rapido/` |
| **Configuración** | `CONTEXTO_PROYECTO.md` → Configuración Actual |
| **Problemas IMAP** | `docs/troubleshooting/SOLUCION_0_CORREOS.md` |
| **API Endpoints** | `api/postman/POSTMAN_SETUP.md` |
| **Estructura de archivos** | `ESTRUCTURA.md` |
| **Decisiones técnicas** | `CONTEXTO_PROYECTO.md` → Decisiones Técnicas |
| **Testing** | `tests/` + `SESION_2025-11-16.md` |
| **Cambios recientes** | `SESION_2025-11-16.md` |

### Por Pregunta

| Pregunta | Respuesta en |
|----------|--------------|
| ¿Cómo inicio el sistema? | `docs/inicio-rapido/INICIO_RAPIDO.md` |
| ¿Por qué no detecta emails? | `docs/troubleshooting/SOLUCION_0_CORREOS.md` |
| ¿Dónde está el código X? | `ESTRUCTURA.md` |
| ¿Qué cambió recientemente? | `SESION_2025-11-16.md` |
| ¿Cómo funciona el flujo? | `CONTEXTO_PROYECTO.md` |
| ¿Cómo pruebo la API? | `api/postman/POSTMAN_SETUP.md` |
| ¿Qué hace este archivo? | `ESTRUCTURA.md` → Descripción de Componentes |

---

## 📝 Tipos de Documentación

### 📖 Lectura (Entender el Sistema)
- `README.md` - Visión general
- `CONTEXTO_PROYECTO.md` - Estado completo
- `ESTRUCTURA.md` - Organización
- `docs/COMPARACION_PYTHON_VS_N8N.md` - Decisiones de arquitectura

### 🚀 Acción (Usar el Sistema)
- `docs/inicio-rapido/` - Empezar
- `api/postman/POSTMAN_SETUP.md` - Probar API
- `scripts/` - Utilidades listas para usar

### 🐛 Solución (Resolver Problemas)
- `docs/troubleshooting/` - Guías de solución
- `SESION_2025-11-16.md` - Problemas resueltos recientemente

### 🧠 Referencia (Consultar Detalles)
- `.claude/project_context.md` - Referencia rápida
- Docstrings en código fuente
- Comentarios inline en archivos críticos

---

## 🎯 Rutas de Aprendizaje

### 🆕 Usuario Nuevo (30 min)
1. Lee: `README.md` (5 min)
2. Lee: `docs/inicio-rapido/LEEME_PRIMERO.txt` (2 min)
3. Sigue: `docs/inicio-rapido/INICIO_RAPIDO.md` (15 min)
4. Revisa: `ESTRUCTURA.md` (8 min)

### 👨‍💻 Desarrollador (1 hora)
1. Lee: `CONTEXTO_PROYECTO.md` (20 min)
2. Explora: `ESTRUCTURA.md` (10 min)
3. Lee: `SESION_2025-11-16.md` (15 min)
4. Revisa: Código en `src/` (15 min)

### 🔧 Troubleshooter (20 min)
1. Identifica problema
2. Busca en: `docs/troubleshooting/TROUBLESHOOTING.md`
3. Si no aparece: `docs/troubleshooting/ERRORES_COMUNES.md`
4. Última opción: `SESION_2025-11-16.md` (problemas recientes)

### 🧪 Tester/QA (45 min)
1. Lee: `api/postman/POSTMAN_SETUP.md` (10 min)
2. Importa: Colecciones Postman (5 min)
3. Ejecuta: Tests en `tests/` (20 min)
4. Revisa: Resultados vs documentación (10 min)

---

## 💡 Tips para Navegar la Documentación

### ✅ DO
- Empieza por `README.md` si es tu primera vez
- Lee `CONTEXTO_PROYECTO.md` para entender decisiones
- Consulta `ESTRUCTURA.md` cuando busques archivos
- Usa `SESION_*.md` para ver cambios recientes

### ❌ DON'T
- No saltes directo al código sin leer contexto
- No ignores `docs/troubleshooting/` cuando tengas problemas
- No modifiques sin entender la estructura (lee `ESTRUCTURA.md`)

---

## 🔄 Mantener la Documentación

### Al hacer cambios importantes:
1. Actualiza `CONTEXTO_PROYECTO.md` si cambia arquitectura
2. Crea nuevo `SESION_YYYY-MM-DD.md` para sesiones largas
3. Actualiza `ESTRUCTURA.md` si cambias organización
4. Actualiza `.claude/project_context.md` para futuras sesiones

### Cada semana:
1. Revisa que los ejemplos sigan funcionando
2. Actualiza versiones de dependencias si es necesario
3. Agrega problemas resueltos a `docs/troubleshooting/`

---

## 📞 Cuando Necesites Ayuda

1. **Busca primero** en este índice
2. **Lee la documentación** relevante
3. **Revisa logs** en `logs/`
4. **Consulta** `.claude/project_context.md` para usar con IA
5. **Crea issue** con contexto completo

---

**Última actualización**: 2025-11-16

Este índice se actualiza con cada sesión importante de trabajo.

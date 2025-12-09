# Documentación del Sistema de Seguimiento de OC

Bienvenido a la documentación completa del Sistema de Seguimiento de Órdenes de Compra.

---

## 📚 Índice de Documentación

### 🚀 Inicio Rápido

- **[LEEME PRIMERO](inicio-rapido/LEEME_PRIMERO.txt)** - Información esencial antes de comenzar
- **[Inicio Rápido](inicio-rapido/INICIO_RAPIDO.md)** - Guía de instalación y configuración
- **[Guía de Prueba Local](inicio-rapido/GUIA_PRUEBA_LOCAL.md)** - Cómo probar el sistema localmente
- **[Guía de Postman Básica](GUIA_POSTMAN_BASICA.md)** 📮 - Cómo usar Postman para principiantes (v1.3.3)

### 📋 Documentación del Proyecto

- **[Alcance del Proyecto](ALCANCE_PROYECTO.md)** - Objetivos, alcance y limitaciones
- **[Diagramas del Sistema](DIAGRAMAS.md)** - Diagramas de arquitectura y flujo
- **[Flujo Detallado del Sistema](FLUJO_DETALLADO_SISTEMA.md)** ⭐ - Diagramas completos con configuraciones (v1.3.3)
- **[Gestión de Scripts](SCRIPTS_GESTION.md)** - Guía de uso de scripts de gestión
- **[Lista de Implementación](LISTA_IMPLEMENTACION_CLIENTE.md)** - Tareas de implementación para cliente

### 🏗️ Arquitectura

- **[Flujo del Sistema](arquitectura/FLUJO_SISTEMA.md)** - Descripción detallada del flujo de datos
- **[Análisis del Modelo de Datos](arquitectura/ANALISIS_MODELO_DATOS.md)** - Evaluación completa del diseño de base de datos (v1.3.3)
- **[Comparativa de Arquitecturas GCP](arquitectura/COMPARATIVA_ARQUITECTURAS_GCP.md)** - Opciones de despliegue en Google Cloud

### ⚙️ Configuración

- **[Configuración de Gmail](configuracion/CONFIGURACION_GMAIL.md)** - Cómo configurar cuentas de Gmail para IMAP/SMTP
- **[Cambio: Email Contacto por Cliente](CAMBIO_EMAIL_CONTACTO.md)** 📧 - Documentación técnica del sistema de emails (v1.3.3)
- **[Guía de Actualización de Emails](GUIA_ACTUALIZACION_EMAILS.md)** 📧 - Cómo configurar emails de contacto (v1.3.3)

### 👥 Para el Cliente

- **[Resumen para el Cliente](cliente/RESUMEN_PARA_CLIENTE.md)** - Descripción del sistema para usuarios finales
- **[Plan de Pruebas](cliente/PLAN_PRUEBAS_CLIENTE.md)** - Plan de pruebas antes del despliegue
- **[Solicitud de Información](cliente/SOLICITUD_INFO_CLIENTE.md)** - Información requerida del cliente

### 🔧 Git y Control de Versiones

- **[Instrucciones Git](git/INSTRUCCIONES_GIT.md)** - Guía de uso de Git para el proyecto

### 🔍 Troubleshooting

- **[Guía de Troubleshooting](troubleshooting/TROUBLESHOOTING.md)** - Solución de problemas comunes
- **[Errores Comunes](troubleshooting/ERRORES_COMUNES.md)** - Lista de errores frecuentes y soluciones
- **[Solución: 0 Correos Detectados](troubleshooting/SOLUCION_0_CORREOS.md)** - Qué hacer si no se detectan correos
- **[Solución: Python 3.14](troubleshooting/SOLUCION_PYTHON314.txt)** - Problemas con Python 3.14

---

## 📖 Organización de la Documentación

```
docs/
├── README.md                          # Este archivo - Índice principal
├── ALCANCE_PROYECTO.md                # Alcance del proyecto
├── DIAGRAMAS.md                       # Diagramas del sistema
├── FLUJO_DETALLADO_SISTEMA.md         # ⭐ Flujo completo con configuraciones (v1.3.3)
├── GUIA_POSTMAN_BASICA.md             # 📮 Guía de Postman para principiantes (v1.3.3)
├── LISTA_IMPLEMENTACION_CLIENTE.md    # Lista de tareas de implementación
├── SCRIPTS_GESTION.md                 # Documentación de scripts de gestión
├── CAMBIO_EMAIL_CONTACTO.md           # 📧 Documentación técnica emails (v1.3.3)
├── GUIA_ACTUALIZACION_EMAILS.md       # 📧 Guía de actualización emails (v1.3.3)
│
├── arquitectura/                      # Arquitectura del sistema
│   ├── FLUJO_SISTEMA.md
│   ├── ANALISIS_MODELO_DATOS.md       # Análisis del modelo de datos (v1.3.3)
│   └── COMPARATIVA_ARQUITECTURAS_GCP.md
│
├── configuracion/                     # Guías de configuración
│   └── CONFIGURACION_GMAIL.md
│
├── cliente/                           # Documentación para el cliente
│   ├── RESUMEN_PARA_CLIENTE.md
│   ├── PLAN_PRUEBAS_CLIENTE.md
│   └── SOLICITUD_INFO_CLIENTE.md
│
├── inicio-rapido/                     # Guías de inicio rápido
│   ├── LEEME_PRIMERO.txt
│   ├── INICIO_RAPIDO.md
│   └── GUIA_PRUEBA_LOCAL.md
│
├── git/                               # Documentación de Git
│   └── INSTRUCCIONES_GIT.md
│
└── troubleshooting/                   # Solución de problemas
    ├── TROUBLESHOOTING.md
    ├── ERRORES_COMUNES.md
    ├── SOLUCION_0_CORREOS.md
    └── SOLUCION_PYTHON314.txt
```

---

## 🎯 Rutas Rápidas

### Para Desarrolladores

1. **Primera vez con el proyecto**: `inicio-rapido/INICIO_RAPIDO.md`
2. **Entender la arquitectura**: `FLUJO_DETALLADO_SISTEMA.md` ⭐ (v1.3.3)
3. **Entender el modelo de datos**: `arquitectura/ANALISIS_MODELO_DATOS.md`
4. **Configurar emails de clientes**: `GUIA_ACTUALIZACION_EMAILS.md` 📧 (v1.3.3)
5. **Desplegar en producción**: `arquitectura/COMPARATIVA_ARQUITECTURAS_GCP.md`
6. **Problemas**: `troubleshooting/TROUBLESHOOTING.md`

### Para Clientes

1. **¿Qué hace el sistema?**: `cliente/RESUMEN_PARA_CLIENTE.md`
2. **¿Cómo probarlo?**: `cliente/PLAN_PRUEBAS_CLIENTE.md`
3. **Información necesaria**: `cliente/SOLICITUD_INFO_CLIENTE.md`

### Para Administradores

1. **Gestionar el sistema**: `SCRIPTS_GESTION.md`
2. **Configurar Gmail**: `configuracion/CONFIGURACION_GMAIL.md`
3. **Solucionar problemas**: `troubleshooting/`

---

## 📝 Convenciones

- **📋**: Documentación general
- **🚀**: Guías de inicio rápido
- **🏗️**: Arquitectura y diseño
- **⚙️**: Configuración
- **🔧**: Troubleshooting
- **👥**: Documentación para clientes
- **💻**: Documentación técnica

---

## 🔄 Actualizaciones

La documentación se actualiza constantemente. Consulta el `CHANGELOG.md` en la raíz del proyecto para ver los cambios más recientes.

---

## 📞 Soporte

Si tienes preguntas o encuentras problemas:

1. Revisa la sección de **Troubleshooting**
2. Consulta los **Errores Comunes**
3. Revisa el código en `src/` para entender el funcionamiento interno

---

**Última actualización**: 8 de Diciembre de 2024
**Versión del sistema**: 1.2.0

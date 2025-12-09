# Tabla Comparativa de Arquitecturas en Google Cloud Platform (GCP)
## Sistema de Seguimiento de Órdenes de Compra

**Fecha**: Diciembre 2024
**Sistema Actual**: Ejecución manual local
**Objetivo**: Migración a la nube con alta disponibilidad

---

## 📊 Comparativa de Arquitecturas

| Criterio | **Opción 1: VM Compute Engine** | **Opción 2: Cloud Run** | **Opción 3: App Engine** | **Opción 4: GKE Autopilot** |
|----------|--------------------------------|------------------------|-------------------------|----------------------------|
| **🏗️ Arquitectura** | VM Ubuntu + systemd | Contenedor serverless | PaaS managed | Kubernetes managed |
| **💰 Costo Mensual (USD)** | $15-25 | $5-15 | $20-30 | $30-50 |
| **⚡ Startup** | Permanente (24/7) | 0-2 segundos | Siempre activo | Permanente |
| **📈 Escalabilidad** | Manual | Automática (0-1000+) | Automática (1-100) | Automática (pods) |
| **🔧 Mantenimiento** | Alto (OS updates) | Muy bajo | Bajo | Medio |
| **💾 Base de Datos** | SQLite local o Cloud SQL | Cloud SQL obligatorio | Cloud SQL o Firestore | Cloud SQL |
| **🔄 Tareas CRON** | systemd timers | Cloud Scheduler | App Engine Cron | CronJobs nativos |
| **📧 IMAP Monitoring** | ✅ Soportado | ⚠️ Limitado (timeout) | ✅ Soportado | ✅ Soportado |
| **🚀 Complejidad Setup** | Media | Baja | Baja | Alta |
| **⏱️ Tiempo Implementación** | 2-4 horas | 1-2 horas | 2-3 horas | 4-8 horas |
| **🔒 Seguridad** | Responsabilidad compartida | Gestionada por GCP | Gestionada por GCP | Gestionada por GCP |
| **📊 Monitoreo** | Cloud Monitoring manual | Integrado automático | Integrado automático | Integrado automático |
| **🌐 IP Estática** | Opcional ($5/mes) | No necesaria | No necesaria | Opcional |
| **💪 Recomendado Para** | Control total, cargas 24/7 | Apps web, tráfico variable | Apps web tradicionales | Apps complejas, microservicios |

---

## 💵 Desglose de Costos Detallado

### **Opción 1: Compute Engine VM (e2-micro)**

#### Costos Base
| Componente | Especificación | Costo Mensual (USD) |
|------------|----------------|---------------------|
| VM Instance | e2-micro (2 vCPU, 1GB RAM) | $7.11 |
| Disco Persistente | 10 GB SSD | $1.70 |
| Tráfico Salida | ~5 GB/mes | $0.50 |
| Cloud SQL (PostgreSQL) | db-f1-micro (compartida) | $7.67 |
| IP Estática (opcional) | 1 IP | $4.92 |
| **TOTAL SIN IP** | | **$16.98** |
| **TOTAL CON IP** | | **$21.90** |

#### Ventajas
✅ Control total del sistema operativo
✅ Procesos permanentes (ideal para IMAP monitoring)
✅ Sin limitaciones de tiempo de ejecución
✅ Fácil migración desde local

#### Desventajas
❌ Requiere gestión manual de OS
❌ No escala automáticamente
❌ Necesita backups manuales
❌ Mayor responsabilidad de seguridad

---

### **Opción 2: Cloud Run (Serverless)**

#### Costos Base
| Componente | Especificación | Costo Mensual (USD) |
|------------|----------------|---------------------|
| Cloud Run | 512MB RAM, 1 vCPU | $2.50 |
| Cloud Scheduler | 3 jobs (monitores) | $0.30 |
| Cloud SQL | db-f1-micro | $7.67 |
| Secret Manager | 3 secretos activos | $0.18 |
| Tráfico Salida | ~5 GB/mes | $0.50 |
| **TOTAL** | | **$11.15** |

#### Ventajas
✅ Pago por uso real (muy económico)
✅ Escalamiento automático instantáneo
✅ Zero mantenimiento de infraestructura
✅ HTTPS gratuito automático
✅ Deploy simplificado

#### Desventajas
❌ Timeout máximo: 60 minutos
❌ IMAP monitoring requiere Cloud Scheduler externo
❌ Cold start ocasional (2-5 segundos)
❌ Requiere rediseño de monitoreo continuo

---

### **Opción 3: App Engine Flexible**

#### Costos Base
| Componente | Especificación | Costo Mensual (USD) |
|------------|----------------|---------------------|
| App Engine | 1 instancia (1 vCPU, 0.5GB RAM) | $18.25 |
| Cloud SQL | db-f1-micro | $7.67 |
| Tráfico Salida | ~5 GB/mes | $0.50 |
| **TOTAL** | | **$26.42** |

#### Ventajas
✅ PaaS completo, fácil de gestionar
✅ Escalamiento automático
✅ Integración nativa con GCP
✅ Cron jobs nativos (app.yaml)
✅ Zero downtime deployments

#### Desventajas
❌ Más costoso que Cloud Run
❌ Menos flexible que Compute Engine
❌ Tiempo de deploy más lento
❌ Requiere al menos 1 instancia siempre activa

---

### **Opción 4: GKE Autopilot**

#### Costos Base
| Componente | Especificación | Costo Mensual (USD) |
|------------|----------------|---------------------|
| GKE Autopilot | Cluster management | $73.00 |
| Pods (2 replicas) | 1 vCPU, 1GB RAM c/u | $35.04 |
| Cloud SQL | db-g1-small | $25.55 |
| Load Balancer | HTTP(S) | $18.00 |
| Tráfico Salida | ~10 GB/mes | $1.00 |
| **TOTAL** | | **$152.59** |

#### Ventajas
✅ Alta disponibilidad nativa
✅ Multi-zona automática
✅ Escalamiento horizontal sofisticado
✅ Ideal para arquitecturas complejas
✅ CI/CD robusto

#### Desventajas
❌ Muy costoso para este caso de uso
❌ Complejidad innecesaria
❌ Requiere expertise en Kubernetes
❌ Overhead de gestión alto

---

## 🎯 Arquitectura Recomendada por Escenario

### **Escenario 1: Startup / MVP (0-50 reservas/mes)**
**Recomendación: Cloud Run + Cloud SQL**

```
┌─────────────────────────────────────────┐
│         Cloud Run Container             │
│  ┌──────────────┐  ┌─────────────┐     │
│  │  FastAPI App │  │  Scheduler  │     │
│  └──────────────┘  └─────────────┘     │
└─────────────┬───────────────────────────┘
              │
              ▼
    ┌─────────────────┐
    │   Cloud SQL     │
    │  (PostgreSQL)   │
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Cloud Scheduler │
    │ (IMAP Monitor)  │
    └─────────────────┘
```

**Costo Total**: ~$11/mes
**Tiempo Setup**: 1-2 horas
**Complejidad**: Baja

---

### **Escenario 2: Crecimiento (50-200 reservas/mes)**
**Recomendación: Compute Engine + Cloud SQL**

```
┌──────────────────────────────────────────┐
│    Compute Engine (e2-small)             │
│  ┌──────────────┐  ┌──────────────┐     │
│  │  FastAPI     │  │  IMAP        │     │
│  │  (Uvicorn)   │  │  Monitors    │     │
│  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐                        │
│  │  APScheduler │  (systemd)             │
│  └──────────────┘                        │
└─────────────┬────────────────────────────┘
              │
              ▼
    ┌─────────────────┐
    │   Cloud SQL     │
    │  (PostgreSQL)   │
    │   db-f1-micro   │
    └─────────────────┘
```

**Costo Total**: ~$22/mes
**Tiempo Setup**: 2-4 horas
**Complejidad**: Media

---

### **Escenario 3: Producción Estable (200-1000 reservas/mes)**
**Recomendación: App Engine Flexible + Cloud SQL**

```
┌──────────────────────────────────────────┐
│      App Engine Flexible                 │
│  ┌──────────────────────────────┐        │
│  │     FastAPI Application      │        │
│  └──────────────────────────────┘        │
│  ┌──────────────────────────────┐        │
│  │    Background Workers        │        │
│  │    (IMAP + Scheduler)        │        │
│  └──────────────────────────────┘        │
└─────────────┬────────────────────────────┘
              │
              ▼
    ┌─────────────────┐
    │   Cloud SQL     │
    │  (PostgreSQL)   │
    │   db-g1-small   │
    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Cloud Scheduler │
    │  (Backup Jobs)  │
    └─────────────────┘
```

**Costo Total**: ~$52/mes
**Tiempo Setup**: 2-3 horas
**Complejidad**: Media

---

## 🏆 Recomendación Final

### **Para Tu Caso Actual: Compute Engine e2-micro + Cloud SQL**

#### ¿Por qué?

1. **IMAP Monitoring 24/7**: El sistema requiere conexiones IMAP persistentes que Cloud Run no puede mantener
2. **APScheduler**: Ya tienes tareas programadas que funcionan perfectamente con systemd
3. **Migración Simple**: Código actual funciona sin cambios significativos
4. **Costo Predecible**: ~$22/mes fijo, sin sorpresas
5. **Control Total**: Puedes ajustar cualquier configuración sin limitaciones

#### Arquitectura Propuesta

```
┌────────────────────────────────────────────────────────┐
│         Compute Engine VM (e2-micro)                   │
│  Ubuntu 22.04 LTS                                      │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  Aplicación (puerto 8001)                    │    │
│  │  • FastAPI + Uvicorn                         │    │
│  │  • IMAP Monitors (background threads)        │    │
│  │  • APScheduler                               │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  Nginx (puerto 80/443)                       │    │
│  │  • Reverse proxy                             │    │
│  │  • SSL/TLS termination (Let's Encrypt)       │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │  Systemd                                     │    │
│  │  • Auto-restart en crash                     │    │
│  │  • Logs centralizados                        │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
└─────────────┬──────────────────────────────────────────┘
              │
              │ Private IP
              ▼
    ┌─────────────────────┐
    │   Cloud SQL         │
    │   PostgreSQL 14     │
    │   db-f1-micro       │
    │   • 0.6GB RAM       │
    │   • Shared vCPU     │
    │   • 10GB Storage    │
    │   • Backups diarios │
    └─────────────────────┘
              │
              ▼
    ┌─────────────────────┐
    │  Cloud Storage      │
    │  (Backups PDFs)     │
    │  ~1GB/mes           │
    │  $0.02/mes          │
    └─────────────────────┘
```

---

## 📋 Plan de Migración Recomendado

### **Fase 1: Preparación (30 minutos)**
1. ✅ Crear proyecto GCP
2. ✅ Habilitar APIs necesarias (Compute Engine, Cloud SQL, Cloud Storage)
3. ✅ Configurar facturación y alertas de costos

### **Fase 2: Base de Datos (1 hora)**
1. ✅ Crear instancia Cloud SQL PostgreSQL (db-f1-micro)
2. ✅ Migrar schema desde SQLite a PostgreSQL
3. ✅ Configurar backups automáticos
4. ✅ Migrar datos existentes

### **Fase 3: Compute Engine (1.5 horas)**
1. ✅ Crear VM e2-micro en región us-central1
2. ✅ Instalar dependencias (Python 3.11, PostgreSQL client)
3. ✅ Clonar repositorio del proyecto
4. ✅ Configurar variables de entorno
5. ✅ Configurar systemd service

### **Fase 4: Configuración Final (1 hora)**
1. ✅ Instalar y configurar Nginx
2. ✅ Configurar SSL con Let's Encrypt
3. ✅ Configurar firewall rules
4. ✅ Configurar Cloud Monitoring

### **Fase 5: Testing (30 minutos)**
1. ✅ Probar monitoreo IMAP
2. ✅ Probar envío de correos
3. ✅ Probar dashboard web
4. ✅ Validar logs y métricas

**Tiempo Total**: 4-5 horas
**Costo Estimado**: $22/mes

---

## 💡 Optimizaciones de Costos

### **Reducir Costos en ~30%**

1. **Usar Free Tier**: GCP ofrece f1-micro gratuito permanente en us-west1, us-central1, us-east1
   - **Ahorro**: $7/mes
   - **Limitación**: Solo 0.6GB RAM (suficiente para tu app)

2. **Committed Use Discount**: Compromiso de 1 año
   - **Ahorro**: 25% adicional
   - **Costo final**: ~$12/mes

3. **Cloud SQL Shared Core**: Ya incluido en la recomendación
   - **Costo**: $7.67/mes vs $51/mes (dedicated)

4. **Preemptible VM** (No recomendado para tu caso)
   - **Ahorro**: 60-91%
   - **Problema**: Se apaga cada 24h (inaceptable para IMAP)

### **Costos Finales Optimizados**

| Componente | Costo Original | Costo Optimizado |
|------------|----------------|------------------|
| VM e2-micro | $7.11 | **$0.00** (Free Tier) |
| Disco 10GB SSD | $1.70 | $1.70 |
| Cloud SQL | $7.67 | $7.67 |
| Tráfico | $0.50 | $0.50 |
| IP Estática | $4.92 | $0.00 (opcional) |
| **TOTAL** | **$21.90** | **$9.87/mes** |

---

## 🚨 Consideraciones Importantes

### **Migración de SQLite a PostgreSQL**
```python
# Cambio mínimo en database.py
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:pass@/dbname?host=/cloudsql/project:region:instance"
)
```

### **Variables de Entorno en GCP**
```bash
# En la VM, crear /etc/systemd/system/oc-seguimiento.env
IMAP_HOST=imap.gmail.com
IMAP_USERNAME=seguimiento-oc@ideasfractal.com
IMAP_PASSWORD=xxx
DATABASE_URL=postgresql://...
ENVIRONMENT=production
```

### **Monitoreo Proactivo**
```yaml
# Alertas recomendadas en Cloud Monitoring
- CPU > 80% por 5 minutos
- RAM > 90% por 5 minutos
- Disco > 85%
- Servicio HTTP no responde (uptime check)
```

---

## 📊 Comparativa de Costos Anuales

| Arquitectura | Costo Mensual | Costo Anual | Ahorro vs Manual |
|--------------|---------------|-------------|------------------|
| **Manual (Local)** | $0 (+ electricidad ~$5) | ~$60 | - |
| **Cloud Run** | $11 | $132 | Confiabilidad 99.95% |
| **Compute Engine (Free Tier)** | $10 | $120 | Alta disponibilidad |
| **Compute Engine (Paid)** | $22 | $264 | IP estática + control |
| **App Engine** | $26 | $312 | PaaS completo |
| **GKE** | $153 | $1,836 | ❌ Overkill |

---

## ✅ Checklist de Decisión

Usa esta tabla para decidir:

| Criterio | Cloud Run | Compute Engine | App Engine |
|----------|-----------|----------------|------------|
| Presupuesto < $15/mes | ✅ | ⚠️ | ❌ |
| IMAP 24/7 requerido | ❌ | ✅ | ✅ |
| Escalamiento automático crítico | ✅ | ❌ | ✅ |
| Mantenimiento mínimo | ✅ | ❌ | ✅ |
| Control total del OS | ❌ | ✅ | ❌ |
| Deploy en < 10 min | ✅ | ⚠️ | ⚠️ |
| Código sin cambios | ⚠️ | ✅ | ⚠️ |

**Resultado**: **Compute Engine e2-micro** es la mejor opción para tu caso.

---

## 📞 Próximos Pasos

1. **Crear cuenta GCP** (incluye $300 en créditos gratis por 90 días)
2. **Validar free tier** en tu región
3. **Ejecutar script de migración** (te lo puedo preparar)
4. **Monitorear costos** primeros 30 días

¿Quieres que prepare los scripts de deployment automático para GCP?

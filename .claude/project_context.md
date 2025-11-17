# Project Context for Claude Code

**Project**: Sistema de Seguimiento de Órdenes de Compra (OC) para Reservas Hoteleras
**Last Updated**: 2025-11-16
**Status**: ✅ Functional in Development

---

## Quick Start Prompt

> "Estoy trabajando en un sistema de seguimiento de órdenes de compra para reservas hoteleras. El sistema monitorea un buzón Gmail via IMAP para detectar confirmaciones de reserva y órdenes de compra (OC). Cuando detecta una confirmación, crea una reserva en la base de datos. Luego envía automáticamente correos solicitando la OC al cliente. Cuando el cliente responde con la OC, el sistema la detecta y cierra el ciclo.
>
> **Problema resuelto recientemente**: Los emails se marcaban como leídos antes de ser procesados. Solucionado cambiando de RFC822 a BODY.PEEK[] en el fetch IMAP.
>
> **Estructura actual**: Código organizado en src/, tests en tests/, scripts en scripts/, docs en docs/, datos en data/.
>
> Lee los archivos CONTEXTO_PROYECTO.md y ESTRUCTURA.md para más detalles."

---

## System Architecture

```
┌─────────────────┐
│  Gmail IMAP     │ ← cuchohbk@gmail.com
│  (inbox)        │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│ Reserva │ │    OC    │
│ Monitor │ │ Monitor  │
└────┬────┘ └────┬─────┘
     │           │
     ▼           ▼
┌──────────────────────┐
│  SQLite Database     │
│  data/oc_seguim.db   │
└──────────────────────┘
          │
          ▼
    ┌──────────┐
    │Scheduler │
    └────┬─────┘
         │
         ▼
    ┌─────────┐
    │  SMTP   │ → Envía solicitudes OC
    └─────────┘
```

---

## Critical Files

| File | Purpose | Key Info |
|------|---------|----------|
| `app.py` | FastAPI main app | Port 8001, endpoints REST |
| `config.py` | Settings | Loads from .env |
| `database.py` | SQLAlchemy models | Reserva, OrdenCompra, etc |
| `src/email_monitor.py` | IMAP monitoring | ReservaMonitor, OCMonitor |
| `src/email_sender.py` | SMTP sending | Templates in templates/ |
| `src/imap_wrapper.py` | IMAP client | **Uses BODY.PEEK[]** |
| `src/pdf_processor.py` | PDF extraction | Extracts reserva data |
| `src/scheduler.py` | Background tasks | Reminders, cleanup |

---

## Known Issues & Solutions

### ✅ SOLVED: Emails marked as read before processing
- **Symptom**: OCMonitor can't find emails ReservaMonitor already saw
- **Cause**: RFC822 marks as read automatically
- **Fix**: Use BODY.PEEK[] in `imap_wrapper.py:165`

### ✅ SOLVED: Both monitors process all emails
- **Symptom**: OC emails processed as confirmations
- **Cause**: No filtering by subject
- **Fix**: Subject filters in both monitors (lines 191-195, 342-345)

### ⚠️ KNOWN: Test requires interactive input
- **Issue**: `test_flujo_completo.py` expects user input
- **Workaround**: Run with redirected stdin or skip interactive parts

---

## Environment Variables (.env)

```bash
# IMAP (monitoring confirmations & OC)
IMAP_HOST=imap.gmail.com
IMAP_USERNAME=cuchohbk@gmail.com
IMAP_PASSWORD=<app password>

# SMTP (sending OC requests)
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=cuchohbk@gmail.com
SMTP_PASSWORD=<app password>

# Database
DATABASE_URL=sqlite:///./data/oc_seguimiento.db

# Agencies requiring OC
AGENCIES_REQUIRING_OC=WALVIS S.A.,EMPRESA CORPORATIVA LTDA
```

---

## Email Subject Filters

### Confirmation Emails (ReservaMonitor)
Must contain: `confirmación` OR `confirmacion` OR `confirmation`

### OC Emails (OCMonitor)
Must contain: `orden de compra` OR `oc` OR `purchase order` OR `orden compra`

---

## Common Commands

```bash
# Start server
python3 app.py

# Send test email
cd scripts && python3 enviar_prueba.py

# Check inbox
python3 scripts/verificar_emails.py

# Run tests
cd tests && python3 test_pdf.py

# View logs
tail -f logs/oc_seguimiento_*.log

# API health check
curl http://localhost:8001/api/health
```

---

## Project Structure

```
envia2/
├── src/                 # Source code
├── tests/               # Testing
├── scripts/             # Utilities
├── docs/                # Documentation
├── api/postman/         # API collections
├── data/                # Database & files
├── templates/           # Email templates
├── static/              # Web assets
├── logs/                # Log files (auto-generated)
├── app.py               # Main FastAPI app
├── config.py            # Settings
└── database.py          # DB models
```

---

## Debugging Tips

### Email not detected?
1. Check if email is marked as read: `python3 scripts/verificar_emails.py`
2. Check subject contains keywords
3. Check logs: `grep "Encontrados.*correos" logs/*.log`

### OC not associating with reserva?
1. Verify reserva exists: `curl localhost:8001/api/reservas`
2. Check PDF contains ID & agency
3. Check reserva is in "pendiente" state

### Database issues?
1. Backup: `cp data/oc_seguimiento.db data/backup_$(date +%Y%m%d).db`
2. Check: `sqlite3 data/oc_seguimiento.db ".tables"`
3. Reset: Delete DB, restart app (recreates)

---

## Recent Changes (2025-11-16)

1. **IMAP Fix**: Changed to BODY.PEEK[] to prevent auto-read
2. **Subject Filters**: Added keyword filtering in monitors
3. **Reorganization**: Moved code to src/, tests to tests/, etc.
4. **Documentation**: Created comprehensive context files
5. **Postman**: Added API collection with 9 endpoints

---

## Key Dependencies

```
fastapi>=0.104.1
uvicorn>=0.24.0
sqlalchemy>=2.0.23
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
loguru>=0.7.2
apscheduler>=3.10.4
pdfplumber>=0.10.3
PyPDF2>=3.0.1
jinja2>=3.1.2
```

---

## Next Steps

1. [ ] Complete E2E test with server running
2. [ ] Test with real hotel emails
3. [ ] Verify automatic reminders work
4. [ ] Add authentication to dashboard
5. [ ] Deploy to GCP

---

## Contact & Configuration

- **Gmail Account**: cuchohbk@gmail.com
- **API Port**: 8001
- **Database**: SQLite (can migrate to PostgreSQL)
- **Timezone**: Chile (GMT-3)

---

## For AI Assistants

When helping with this project:
1. Always check `CONTEXTO_PROYECTO.md` first for full context
2. Respect the new structure (don't move files back to root)
3. Use imports from `src.module` not just `module`
4. Remember BODY.PEEK[] is critical for IMAP
5. Subject filters are case-insensitive
6. PDF location is `data/resumen del servicio.pdf`

---

**End of Project Context**

This file provides quick context for resuming work.
For detailed information, see:
- `CONTEXTO_PROYECTO.md` - Full system context
- `ESTRUCTURA.md` - Repository organization
- `SESION_2025-11-16.md` - Latest work session details

"""
Sistema de Seguimiento de Órdenes de Compra (OC) para Reservas Hoteleras
Aplicación principal FastAPI con interfaz web de administración
"""
import asyncio
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, Request, Depends, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from loguru import logger
import sys

from config import settings, validate_config
from database import (
    init_db,
    get_db,
    Reserva,
    CorreoEnviado,
    OrdenCompra,
    ConfiguracionCliente,
    EstadoOC,
    TipoCorreo,
    crear_cliente_inicial
)
from src.email_monitor import ReservaMonitor, OCMonitor
from src.scheduler import oc_scheduler
from src.email_sender import email_sender

# Configurar logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
    level=settings.log_level
)
logger.add(
    "logs/oc_seguimiento_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} | {message}"
)

# Crear FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema automatizado de seguimiento de órdenes de compra para reservas hoteleras"
)

# Configurar archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Variables globales para monitores
reserva_monitor: Optional[ReservaMonitor] = None
oc_monitor: Optional[OCMonitor] = None


# ==================== EVENTOS DE INICIO/CIERRE ====================

@app.on_event("startup")
async def startup_event():
    """Inicializa el sistema al arrancar"""
    global reserva_monitor, oc_monitor

    logger.info("🚀 Iniciando Sistema de Seguimiento de OC...")

    try:
        # Validar configuración
        validate_config()
        logger.info("✅ Configuración validada")

        # Inicializar base de datos
        init_db()
        logger.info("✅ Base de datos inicializada")

        # Crear clientes iniciales
        db = next(get_db())
        crear_cliente_inicial(db)
        logger.info("✅ Clientes configurados")

        # Iniciar scheduler
        oc_scheduler.start()
        logger.info("✅ Scheduler iniciado")

        # Iniciar monitores de correo
        reserva_monitor = ReservaMonitor()
        oc_monitor = OCMonitor()

        # Iniciar loops de monitoreo en background
        asyncio.create_task(reserva_monitor.monitor_loop())
        asyncio.create_task(oc_monitor.monitor_loop())
        logger.info("✅ Monitores de correo iniciados")

        logger.info(f"🎉 Sistema iniciado correctamente en {settings.environment} mode")

    except Exception as e:
        logger.error(f"❌ Error al iniciar sistema: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Limpieza al cerrar el sistema"""
    logger.info("⏹️ Deteniendo Sistema de Seguimiento de OC...")

    try:
        oc_scheduler.shutdown()
        logger.info("✅ Scheduler detenido")

        if reserva_monitor:
            reserva_monitor.disconnect()
        if oc_monitor:
            oc_monitor.disconnect()
        logger.info("✅ Monitores desconectados")

    except Exception as e:
        logger.error(f"Error al cerrar sistema: {e}")


# ==================== RUTAS DE LA INTERFAZ WEB ====================

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Dashboard principal"""
    # Obtener estadísticas
    stats = oc_scheduler.get_stats()

    # Obtener reservas recientes pendientes
    reservas_pendientes = db.query(Reserva).filter_by(
        estado_oc=EstadoOC.PENDIENTE,
        requiere_oc=True
    ).order_by(Reserva.fecha_creacion.desc()).limit(10).all()

    # Obtener OC recibidas recientemente
    oc_recientes = db.query(OrdenCompra).order_by(
        OrdenCompra.fecha_creacion.desc()
    ).limit(5).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": stats,
        "reservas_pendientes": reservas_pendientes,
        "oc_recientes": oc_recientes,
        "settings": settings
    })


@app.get("/reservas", response_class=HTMLResponse)
async def ver_reservas(request: Request, db: Session = Depends(get_db)):
    """Vista HTML de todas las reservas"""
    # Obtener todas las reservas
    reservas = db.query(Reserva).order_by(Reserva.fecha_creacion.desc()).all()

    return templates.TemplateResponse("reservas.html", {
        "request": request,
        "reservas": reservas,
        "settings": settings
    })


@app.get("/clientes", response_class=HTMLResponse)
async def ver_clientes(request: Request, db: Session = Depends(get_db)):
    """Vista HTML de todos los clientes"""
    # Obtener todos los clientes
    clientes = db.query(ConfiguracionCliente).order_by(
        ConfiguracionCliente.nombre_agencia
    ).all()

    # Estadísticas
    total_clientes = len(clientes)
    clientes_con_oc = sum(1 for c in clientes if c.requiere_oc)
    clientes_sin_oc = total_clientes - clientes_con_oc
    clientes_activos = sum(1 for c in clientes if c.activo)

    return templates.TemplateResponse("clientes.html", {
        "request": request,
        "clientes": clientes,
        "total_clientes": total_clientes,
        "clientes_con_oc": clientes_con_oc,
        "clientes_sin_oc": clientes_sin_oc,
        "clientes_activos": clientes_activos,
        "settings": settings
    })


# ==================== API REST ====================

@app.get("/api/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/stats")
async def get_stats():
    """Obtiene estadísticas del sistema"""
    return oc_scheduler.get_stats()


@app.get("/api/reservas")
async def list_reservas(
    estado: Optional[str] = None,
    agencia: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista reservas con filtros opcionales"""
    query = db.query(Reserva).filter_by(requiere_oc=True)

    if estado:
        try:
            estado_enum = EstadoOC[estado.upper()]
            query = query.filter_by(estado_oc=estado_enum)
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Estado inválido: {estado}")

    if agencia:
        query = query.filter(Reserva.agencia.like(f"%{agencia}%"))

    reservas = query.order_by(Reserva.fecha_creacion.desc()).offset(skip).limit(limit).all()

    return {
        "total": query.count(),
        "skip": skip,
        "limit": limit,
        "reservas": [
            {
                "id": r.id,
                "id_reserva": r.id_reserva,
                "loc_interno": r.loc_interno,
                "agencia": r.agencia,
                "nombre_hotel": r.nombre_hotel,
                "fecha_checkin": r.fecha_checkin.isoformat() if r.fecha_checkin else None,
                "fecha_checkout": r.fecha_checkout.isoformat() if r.fecha_checkout else None,
                "monto_total": r.monto_total,
                "moneda": r.moneda,
                "estado_oc": r.estado_oc.value,
                "dias_desde_creacion": r.dias_desde_creacion,
                "fecha_creacion": r.fecha_creacion.isoformat()
            }
            for r in reservas
        ]
    }


@app.get("/api/reservas/{reserva_id}")
async def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Obtiene detalles de una reserva específica"""
    reserva = db.query(Reserva).filter_by(id=reserva_id).first()

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    return {
        "id": reserva.id,
        "id_reserva": reserva.id_reserva,
        "loc_interno": reserva.loc_interno,
        "localizador": reserva.localizador,
        "agencia": reserva.agencia,
        "nombre_hotel": reserva.nombre_hotel,
        "direccion_hotel": reserva.direccion_hotel,
        "fecha_checkin": reserva.fecha_checkin.isoformat() if reserva.fecha_checkin else None,
        "fecha_checkout": reserva.fecha_checkout.isoformat() if reserva.fecha_checkout else None,
        "monto_total": reserva.monto_total,
        "moneda": reserva.moneda,
        "estado_oc": reserva.estado_oc.value,
        "dias_desde_creacion": reserva.dias_desde_creacion,
        "fecha_creacion": reserva.fecha_creacion.isoformat(),
        "correos_enviados": [
            {
                "tipo": c.tipo_correo.value,
                "estado": c.estado.value,
                "fecha_enviado": c.fecha_enviado.isoformat() if c.fecha_enviado else None,
                "destinatario": c.destinatario
            }
            for c in reserva.correos_enviados
        ],
        "orden_compra": {
            "recibida": reserva.orden_compra is not None,
            "fecha_recepcion": reserva.orden_compra.fecha_creacion.isoformat() if reserva.orden_compra else None,
            "numero_oc": reserva.orden_compra.numero_oc if reserva.orden_compra else None
        } if reserva.orden_compra else None
    }


@app.post("/api/reservas/{reserva_id}/marcar-oc-recibida")
async def marcar_oc_recibida(
    reserva_id: int,
    numero_oc: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Marca manualmente una OC como recibida"""
    reserva = db.query(Reserva).filter_by(id=reserva_id).first()

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    if reserva.estado_oc == EstadoOC.RECIBIDA:
        return {"message": "La OC ya estaba marcada como recibida"}

    # Crear registro de OC manual
    oc = OrdenCompra(
        reserva_id=reserva.id,
        email_remitente="manual",
        email_fecha=datetime.utcnow(),
        numero_oc=numero_oc,
        validada=True,
        fecha_validacion=datetime.utcnow(),
        validada_por="admin",
        observaciones="Marcada manualmente desde interfaz admin"
    )

    db.add(oc)
    reserva.estado_oc = EstadoOC.RECIBIDA
    db.commit()

    logger.info(f"✅ OC marcada manualmente como recibida: Reserva {reserva.id_reserva}")

    return {"message": "OC marcada como recibida exitosamente"}


@app.post("/api/reservas/{reserva_id}/reenviar-correo")
async def reenviar_correo(
    reserva_id: int,
    tipo_correo: str,
    db: Session = Depends(get_db)
):
    """Reenvía manualmente un correo a una reserva"""
    reserva = db.query(Reserva).filter_by(id=reserva_id).first()

    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    # Obtener email de contacto del cliente
    config_cliente = db.query(ConfiguracionCliente).filter_by(
        nombre_agencia=reserva.agencia
    ).first()

    if not config_cliente or not config_cliente.email_contacto:
        raise HTTPException(
            status_code=400,
            detail="Cliente no tiene email de contacto configurado"
        )

    # Enviar correo según el tipo
    try:
        if tipo_correo == "solicitud_inicial":
            success = email_sender.send_solicitud_inicial(reserva, db, config_cliente.email_contacto)
        elif tipo_correo == "recordatorio_dia2":
            success = email_sender.send_recordatorio_dia2(reserva, db, config_cliente.email_contacto)
        elif tipo_correo == "ultimatum_dia4":
            success = email_sender.send_ultimatum_dia4(reserva, db, config_cliente.email_contacto)
        else:
            raise HTTPException(status_code=400, detail="Tipo de correo inválido")

        if success:
            return {"message": "Correo reenviado exitosamente"}
        else:
            raise HTTPException(status_code=500, detail="Error al enviar correo")

    except Exception as e:
        logger.error(f"Error reenviando correo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/clientes")
async def list_clientes(db: Session = Depends(get_db)):
    """Lista clientes configurados"""
    clientes = db.query(ConfiguracionCliente).all()

    return {
        "total": len(clientes),
        "clientes": [
            {
                "id": c.id,
                "nombre_agencia": c.nombre_agencia,
                "email_contacto": c.email_contacto,
                "requiere_oc": c.requiere_oc,
                "activo": c.activo,
                "dias_recordatorio_1": c.dias_recordatorio_1,
                "dias_recordatorio_2": c.dias_recordatorio_2
            }
            for c in clientes
        ]
    }


@app.post("/api/clientes")
async def create_cliente(
    nombre_agencia: str,
    email_contacto: str,
    requiere_oc: bool = True,
    db: Session = Depends(get_db)
):
    """Crea o actualiza configuración de cliente"""
    cliente = db.query(ConfiguracionCliente).filter_by(
        nombre_agencia=nombre_agencia
    ).first()

    if cliente:
        cliente.email_contacto = email_contacto
        cliente.requiere_oc = requiere_oc
        cliente.activo = True
    else:
        cliente = ConfiguracionCliente(
            nombre_agencia=nombre_agencia,
            email_contacto=email_contacto,
            requiere_oc=requiere_oc,
            activo=True
        )
        db.add(cliente)

    db.commit()

    return {"message": "Cliente configurado exitosamente"}


@app.post("/api/process-now")
async def process_now():
    """Fuerza procesamiento inmediato de correos pendientes"""
    await oc_scheduler.process_pending_emails()
    return {"message": "Procesamiento ejecutado"}


# ==================== PUNTO DE ENTRADA ====================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.web_host,
        port=settings.web_port,
        reload=settings.web_reload,
        log_level=settings.log_level.lower()
    )

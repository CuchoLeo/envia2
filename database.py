"""
Modelos de base de datos para el sistema de seguimiento de OC
SQLAlchemy ORM con SQLite
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    Text,
    ForeignKey,
    Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.pool import StaticPool
import enum

from config import settings

# Base para modelos
Base = declarative_base()


# Enums
class EstadoOC(enum.Enum):
    """Estados posibles de una orden de compra"""
    NO_REQUIERE_OC = "no_requiere_oc"
    PENDIENTE = "pendiente"
    RECIBIDA = "recibida"
    CANCELADA = "cancelada"
    EXPIRADA = "expirada"


class TipoCorreo(enum.Enum):
    """Tipos de correo enviados"""
    SOLICITUD_INICIAL = "solicitud_inicial"
    RECORDATORIO_DIA_2 = "recordatorio_dia_2"
    ULTIMATUM_DIA_4 = "ultimatum_dia_4"


class EstadoEnvio(enum.Enum):
    """Estados de envío de correos"""
    PENDIENTE = "pendiente"
    ENVIADO = "enviado"
    ERROR = "error"
    CANCELADO = "cancelado"


# Modelos
class Reserva(Base):
    """Modelo de reserva hotelera extraída del PDF"""
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Datos principales de la reserva
    id_reserva = Column(String(50), unique=True, nullable=False, index=True)
    loc_interno = Column(String(50), nullable=False, index=True)
    localizador = Column(String(50), nullable=True)
    agencia = Column(String(200), nullable=False, index=True)

    # Datos del hotel
    nombre_hotel = Column(String(300), nullable=True)
    direccion_hotel = Column(Text, nullable=True)
    telefono_hotel = Column(String(50), nullable=True)

    # Fechas y estadía
    fecha_checkin = Column(DateTime, nullable=True)
    fecha_checkout = Column(DateTime, nullable=True)
    hora_llegada = Column(String(20), nullable=True)
    hora_salida = Column(String(20), nullable=True)
    numero_noches = Column(Integer, nullable=True)
    numero_habitaciones = Column(Integer, nullable=True)

    # Información financiera
    monto_total = Column(Float, nullable=False)
    moneda = Column(String(10), default="CLP")

    # Detalles de habitaciones (JSON serializado)
    detalles_habitaciones = Column(Text, nullable=True)

    # Límite de cancelación
    fecha_limite_cancelacion = Column(DateTime, nullable=True)

    # Observaciones
    observaciones_hotel = Column(Text, nullable=True)
    notas_asesor = Column(Text, nullable=True)

    # Estado de OC
    estado_oc = Column(SQLEnum(EstadoOC), default=EstadoOC.PENDIENTE, nullable=False)
    requiere_oc = Column(Boolean, default=False, nullable=False)

    # Metadatos
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_emision = Column(String(50), nullable=True)

    # Datos del correo original
    email_origen_id = Column(String(200), nullable=True)
    email_origen_fecha = Column(DateTime, nullable=True)
    pdf_filename = Column(String(500), nullable=True)

    # Relaciones
    correos_enviados = relationship("CorreoEnviado", back_populates="reserva", cascade="all, delete-orphan")
    orden_compra = relationship("OrdenCompra", back_populates="reserva", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Reserva {self.id_reserva} - {self.agencia} - {self.estado_oc.value}>"

    @property
    def dias_desde_creacion(self) -> int:
        """
        Calcula días desde que LLEGÓ el correo de confirmación (no desde la creación en BD)
        Esta es la fecha correcta para el flujo de seguimiento de OC:
        - Día 0: Llega el correo de confirmación
        - Día 2: Primer recordatorio
        - Día 4: Ultimátum
        """
        # Usar la fecha del correo original como referencia (día 0 del flujo)
        fecha_referencia = self.email_origen_fecha or self.fecha_creacion
        return (datetime.utcnow() - fecha_referencia).days

    @property
    def necesita_solicitud_inicial(self) -> bool:
        """Verifica si necesita envío de solicitud inicial"""
        return (
            self.requiere_oc
            and self.estado_oc == EstadoOC.PENDIENTE
            and not any(c.tipo_correo == TipoCorreo.SOLICITUD_INICIAL for c in self.correos_enviados)
        )

    @property
    def necesita_recordatorio_dia2(self) -> bool:
        """Verifica si necesita recordatorio día 2"""
        return (
            self.requiere_oc
            and self.estado_oc == EstadoOC.PENDIENTE
            and self.dias_desde_creacion >= 2
            and not any(c.tipo_correo == TipoCorreo.RECORDATORIO_DIA_2 for c in self.correos_enviados)
        )

    @property
    def necesita_ultimatum_dia4(self) -> bool:
        """Verifica si necesita ultimátum día 4"""
        return (
            self.requiere_oc
            and self.estado_oc == EstadoOC.PENDIENTE
            and self.dias_desde_creacion >= 4
            and not any(c.tipo_correo == TipoCorreo.ULTIMATUM_DIA_4 for c in self.correos_enviados)
        )


class CorreoEnviado(Base):
    """Historial de correos enviados para cada reserva"""
    __tablename__ = "correos_enviados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"), nullable=False)

    # Tipo de correo
    tipo_correo = Column(SQLEnum(TipoCorreo), nullable=False)

    # Detalles del envío
    destinatario = Column(String(200), nullable=False)
    cc = Column(Text, nullable=True)  # Lista de CC separados por coma
    asunto = Column(String(500), nullable=False)
    cuerpo_html = Column(Text, nullable=True)
    cuerpo_texto = Column(Text, nullable=True)

    # Estado del envío
    estado = Column(SQLEnum(EstadoEnvio), default=EstadoEnvio.PENDIENTE, nullable=False)
    fecha_programado = Column(DateTime, nullable=False)
    fecha_enviado = Column(DateTime, nullable=True)
    fecha_error = Column(DateTime, nullable=True)
    mensaje_error = Column(Text, nullable=True)

    # Reintentos
    intentos = Column(Integer, default=0)
    max_intentos = Column(Integer, default=3)

    # Metadatos
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    reserva = relationship("Reserva", back_populates="correos_enviados")

    def __repr__(self):
        return f"<CorreoEnviado {self.tipo_correo.value} - {self.estado.value}>"

    @property
    def puede_reintentar(self) -> bool:
        """Verifica si se puede reintentar el envío"""
        return self.intentos < self.max_intentos and self.estado == EstadoEnvio.ERROR


class OrdenCompra(Base):
    """Órdenes de compra recibidas"""
    __tablename__ = "ordenes_compra"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"), nullable=False, unique=True)

    # Datos del correo de OC
    email_remitente = Column(String(200), nullable=False)
    email_asunto = Column(String(500), nullable=True)
    email_fecha = Column(DateTime, nullable=False)
    email_id = Column(String(200), nullable=True)

    # Datos del archivo PDF de OC
    archivo_nombre = Column(String(500), nullable=True)
    archivo_tamano = Column(Integer, nullable=True)  # en bytes
    archivo_ruta = Column(String(1000), nullable=True)  # ruta local o GCS

    # Número de OC (si se puede extraer del PDF)
    numero_oc = Column(String(100), nullable=True)

    # Validación
    validada = Column(Boolean, default=False)
    fecha_validacion = Column(DateTime, nullable=True)
    validada_por = Column(String(100), nullable=True)  # usuario que validó

    # Observaciones
    observaciones = Column(Text, nullable=True)

    # Metadatos
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    reserva = relationship("Reserva", back_populates="orden_compra")

    def __repr__(self):
        return f"<OrdenCompra {self.numero_oc or 'Sin número'} - Reserva {self.reserva_id}>"


class ConfiguracionCliente(Base):
    """Configuración de clientes que requieren OC"""
    __tablename__ = "configuracion_clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Datos del cliente
    nombre_agencia = Column(String(200), unique=True, nullable=False, index=True)
    email_contacto = Column(String(200), nullable=True)
    telefono_contacto = Column(String(50), nullable=True)

    # Configuración de seguimiento
    requiere_oc = Column(Boolean, default=True, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    # Personalización de tiempos (en días)
    dias_recordatorio_1 = Column(Integer, default=2)
    dias_recordatorio_2 = Column(Integer, default=4)

    # Notas
    notas = Column(Text, nullable=True)

    # Metadatos
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ConfiguracionCliente {self.nombre_agencia} - Activo: {self.activo}>"


class LogSistema(Base):
    """Log de eventos del sistema"""
    __tablename__ = "log_sistema"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Nivel de log
    nivel = Column(String(20), nullable=False, index=True)  # INFO, WARNING, ERROR, CRITICAL

    # Información del evento
    modulo = Column(String(100), nullable=True)
    mensaje = Column(Text, nullable=False)
    detalles = Column(Text, nullable=True)  # JSON serializado

    # Contexto
    reserva_id = Column(Integer, nullable=True)
    usuario = Column(String(100), nullable=True)

    # Metadatos
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f"<LogSistema {self.nivel} - {self.modulo}>"


# Motor de base de datos y sesión
engine = None
SessionLocal = None


def init_db(database_url: Optional[str] = None):
    """Inicializa la base de datos y crea las tablas"""
    global engine, SessionLocal

    if database_url is None:
        database_url = settings.database_url

    # Configuración especial para SQLite
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    engine = create_engine(
        database_url,
        connect_args=connect_args,
        echo=settings.debug,
        poolclass=StaticPool if database_url.startswith("sqlite") else None
    )

    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    # Crear sesión
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return engine


def get_db() -> Session:
    """Obtiene una sesión de base de datos"""
    if SessionLocal is None:
        init_db()

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def crear_cliente_inicial(db: Session):
    """Crea configuración inicial de clientes desde settings"""
    for agency in settings.agencies_list:
        cliente_existente = db.query(ConfiguracionCliente).filter_by(
            nombre_agencia=agency
        ).first()

        if not cliente_existente:
            nuevo_cliente = ConfiguracionCliente(
                nombre_agencia=agency,
                requiere_oc=True,
                activo=True,
                dias_recordatorio_1=settings.days_for_reminder_1,
                dias_recordatorio_2=settings.days_for_reminder_2
            )
            db.add(nuevo_cliente)

    db.commit()


if __name__ == "__main__":
    # Test de inicialización de base de datos
    print("=== Inicializando Base de Datos ===")
    engine = init_db()
    print(f"✅ Base de datos creada: {settings.database_url}")
    print(f"✅ Tablas creadas: {', '.join(Base.metadata.tables.keys())}")

    # Crear clientes iniciales
    db = next(get_db())
    crear_cliente_inicial(db)
    print(f"✅ Clientes configurados: {', '.join(settings.agencies_list)}")

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================

DATABASE_URL = "sqlite:///./device_systems.db"


# Crear motor de conexión
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Crear fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Clase base para los modelos
Base = declarative_base()
from typing import Generator

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Crea una sesión de base de datos para cada petición
    y la cierra cuando termina la petición.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
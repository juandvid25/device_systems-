from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate


# ============================================================
# CREAR PRÉSTAMO
# ============================================================

def create_loan(
    db: Session,
    loan_data: LoanCreate
) -> Loan:

    # Verificar usuario
    user = (
        db.query(User)
        .filter(User.id == loan_data.user_id)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Usuario con ID "
                f"{loan_data.user_id} no encontrado"
            )
        )

    # Verificar dispositivo
    device = (
        db.query(Device)
        .filter(Device.id == loan_data.device_id)
        .first()
    )

    if not device:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Dispositivo con ID "
                f"{loan_data.device_id} no encontrado"
            )
        )

    # Verificar disponibilidad
    if not device.is_available:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El dispositivo no está disponible"
        )

    # Crear préstamo
    db_loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        loan_date=datetime.utcnow(),
        status="active"
    )

    # Marcar dispositivo como no disponible
    device.is_available = False

    db.add(db_loan)

    db.commit()

    db.refresh(db_loan)

    return db_loan


# ============================================================
# OBTENER PRÉSTAMO POR ID
# ============================================================

def get_loan_by_id(
    db: Session,
    loan_id: int
) -> Loan:

    loan = (
        db.query(Loan)
        .filter(Loan.id == loan_id)
        .first()
    )

    if not loan:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Préstamo con ID "
                f"{loan_id} no encontrado"
            )
        )

    return loan


# ============================================================
# DEVOLVER PRÉSTAMO
# ============================================================

def return_loan(
    db: Session,
    loan_id: int
) -> Loan:

    loan = get_loan_by_id(
        db,
        loan_id
    )

    if loan.status.lower() == "returned":

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El préstamo ya fue devuelto"
        )

    loan.status = "returned"

    loan.return_date = datetime.utcnow()

    device = (
        db.query(Device)
        .filter(Device.id == loan.device_id)
        .first()
    )

    if device:

        device.is_available = True

    db.commit()

    db.refresh(loan)

    return loan


# ============================================================
# CONSULTAS CON JOINS Y FILTROS
# ============================================================

def get_loans_with_filters(
    db: Session,
    status_filter: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None
) -> List[dict]:

    query = (
        db.query(Loan, User, Device)
        .join(
            User,
            Loan.user_id == User.id
        )
        .join(
            Device,
            Loan.device_id == Device.id
        )
    )

    filters = []

    if status_filter:

        filters.append(
            Loan.status.ilike(
                f"%{status_filter}%"
            )
        )

    if user_email:

        filters.append(
            User.email.ilike(
                f"%{user_email}%"
            )
        )

    if device_type:

        filters.append(
            Device.device_type.ilike(
                f"%{device_type}%"
            )
        )

    if filters:

        query = query.where(
            and_(*filters)
        )

    results = query.all()

    response = []

    for loan, user, device in results:

        response.append({

            "loan_id": loan.id,

            "status": loan.status,

            "loan_date": loan.loan_date,

            "return_date": loan.return_date,

            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            },

            "device": {
                "id": device.id,
                "name": device.name,
                "serial_number": device.serial_number,
                "device_type": device.device_type,
                "brand": device.brand
            }
        })

    return response


# ============================================================
# PRÉSTAMOS DE UN USUARIO
# ============================================================

def get_loans_by_user_id(
    db: Session,
    user_id: int
) -> List[dict]:

    user_exists = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user_exists:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Usuario con ID "
                f"{user_id} no encontrado"
            )
        )

    query = (
        db.query(Loan, User, Device)
        .join(
            User,
            Loan.user_id == User.id
        )
        .join(
            Device,
            Loan.device_id == Device.id
        )
        .where(
            User.id == user_id
        )
        .all()
    )

    return [

        {
            "loan_id": loan.id,

            "status": loan.status,

            "loan_date": loan.loan_date,

            "return_date": loan.return_date,

            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            },

            "device": {
                "id": device.id,
                "name": device.name,
                "serial_number": device.serial_number,
                "device_type": device.device_type,
                "brand": device.brand
            }
        }

        for loan, user, device in query
    ]


# ============================================================
# PRÉSTAMOS DE UN DISPOSITIVO
# ============================================================

def get_loans_by_device_id(
    db: Session,
    device_id: int
) -> List[dict]:

    device_exists = (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

    if not device_exists:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Dispositivo con ID "
                f"{device_id} no encontrado"
            )
        )

    query = (
        db.query(Loan, User, Device)
        .join(
            User,
            Loan.user_id == User.id
        )
        .join(
            Device,
            Loan.device_id == Device.id
        )
        .where(
            Device.id == device_id
        )
        .all()
    )

    return [

        {
            "loan_id": loan.id,

            "status": loan.status,

            "loan_date": loan.loan_date,

            "return_date": loan.return_date,

            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            },

            "device": {
                "id": device.id,
                "name": device.name,
                "serial_number": device.serial_number,
                "device_type": device.device_type,
                "brand": device.brand
            }
        }

        for loan, user, device in query
    ]
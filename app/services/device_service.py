from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate


# ============================================================
# CREAR DISPOSITIVO
# ============================================================

def create_device(
    db: Session,
    device_data: DeviceCreate
) -> Device:

    existing_device = (
        db.query(Device)
        .filter(
            Device.serial_number == device_data.serial_number
        )
        .first()
    )

    if existing_device:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Ya existe un dispositivo registrado "
                f"con el número de serie "
                f"'{device_data.serial_number}'"
            )
        )

    db_device = Device(
        **device_data.model_dump()
    )

    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    return db_device


# ============================================================
# OBTENER DISPOSITIVOS CON FILTROS
# ============================================================

def get_devices(
    db: Session,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None
) -> List[Device]:

    query = db.query(Device)

    if device_type is not None:

        query = query.filter(
            Device.device_type.ilike(
                f"%{device_type}%"
            )
        )

    if is_available is not None:

        query = query.filter(
            Device.is_available == is_available
        )

    if brand is not None:

        query = query.filter(
            Device.brand.ilike(
                f"%{brand}%"
            )
        )

    if search is not None:

        search_filter = f"%{search}%"

        query = query.filter(
            or_(
                Device.name.ilike(search_filter),
                Device.serial_number.ilike(search_filter),
                Device.brand.ilike(search_filter),
                Device.device_type.ilike(search_filter)
            )
        )

    return query.all()


# ============================================================
# OBTENER DISPOSITIVO POR ID
# ============================================================

def get_device_by_id(
    db: Session,
    device_id: int
) -> Device:

    device = (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

    if not device:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Dispositivo con ID "
                f"{device_id} no encontrado"
            )
        )

    return device


# ============================================================
# ACTUALIZAR DISPOSITIVO
# ============================================================

def update_device(
    db: Session,
    device_id: int,
    device_data: DeviceUpdate,
    partial: bool = False
) -> Device:

    db_device = get_device_by_id(
        db,
        device_id
    )

    update_data = device_data.model_dump(
        exclude_unset=partial
    )

    if (
        "serial_number" in update_data
        and update_data["serial_number"]
        != db_device.serial_number
    ):

        existing = (
            db.query(Device)
            .filter(
                Device.serial_number
                == update_data["serial_number"],
                Device.id != device_id
            )
            .first()
        )

        if existing:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"El número de serie "
                    f"'{update_data['serial_number']}' "
                    f"ya pertenece a otro dispositivo"
                )
            )

    for field, value in update_data.items():

        setattr(
            db_device,
            field,
            value
        )

    db.commit()
    db.refresh(db_device)

    return db_device


# ============================================================
# ELIMINAR DISPOSITIVO
# ============================================================

def delete_device(
    db: Session,
    device_id: int
) -> None:

    db_device = get_device_by_id(
        db,
        device_id
    )

    has_active_loans = any(
        loan.status.lower() == "active"
        for loan in db_device.loans
    )

    if has_active_loans:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se puede eliminar un dispositivo "
                "que actualmente se encuentra "
                "en préstamo activo"
            )
        )

    db.delete(db_device)
    db.commit()
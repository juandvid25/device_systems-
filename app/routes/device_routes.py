from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.device_schema import (
    DeviceCreate,
    DeviceResponse,
    DeviceUpdate
)

from app.schemas.loan_schema import LoanDetailCustomResponse

from app.services import device_service, loan_service


router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


# ============================================================
# OBTENER DISPOSITIVOS
# ============================================================

@router.get(
    "/",
    response_model=List[DeviceResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar dispositivos",
    description=(
        "Obtiene los dispositivos registrados "
        "permitiendo filtros por tipo, disponibilidad, "
        "marca y búsqueda general."
    ),
    response_description="Lista de dispositivos"
)
def get_devices(
    device_type: Optional[str] = Query(
        None,
        description="Filtrar por tipo de dispositivo"
    ),
    is_available: Optional[bool] = Query(
        None,
        description="Filtrar por disponibilidad"
    ),
    brand: Optional[str] = Query(
        None,
        description="Filtrar por marca"
    ),
    search: Optional[str] = Query(
        None,
        description=(
            "Buscar por nombre, serial, "
            "tipo o marca"
        )
    ),
    db: Session = Depends(get_db)
):

    return device_service.get_devices(
        db=db,
        device_type=device_type,
        is_available=is_available,
        brand=brand,
        search=search
    )


# ============================================================
# PRÉSTAMOS DE UN DISPOSITIVO
# ============================================================

@router.get(
    "/{device_id}/loans",
    response_model=List[LoanDetailCustomResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener préstamos de un dispositivo",
    description=(
        "Obtiene el historial de préstamos "
        "asociados a un dispositivo."
    )
)
def get_device_loans(
    device_id: int,
    db: Session = Depends(get_db)
):

    return loan_service.get_loans_by_device_id(
        db,
        device_id
    )


# ============================================================
# OBTENER DISPOSITIVO POR ID
# ============================================================

@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener dispositivo",
    description="Obtiene un dispositivo mediante su ID."
)
def get_device_by_id(
    device_id: int,
    db: Session = Depends(get_db)
):

    return device_service.get_device_by_id(
        db,
        device_id
    )


# ============================================================
# CREAR DISPOSITIVO
# ============================================================

@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description=(
        "Registra un nuevo dispositivo. "
        "El número de serie debe ser único."
    ),
    response_description="Dispositivo creado"
)
def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db)
):

    return device_service.create_device(
        db,
        device_data
    )


# ============================================================
# ACTUALIZACIÓN COMPLETA
# ============================================================

@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo",
    description="Actualiza los datos del dispositivo."
)
def update_device_complete(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db)
):

    return device_service.update_device(
        db,
        device_id,
        device_data,
        partial=False
    )


# ============================================================
# ACTUALIZACIÓN PARCIAL
# ============================================================

@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente dispositivo",
    description=(
        "Actualiza solamente los campos "
        "enviados del dispositivo."
    )
)
def update_device_partial(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db)
):

    return device_service.update_device(
        db,
        device_id,
        device_data,
        partial=True
    )


# ============================================================
# ELIMINAR DISPOSITIVO
# ============================================================

@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description=(
        "Elimina un dispositivo siempre que "
        "no tenga un préstamo activo."
    )
)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db)
):

    device_service.delete_device(
        db,
        device_id
    )

    return None
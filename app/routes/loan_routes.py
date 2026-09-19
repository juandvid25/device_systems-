from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.loan_schema import (
    LoanCreate,
    LoanResponse,
    LoanDetailCustomResponse
)

from app.services import loan_service


router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


# ============================================================
# LISTAR PRÉSTAMOS
# ============================================================

@router.get(
    "/",
    response_model=List[LoanDetailCustomResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos",
    description=(
        "Obtiene los préstamos utilizando "
        "JOIN entre usuarios y dispositivos. "
        "Permite filtrar por estado, correo "
        "del usuario y tipo de dispositivo."
    ),
    response_description="Lista de préstamos"
)
def get_loans(
    status_filter: Optional[str] = Query(
        default=None,
        alias="status",
        description=(
            "Filtrar por estado: "
            "active, returned u overdue"
        )
    ),
    user_email: Optional[str] = Query(
        default=None,
        description="Filtrar por correo electrónico"
    ),
    device_type: Optional[str] = Query(
        default=None,
        description="Filtrar por tipo de dispositivo"
    ),
    db: Session = Depends(get_db)
):

    return loan_service.get_loans_with_filters(
        db=db,
        status_filter=status_filter,
        user_email=user_email,
        device_type=device_type
    )


# ============================================================
# DETALLES DE TODOS LOS PRÉSTAMOS
# ============================================================

@router.get(
    "/details",
    response_model=List[LoanDetailCustomResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener detalles de préstamos",
    description=(
        "Obtiene los préstamos junto con "
        "la información básica del usuario "
        "y del dispositivo."
    )
)
def get_loans_details(
    db: Session = Depends(get_db)
):

    return loan_service.get_loans_with_filters(
        db=db
    )


# ============================================================
# OBTENER PRÉSTAMO POR ID
# ============================================================

@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener préstamo",
    description="Obtiene un préstamo mediante su ID."
)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):

    return loan_service.get_loan_by_id(
        db,
        loan_id
    )


# ============================================================
# CREAR PRÉSTAMO
# ============================================================

@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description=(
        "Crea un préstamo verificando que "
        "el usuario exista, que el dispositivo "
        "exista y que esté disponible."
    ),
    response_description="Préstamo creado"
)
def create_loan(
    loan_data: LoanCreate,
    db: Session = Depends(get_db)
):

    return loan_service.create_loan(
        db,
        loan_data
    )


# ============================================================
# DEVOLVER PRÉSTAMO
# ============================================================

@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Devolver préstamo",
    description=(
        "Registra la devolución del dispositivo, "
        "actualiza la fecha de devolución y "
        "vuelve a marcar el dispositivo como disponible."
    )
)
def return_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):

    return loan_service.return_loan(
        db,
        loan_id
    )
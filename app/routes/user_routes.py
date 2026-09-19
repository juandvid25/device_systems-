from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse,
    UserRole
)

from app.schemas.loan_schema import LoanDetailCustomResponse

from app.services import user_service, loan_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ============================================================
# LISTAR USUARIOS
# ============================================================

@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description=(
        "Lista los usuarios permitiendo "
        "filtros por rol, estado y ordenamiento."
    )
)
def get_users(
    role: UserRole | None = Query(
        default=None,
        description="Filtrar por rol"
    ),
    is_active: bool | None = Query(
        default=None,
        description="Filtrar por estado activo/inactivo"
    ),
    order_by: str | None = Query(
        default=None,
        description=(
            "Ordenar por name o created_at"
        )
    ),
    descending: bool = Query(
        default=False,
        description="Orden descendente"
    ),
    db: Session = Depends(get_db)
):

    if role is not None:

        return user_service.get_users_by_role(
            db,
            role.value
        )

    if is_active is not None:

        return user_service.get_users_by_status(
            db,
            is_active
        )

    if order_by is not None:

        return user_service.get_users_ordered(
            db,
            order_by=order_by,
            descending=descending
        )

    return user_service.get_users(db)


# ============================================================
# PRÉSTAMOS DE UN USUARIO
# ============================================================

@router.get(
    "/{user_id}/loans",
    response_model=list[LoanDetailCustomResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener préstamos de un usuario",
    description=(
        "Obtiene todos los préstamos realizados "
        "por un usuario."
    )
)
def get_user_loans(
    user_id: int,
    db: Session = Depends(get_db)
):

    return loan_service.get_loans_by_user_id(
        db,
        user_id
    )


# ============================================================
# OBTENER USUARIO POR ID
# ============================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario",
    description="Obtiene un usuario mediante su ID."
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = user_service.get_user_by_id(
        db,
        user_id
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return user


# ============================================================
# CREAR USUARIO
# ============================================================

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description=(
        "Crea un nuevo usuario verificando "
        "que el correo no esté registrado."
    )
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = user_service.get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    return user_service.create_user(
        db,
        user_data
    )


# ============================================================
# ACTUALIZAR USUARIO
# ============================================================

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario"
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):

    existing_user = user_service.get_user_by_id(
        db,
        user_id
    )

    if existing_user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    user_with_email = user_service.get_user_by_email(
        db,
        user_data.email
    )

    if (
        user_with_email
        and user_with_email.id != user_id
    ):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "El email ya está registrado "
                "por otro usuario"
            )
        )

    return user_service.update_user(
        db,
        user_id,
        user_data
    )


# ============================================================
# ACTUALIZACIÓN PARCIAL
# ============================================================

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente usuario"
)
def patch_user(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db)
):

    existing_user = user_service.get_user_by_id(
        db,
        user_id
    )

    if existing_user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if user_data.email is not None:

        user_with_email = (
            user_service.get_user_by_email(
                db,
                user_data.email
            )
        )

        if (
            user_with_email
            and user_with_email.id != user_id
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "El email ya está registrado "
                    "por otro usuario"
                )
            )

    return user_service.patch_user(
        db,
        user_id,
        user_data
    )


# ============================================================
# ELIMINAR USUARIO
# ============================================================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    deleted = user_service.delete_user(
        db,
        user_id
    )

    if not deleted:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return {
        "message": "Usuario eliminado correctamente"
    }
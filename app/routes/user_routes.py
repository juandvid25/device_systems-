from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse,
    UserRole,
)
from app.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(
    role: UserRole | None = Query(default=None, description="Filtrar por rol"),
    is_active: bool | None = Query(default=None, description="Filtrar por estado activo/inactivo"),
    order_by: str | None = Query(default=None, description="Ordenar por 'name' o 'created_at'"),
    descending: bool = Query(default=False, description="Orden descendente"),
    db: Session = Depends(get_db)
):
    """Lista usuarios permitiendo filtros por rol, estado y ordenamiento."""
    if role is not None:
        return user_service.get_users_by_role(db, role.value)
    if is_active is not None:
        return user_service.get_users_by_status(db, is_active)
    if order_by is not None:
        return user_service.get_users_ordered(db, order_by=order_by, descending=descending)

    return user_service.get_users(db)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario por su ID."""
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario validando que el email no esté registrado."""
    existing_user = user_service.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    return user_service.create_user(db, user_data)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Actualización completa de un usuario."""
    existing_user = user_service.get_user_by_id(db, user_id)
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    user_with_email = user_service.get_user_by_email(db, user_data.email)
    if user_with_email and user_with_email.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado por otro usuario"
        )

    return user_service.update_user(db, user_id, user_data)


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def patch_user(user_id: int, user_data: UserPatch, db: Session = Depends(get_db)):
    """Actualización parcial de un usuario."""
    existing_user = user_service.get_user_by_id(db, user_id)
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if user_data.email is not None:
        user_with_email = user_service.get_user_by_email(db, user_data.email)
        if user_with_email and user_with_email.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado por otro usuario"
            )

    return user_service.patch_user(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario por su ID."""
    deleted = user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return {"message": "Usuario eliminado correctamente"}
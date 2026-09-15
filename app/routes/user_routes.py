from fastapi import APIRouter, Depends, Query, status

from app.dependencies.user_dependencies import get_user_or_404
from app.schemas.user_schema import (
    UserCreate,
    UserPatch,
    UserResponse,
    UserRole,
    UserUpdate,
)
from app.services.user_service import (
    create_user,
    delete_user,
    get_users,
    patch_user,
    update_user,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Obtiene todos los usuarios y permite filtrarlos por rol o estado.",
    response_description="Lista de usuarios encontrada."
)
def list_users(
    role: UserRole | None = Query(default=None),
    is_active: bool | None = Query(default=None)
):
    return get_users(
        role=role,
        is_active=is_active
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario",
    description="Obtiene un usuario por su identificador.",
    response_description="Usuario encontrado."
)
def get_user(
    user: UserResponse = Depends(get_user_or_404)
):
    return user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario y valida que su correo no esté registrado.",
    response_description="Usuario creado correctamente."
)
def create_user_endpoint(
    user: UserCreate
):
    return create_user(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completamente",
    description="Reemplaza completamente la información de un usuario existente.",
    response_description="Usuario actualizado correctamente."
)
def update_user_endpoint(
    user: UserUpdate,
    existing_user: UserResponse = Depends(get_user_or_404)
):
    return update_user(
        existing_user,
        user
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente",
    description="Modifica solamente los campos enviados del usuario existente.",
    response_description="Usuario actualizado parcialmente."
)
def patch_user_endpoint(
    user: UserPatch,
    existing_user: UserResponse = Depends(get_user_or_404)
):
    return patch_user(
        existing_user,
        user
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario existente por su identificador.",
    response_description="Usuario eliminado correctamente."
)
def delete_user_endpoint(
    existing_user: UserResponse = Depends(get_user_or_404)
):
    delete_user(existing_user)

    return None
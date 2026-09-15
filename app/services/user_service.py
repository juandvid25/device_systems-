from fastapi import HTTPException, status

from app.data.users_db import users_db
from app.schemas.user_schema import UserCreate, UserPatch, UserUpdate, UserResponse


def get_users(role=None, is_active=None):
    users = users_db

    if role is not None:
        users = [user for user in users if user.role == role]

    if is_active is not None:
        users = [user for user in users if user.is_active == is_active]

    return users


def create_user(user: UserCreate) -> UserResponse:
    existing_user = next(
        (existing for existing in users_db if existing.email == user.email),
        None
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )

    new_id = max((existing.id for existing in users_db), default=0) + 1

    new_user = UserResponse(
        id=new_id,
        **user.model_dump()
    )

    users_db.append(new_user)

    return new_user


def update_user(
    existing_user: UserResponse,
    user: UserUpdate
) -> UserResponse:

    email_exists = next(
        (
            user_db
            for user_db in users_db
            if user_db.email == user.email
            and user_db.id != existing_user.id
        ),
        None
    )

    if email_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.role = user.role
    existing_user.is_active = user.is_active

    return existing_user


def patch_user(
    existing_user: UserResponse,
    user: UserPatch
) -> UserResponse:

    update_data = user.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar"
        )

    if "email" in update_data:

        email_exists = next(
            (
                user_db
                for user_db in users_db
                if user_db.email == update_data["email"]
                and user_db.id != existing_user.id
            ),
            None
        )

        if email_exists is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado"
            )

    for field, value in update_data.items():
        setattr(existing_user, field, value)

    return existing_user


def delete_user(existing_user: UserResponse) -> None:
    users_db.remove(existing_user)
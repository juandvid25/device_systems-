from fastapi import HTTPException, status

from app.data.users_db import users_db
from app.schemas.user_schema import UserResponse


def get_user_or_404(user_id: int) -> UserResponse:
    """Obtiene un usuario por ID o genera un error 404 si no existe."""
    user = next(
        (user for user in users_db if user.id == user_id),
        None
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return user
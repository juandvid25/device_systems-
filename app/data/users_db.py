from app.schemas.user_schema import UserResponse, UserRole


# Base de datos temporal en memoria
users_db = [
    UserResponse(
        id=1,
        name="Juan David",
        email="juan@gmail.com",
        role=UserRole.USER,
        is_active=True
    ),
    UserResponse(
        id=2,
        name="Maria Lopez",
        email="maria@gmail.com",
        role=UserRole.ADMIN,
        is_active=True
    ),
    UserResponse(
        id=3,
        name="Carlos Perez",
        email="carlos@gmail.com",
        role=UserRole.SUPPORT,
        is_active=False
    )
]
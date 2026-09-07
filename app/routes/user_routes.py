from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.user_schema import UserCreate, UserResponse, UserRole


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


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


# ==========================================================
# GET /users
# Obtener todos los usuarios y aplicar filtros
# ==========================================================

@router.get("", response_model=list[UserResponse])
def get_users(
    role: UserRole | None = Query(default=None),
    is_active: bool | None = Query(default=None)
):
    users = users_db

    # Filtrar por rol
    if role is not None:
        users = [
            user for user in users
            if user.role == role
        ]

    # Filtrar por estado
    if is_active is not None:
        users = [
            user for user in users
            if user.is_active == is_active
        ]

    return users


# ==========================================================
# GET /users/{user_id}
# Obtener un usuario por ID
# ==========================================================

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):

    user = next(
        (user for user in users_db if user.id == user_id),
        None
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


# ==========================================================
# POST /users
# Crear un nuevo usuario
# ==========================================================

@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):

    # Verificar si el correo ya existe
    existing_user = next(
        (
            existing
            for existing in users_db
            if existing.email == user.email
        ),
        None
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="El correo electrónico ya está registrado"
        )

    # Generar nuevo ID
    new_id = max(
        (existing.id for existing in users_db),
        default=0
    ) + 1

    # Crear usuario
    new_user = UserResponse(
        id=new_id,
        **user.model_dump()
    )

    # Guardar usuario
    users_db.append(new_user)

    return new_user
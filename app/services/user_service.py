from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch


def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role.value if hasattr(user_data.role, 'value') else user_data.role,
        is_active=user_data.is_active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User | None:
    user = get_user_by_id(db, user_id)
    if user is None:
        return None

    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role.value if hasattr(user_data.role, 'value') else user_data.role
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)
    return user


def patch_user(db: Session, user_id: int, user_data: UserPatch) -> User | None:
    user = get_user_by_id(db, user_id)
    if user is None:
        return None

    data = user_data.model_dump(exclude_unset=True)
    for field, value in data.items():
        if field == "role" and value is not None and hasattr(value, 'value'):
            value = value.value
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if user is None:
        return False

    db.delete(user)
    db.commit()
    return True


def get_users_by_role(db: Session, role: str) -> list[User]:
    return db.query(User).filter(User.role == role).all()


def get_users_by_status(db: Session, is_active: bool) -> list[User]:
    return db.query(User).filter(User.is_active == is_active).all()


def get_users_ordered(db: Session, order_by: str = "name", descending: bool = False) -> list[User]:
    if order_by == "created_at":
        column = User.created_at
    else:
        column = User.name

    if descending:
        column = column.desc()
    else:
        column = column.asc()

    return db.query(User).order_by(column).all()
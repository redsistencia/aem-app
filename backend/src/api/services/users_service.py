from sqlalchemy.orm import Session
from models.user import User, UserCreate, UserLogin
from exceptions.user_exceptions import UserNotFound, InvalidUserCredentials, UserExists
from repositories.users_repo import get_user_by_email, create_user
from security.hash import verify_password

def register_user_service(db: Session, user_data: UserCreate) -> User:
    # Buscar si ya existe un usuario con el mismo email
    existing = get_user_by_email(db, user_data.email)

    # Si existe, lanzar error
    if existing:
        raise UserExists()

    # Crear el usuario con los datos proporcionados
    return create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        role=user_data.role
    )


def login_user_service(db: Session, login_data: UserLogin) -> User:
    # Buscar el usuario por email
    user = get_user_by_email(db, login_data.email)

    # Error si el usuario no existe
    if not user:
        raise UserNotFound()

    # Verificar que la contraseña sea correcta
    if not verify_password(login_data.password, user.password):
        raise InvalidUserCredentials()

    # Devolver el usuario completo si las credenciales son válidas
    return user
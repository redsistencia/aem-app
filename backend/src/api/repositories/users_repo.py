from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from src.api.exceptions.user_exceptions import UserExists
from src.api.models.user import User, UserRole
from src.api.security.hash import hash_password

# Obtener usuario por email
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(func.lower(User.email) == email.lower()).first()

# Crear un nuevo usuario
def create_user(db: Session, username: str, email: str, password: str, role: UserRole) -> User:
    hashed = hash_password(password) # Hashear la contraseña antes de guardar

    # Crear la instancia de User
    new_user = User(
        username=username,
        email=email.lower(),
        password=hashed,
        role=role
    )

    db.add(new_user)        # Agregar user a la sesión de la DB
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise UserExists()
    db.refresh(new_user)    # db.refresh() actualiza el objeto con los datos finales de la DB
    return new_user
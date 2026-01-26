from sqlalchemy.orm import Session
from models.user import User, UserRole
from security.hash import hash_password

# Obtener usuario por email
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

# Crear un nuevo usuario
def create_user(db: Session, username: str, email: str, password: str, role: UserRole) -> User:
    hashed = hash_password(password) # Hashear la contraseña antes de guardar

    # Crear la instancia de User
    new_user = User(
        username=username,
        email=email,
        password=hashed,
        role=role
    )

    db.add(new_user)        # Agregar user a la sesión de la DB
    db.commit()         # db.commit() guarda cambios
    db.refresh(new_user)    # db.refresh() actualiza el objeto con los datos finales de la DB
    return new_user
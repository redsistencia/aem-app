.venv/bin/python -c '
from getpass import getpass
from src.api.models.user import UserCreate
from src.api.services.users_service import register_user_service
from src.db.session import SessionLocal

data = UserCreate(
    username=input("Nombre de usuario: ").strip(),
    email=input("Email: ").strip(),
    password=getpass("Contraseña: "),
    role="admin",
)

with SessionLocal() as db:
    user = register_user_service(db, data)
    print(f"Administrador creado: {user.email}")
'
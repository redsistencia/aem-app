from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.user import UserCreate, UserLogin, UserRead, User
from services.users_service import register_user_service, login_user_service
from security.auth import create_access_token, require_role

# Inicializa el router de FastAPI para las suscripciones
router = APIRouter()

# Endpoint para registrar un usuario administrador
@router.post("/admin/register", response_model=UserRead)
def register_user_endpoint(
    user_data: UserCreate,                  # Datos del usuario que llegan en el body (email, password, etc.)
    db: Session = Depends(get_db),          # Sesión de base de datos inyectada por FastAPI
    user: User = Depends(require_role("admin")) # Control de acceso por rol
) -> UserRead:
    # Llama al servicio encargado de registrar el usuario en la base de datos
    return register_user_service(db, user_data)


# Endpoint para iniciar sesión como administrador
@router.post("/login")
def login_user_endpoint(
    login_data: UserLogin,            # Datos de login (email y contraseña)
    db: Session = Depends(get_db)     # Sesión de base de datos
) -> dict[str, Any]:
    # Verifica las credenciales del usuario
    user = login_user_service(db, login_data)

    # Genera un token JWT con información del usuario
    token = create_access_token({
        "user_email": user.email,     # Email del usuario autenticado
        "role": user.role             # Rol del usuario (admin, user, etc.)
    })

    # Devuelve el token y datos básicos del usuario
    return {
        "access_token": token,        # Token JWT
        "token_type": "bearer",        # Tipo de autenticación
        "user_email": user.email,      # Email del usuario
        "user_role": user.role         # Rol del usuario
    }

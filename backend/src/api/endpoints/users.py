from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.user import UserCreate, UserLogin, UserRead, User
from services.users_service import register_user_service, login_user_service
from security.auth import create_access_token, require_role
from fastapi.security import OAuth2PasswordRequestForm

# Inicializa el router de FastAPI para las suscripciones
router = APIRouter(
    prefix="/admin",
    tags=["Admin · Usuaries"],
)

# Endpoint para registrar un usuario administrador
@router.post("/register", response_model=UserRead)
def register_user_endpoint(
    user_data: UserCreate,                  # Datos del usuario que llegan en el body (email, password, etc.)
    db: Session = Depends(get_db),          # Sesión de base de datos inyectada por FastAPI
    user: User = Depends(require_role("admin")) # Control de acceso por rol
) -> UserRead:
    # Llama al servicio encargado de registrar el usuario en la base de datos
    return register_user_service(db, user_data)


# Endpoint para iniciar sesión como administrador
@router.post("/auth/token", response_model=dict[str, Any])
def login_user_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    login_data = UserLogin(
        email=form_data.username,   # Swagger manda "username"
        password=form_data.password,
    )

    user = login_user_service(db, login_data)

    token = create_access_token({
        "user_email": user.email,
        "role": user.role,
    })

    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.post("/login", response_model=dict[str, Any])
def login_user_endpoint(
    login_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = login_user_service(db, login_data)

    token = create_access_token({
        "user_email": user.email,
        "role": user.role,
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_email": user.email,
        "user_role": user.role,
    }
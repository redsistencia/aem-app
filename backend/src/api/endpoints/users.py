from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from src.api.exceptions.user_exceptions import InvalidUserCredentials
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.api.models.user import UserCreate, UserLogin, UserRead, User
from src.api.services.users_service import register_user_service, login_user_service
from src.api.security.auth import create_access_token, get_current_user, require_role

# Inicializa el router de FastAPI para las suscripciones
router = APIRouter(
    prefix="/admin/users",
    tags=["Admin · Usuaries"],
)

# Endpoint para registrar un usuario administrador
@router.post("/", response_model=UserRead, status_code=201)
def register_user_endpoint(
    user_data: UserCreate,                  # Datos del usuario que llegan en el body (email, password, etc.)
    db: Session = Depends(get_db),          # Sesión de base de datos inyectada por FastAPI
    user: User = Depends(require_role("admin")) # Control de acceso por rol
) -> UserRead:
    # Llama al servicio encargado de registrar el usuario en la base de datos
    return register_user_service(db, user_data)


# Lógica compartida entre el login JSON y el formulario OAuth2.
def issue_login_token(
    login_data: UserLogin,            # Datos de login (email y contraseña)
    db: Session,
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


@router.post("/login")
def login_user_endpoint(login_data: UserLogin, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Login JSON usado por el frontend."""
    return issue_login_token(login_data, db)


@router.post("/token")
def login_oauth2_endpoint(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Login OAuth2 de Swagger: username contiene el email del usuario."""
    try:
        login_data = UserLogin(email=form.username, password=form.password)
    except ValidationError:
        raise InvalidUserCredentials() from None
    return issue_login_token(login_data, db)


@router.get("/me", response_model=UserRead)
def current_user(user: User = Depends(get_current_user)) -> User:
    return user

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from typing import Any
import os
from models.user import User

# Este módulo gestiona la autenticación (JWT) y la autorización (roles) del backend.

# Carga las variables de entorno
load_dotenv()

# SECRET_KEY: clave secreta para firmar los tokens.
# ALGORITHM: HS256 es un algoritmo estándar y seguro para JWT.
# EXPIRATION: duración del token en minutos.
_raw = os.getenv("secret_key")
if _raw is None:
    raise RuntimeError("secret_key no definida")

SECRET_KEY: str = _raw
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Ubicacion donde el cliente debe enviar el token, FastAPI lo extrae automáticamente.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

# Copia los datos que quieres meter en el token (email, rol…).
# Añade una fecha de expiración.
# Codifica todo en un JWT firmado con tu SECRET_KEY.
def create_access_token(data: dict[str, Any], expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Lee el header Authorization, extrae el token, lo pasa a esta función.
def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        # Si el token es inválido o está manipulado → error.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extrae datos del usuario.
        email = payload.get("user_email")
        role = payload.get("role")

        # Valida los datos, si falta algo, token invalido.
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return User(email=email, role=role)

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Esta funcion permite definir roles permitidos en un endpoint.
# Si el rol del usuario no está en la lista, lanza un error 403.
def require_role(*allowed_roles: str):
    def wrapper(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )
        return user

    return wrapper
    
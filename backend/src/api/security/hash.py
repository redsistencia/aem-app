from passlib.context import CryptContext

# Configuración del contexto de encriptación usando bcrypt
# "deprecated='auto'" permite migrar hashes antiguos si fuera necesario
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Genera un hash seguro a partir de la contraseña en texto plano
    # Este hash es el que se almacena en la base de datos
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verifica que la contraseña en texto plano coincida
    # con el hash almacenado en la base de datos
    return pwd_context.verify(plain_password, hashed_password)

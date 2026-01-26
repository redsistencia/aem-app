import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

# Obtenemos los datos de conexión
DB_USER = os.getenv("user")
DB_HOST = os.getenv("host")
DB_PORT = os.getenv("port")
DB_NAME = os.getenv("dbname")
DB_PASSWORD = os.getenv("password")
SSL_MODE = "?sslmode=require" if DB_PORT == "5432" else ""

# Construimos la URL de conexión segura

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}{SSL_MODE}"

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

class Settings(BaseSettings):
    env: str = "local"
    debug: bool = False
    app_name: str = "Argentinxs en Mallorca"

    session_cookie_name: str = "aem_session"

    brevo_api_key: str
    brevo_sender_email: str
    brevo_sender_name: str

    frontend_url: str

    user: str
    password: str
    host: str 
    port: int
    dbname: str

    secret_key: str
    database_url: str

    # Configuración pydantic v2
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


# mypy no puede inferir carga desde env → ignore justificado
settings = Settings()  # type: ignore[call-arg]

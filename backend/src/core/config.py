import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

class Settings(BaseSettings):
    env: str = "local"
    debug: bool = False
    app_name: str = "Argentinxs en Mallorca"

    secret_key: str = Field(..., min_length=32)
    session_cookie_name: str = "aem_session"

    database_url: str

    brevo_api_key: str
    brevo_sender_email: str
    brevo_sender_name: str

    frontend_url: str

    # Configuración pydantic v2
    model_config = SettingsConfigDict(env_file=".env")


# mypy no puede inferir carga desde env → ignore justificado
settings = Settings()  # type: ignore[call-arg]

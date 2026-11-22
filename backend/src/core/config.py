from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    env: str = "local"
    debug: bool = Field(default=False, validation_alias=AliasChoices("DEBUG", "debug"))
    app_name: str = "Argentinxs en Mallorca"
    session_cookie_name: str = "aem_session"
    brevo_api_key: str = ""
    brevo_sender_email: str = ""
    brevo_sender_name: str = ""
    frontend_url: str = "http://localhost:5173"
    db_user: str = Field(default="postgres", alias="user")
    db_password: str = Field(default="", alias="password")
    db_host: str = Field(default="localhost", alias="host")
    db_port: int = Field(default=5432, alias="port")
    db_name: str = Field(default="postgres", alias="dbname")
    db_sslmode: str | None = None
    database_url: str | None = Field(default=None, validation_alias=AliasChoices("DATABASE_URL", "database_url"))
    secret_key: str = Field(validation_alias=AliasChoices("SECRET_KEY", "secret_key"))

    @property
    def sqlalchemy_url(self) -> str:
        if self.database_url:
            return self.database_url
        return URL.create(
            "postgresql+psycopg2",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query={"sslmode": self.db_sslmode} if self.db_sslmode else {},
        ).render_as_string(hide_password=False)

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",
        populate_by_name=True,
        case_sensitive=True,
    )


settings = Settings()

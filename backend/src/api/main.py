from dotenv import load_dotenv
from typing import Dict

# Carga las variables de entorno desde .env
# Debe ejecutarse antes de acceder a os.environ o Settings
load_dotenv()

# Importa la clase principal para crear la API
from fastapi import FastAPI
from src.core.config import settings
from src.db.base import Base
from src.db.session import engine

# Importar modelos para que SQLAlchemy los registre
from src.db.models import subscription, activity, user

from endpoints import activities, subscribers, users

# Crea la instancia de tu API
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(activities.router)
app.include_router(subscribers.router)
app.include_router(users.router)

# Define un endpoint que responde a solicitudes GET en /health
@app.get("/health", status_code=200)
 # Función que se ejecuta cuando alguien visita /health
def health_check() -> Dict[str, str]:
    # Devuelve un JSON indicando que todo está bien
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    print("🚀 Startup event ejecutado")

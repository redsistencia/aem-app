from dotenv import load_dotenv
from typing import Dict

# Carga las variables de entorno desde .env
# Debe ejecutarse antes de acceder a os.environ o Settings
load_dotenv()

# Importa la clase principal para crear la API
from fastapi import FastAPI
from src.api.config import settings

# Crea la instancia de tu API
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

# Define un endpoint que responde a solicitudes GET en /health
@app.get("/health", status_code=200)
 # Función que se ejecuta cuando alguien visita /health
def health_check() -> Dict[str, str]:
    # Devuelve un JSON indicando que todo está bien
    return {"status": "ok"}

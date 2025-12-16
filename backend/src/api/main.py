# Importa la clase principal para crear la API
from fastapi import FastAPI

# Crea la instancia de tu API
app = FastAPI()

# Define un endpoint que responde a solicitudes GET en /health
@app.get("/health", status_code=200)
def health_check():  # Función que se ejecuta cuando alguien visita /health
    # Devuelve un JSON indicando que todo está bien
    return {"status": "ok"}

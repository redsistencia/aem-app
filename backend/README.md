Backend para la API y proyectos relacionados de Argentinos En Mallorca.

## Requisitos
- Python 3.10 o superior

## Configuración inicial

Dentro de la carpeta Backend:

- Crear el entorno virtual dentro de la carpeta Backend:

    python3 -m venv .venv

- Activar el entorno:

    source .venv/bin/activate

- Actualizar herramientas base:

    pip install --upgrade pip setuptools wheel

- Instalar dependencias:

    pip install -r requirements.txt

## Ejecutar la API

En la carpeta /backend:

    uvicorn main:app --reload --app-dir src/api

La API estará disponible en:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs


## Actualizar dependencias

Para agregar nuevas dependencias:

    pip install nombre-paquete
    pip freeze > requirements.txt

## Notas
- Las dependencias están fijadas para garantizar reproducibilidad
- Se recomienda usar un entorno virtual por proyecto
- FastAPI incluye documentación interactiva automáticamente en /docs

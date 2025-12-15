# aem-app
aem-app es una plataforma para Argentinxs en Mallorca, con formulario de asociación, panel admin para cargar actividades y envío automático de newsletters. Usa Svelte en el front, Python + Jinja2 para correos y PostgreSQL para almacenar datos.

## Requisitos
- Python 3.10 o superior

## Configuración inicial

- Crear el entorno virtual:

    python3 -m venv .venv

- Activar el entorno:

    source .venv/bin/activate

- Actualizar herramientas base:

    pip install --upgrade pip setuptools wheel

- Instalar dependencias:

    pip install -r requirements.txt

## Ejecutar la aplicación

    uvicorn app.main:app --reload

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

# Backend para la API y proyectos relacionados de Argentinos En Mallorca

## Requisitos

- Python 3.10 o superior

## Configuración inicial

Dentro de la carpeta Backend:

- Crear el entorno virtual dentro de la carpeta Backend:

  python3 -m venv .venv

- Activar el entorno:

  source .venv/bin/activate

- Desactivar el entorno:

    deactivate

- Actualizar herramientas base:

  pip install --upgrade pip setuptools wheel

- Instalar dependencias:

  pip install -r requirements.txt

- Instalar nuevas librerías:

    python -m pip install package-name

- Al agregar librerías nuevas, exportarlas para que todo el equipo tenga el mismo setup:

    python -m pip freeze > requirements.txt

- Copiar el archivo .env:

    cp .env.example .env

## Levantar el docker

En la carpeta /backend/docker:

docker-compose up

## Ejecutar migraciones

En la carpeta /backend/src/api:

alembic upgrade head

## Ejecutar la API

En la carpeta /backend:

    python -m uvicorn src.api.main:app --reload

    o mejor, usando Run and debug del vscode

La API estará disponible en:

- <http://127.0.0.1:8000>

- <http://127.0.0.1:8000/docs>

## Ejecutar mypy (type checking)

- Tener activado el .venv
- Tener instaladas todos los paquetes
- Ejecutar:
   mypy src/api

## Actualizar dependencias

Para agregar nuevas dependencias:

    pip install nombre-paquete
    pip freeze > requirements.txt

## Databse

Desde la consola:

    sqlite3 aem.db
    .tables
    .schema subscriptions

## Notas

- Las dependencias están fijadas para garantizar reproducibilidad
- Se recomienda usar un entorno virtual por proyecto
- FastAPI incluye documentación interactiva automáticamente en /docs

## Arquitectura del proyecto

Flujo de un request:
Cliente → Endpoint → Service → Repository → DB → Repository → Service → Endpoint → Cliente

api/
│
│
├── endpoints/
│ ├── users.py
│ ├── subscribers.py
│ └── activities.py
│
├── services/
│ ├── users_service.py
│ ├── subscribers_service.py
│ └── activities_service.py
│
├── repositories/
│ ├── users_repo.py
│ ├── subscribers_repo.py
│ └── activities_repo.py
│
├── models/
│ ├── user.py
│ ├── subscriber.py
│ └── activity.py
│
├── security/
│ ├── auth.py
│ └── hash.py
│
├── db/
│ ├── session.py
│ └── base.py
│
└── main.py

## Explicación arquitectura

endpoints/

    - Recibir requests HTTP
    - Validar entrada (con Pydantic)
    - Llamar a la capa services
    - Devolver respuestas JSON
    - Manejar códigos HTTP

services/

    - Reglas de la aplicación.
    - Validaciones.
    - Decidir qué se puede y qué no.

repositories/

    - Interaccion directa a la base de datos con SQLAlchemy.
    - Define que queries se usarán en la comunicación con la DB.

models/

    - Define la forma de los datos.
    - Por un lado se describen los modelos de los datos ORM con SQLAlchemy. (DB)
        - Se usa para guardar en la DB
        - Leer de la DB
        - Migraciones (Alembic)
    - Por otro lado representa el JSON que entra y sale por la API, para esto usamos Schemas Pydantic. (API)
        - Define qué campos espera el backend
        - Define qué tipos
        - Valida automáticamente el JSON
        - Convierte JSON → objeto Python

db/

    - session.py
        - Configuración de la conexión a la DB.
    - base.py
        - Creación de tabla base

security/

    - auth.py
        - Gestion completa de autentificación / control de sesiones.
    - hash.py
        - Funciones de hasheo de password

main.py

    - Punto de entrada de la aplicación, crea la app FastAPI, registra routers y configura middlewares.

## Librerias usadas

fastapi==0.109.2
    - Framework web moderno y rápido para crear APIs REST.
    - Usa type hints de Python para validación automática y documentación (Swagger / OpenAPI).

uvicorn==0.27.1
    - Servidor ASGI de alto rendimiento.
    - Se usa para ejecutar aplicaciones FastAPI en desarrollo y producción.

SQLAlchemy==2.0.25
    - ORM (Object Relational Mapper) para interactuar con bases de datos.
    - Permite trabajar con tablas como si fueran clases de Python.

psycopg2-binary==2.9.9
    - Driver para conectarse a bases de datos PostgreSQL.
    - SQLAlchemy lo utiliza internamente para comunicarse con Postgres.

passlib[bcrypt]==1.7.4
    - Librería para manejar hashing de contraseñas.
    - Incluye soporte para bcrypt y buenas prácticas de seguridad.

bcrypt==4.1.2
    - Algoritmo de hashing seguro para contraseñas.
    - Se usa directamente o a través de passlib para cifrar passwords.

python-jose==3.3.0
    - Implementación de JOSE (JWT, JWS, JWE).
    - Se usa comúnmente para crear y verificar tokens JWT en autenticación.

python-dotenv==1.0.1
    - Permite cargar variables de entorno desde un archivo .env.
    - Útil para manejar secretos como claves, URLs de DB, etc.

email-validator==2.1.0.post1
    - Valida direcciones de correo electrónico.
    - Se integra muy bien con Pydantic y FastAPI para validaciones automáticas.

pydantic==2.6.1
    - Librería para validación y serialización de datos.
    - FastAPI la usa para validar requests y responses usando modelos.

pydantic_core==2.16.2
    - Núcleo interno de alto rendimiento de Pydantic.
    - Maneja la validación rápida de datos (no se usa directamente).

alembic==1.13.1
    - Herramienta de migraciones de bases de datos.
    - Permite versionar y aplicar cambios al esquema de la DB con SQLAlchemy.

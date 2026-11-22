# Argentinxs en Mallorca — Backend

API de la plataforma, construida con FastAPI, SQLAlchemy, Pydantic y PostgreSQL.
Gestiona personas asociadas, actividades y acceso al panel de administración.
El frontend está documentado en [su README](../frontend/README.md).

## Requisitos

- Python 3.11 y un entorno virtual.
- Docker con Docker Compose v2 para la base local.
- Docker Desktop iniciado si trabajás en macOS.

Los comandos siguientes se ejecutan desde `backend/`, salvo indicación contraria.

## Configuración inicial

Desde la raíz del repositorio:

```sh
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
cp .env.example .env
```

Si ya tenés `.env`, conservá su configuración. Editá `secret_key` con una clave
aleatoria propia; el valor `None` del ejemplo debe reemplazarse. Podés generar
una clave con:

```sh
python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

La aplicación carga `backend/.env` independientemente del directorio desde el que
se invoque Python. Las variables del proceso tienen prioridad sobre ese archivo.

| Variable                                     | Uso                                                                                                                              |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `user`, `password`, `host`, `port`, `dbname` | Conexión PostgreSQL. Los valores del ejemplo corresponden al Compose local, en `localhost:5450`.                                 |
| `DATABASE_URL`                               | Conexión completa opcional; tiene prioridad sobre los campos anteriores. Usar el esquema `postgresql+psycopg2://`.               |
| `db_sslmode`                                 | Configurar `require` si el servidor requiere SSL. No se deduce del puerto. Si usás `DATABASE_URL`, incluir `sslmode` en esa URL. |
| `secret_key` o `SECRET_KEY`                  | Clave para firmar los tokens JWT.                                                                                                |
| `frontend_url`                               | Origen permitido por CORS; por defecto, `http://localhost:5173`.                                                                 |
| `debug` o `DEBUG`                            | Booleano; usar `false` en producción.                                                                                            |
| `app_name`                                   | Nombre mostrado en la documentación de la API.                                                                                   |

Al usar los campos de conexión separados, las credenciales con caracteres especiales
se codifican automáticamente. Si proporcionás una URL completa, debe estar correctamente
codificada. PostgreSQL es la base de la aplicación; el archivo histórico `aem.db`
no se usa con la configuración local de PostgreSQL.

## Levantar la base y aplicar migraciones

Primero iniciá Docker Desktop y esperá a que el motor esté disponible. Luego:

```sh
docker compose -f docker/docker-compose.yml up -d --wait db
.venv/bin/alembic -c src/api/alembic.ini upgrade head
```

Compose publica PostgreSQL en `localhost:5450` y conserva los datos en un volumen.
El chequeo de disponibilidad espera a que la base acepte conexiones antes de continuar.
Las migraciones se aplican a la conexión configurada en `.env` o `DATABASE_URL`.

Para consultar el estado y detener el servicio conservando sus datos:

```sh
docker compose -f docker/docker-compose.yml ps
docker compose -f docker/docker-compose.yml stop db
```

La migración de campos públicos de actividades conserva las fechas y ubicaciones
anteriores y asigna direcciones únicas `actividad-<id>` a los registros existentes.

## Ejecutar la API

```sh
.venv/bin/python -m uvicorn src.api.main:app --reload
```

- Documentación interactiva: <http://localhost:8000/docs>.
- Esquema OpenAPI: <http://localhost:8000/openapi.json>.
- Comprobación del proceso: <http://localhost:8000/health>.

`/health` comprueba que la API responde; no verifica la conexión con PostgreSQL.
Para comprobar también una lectura de la base:

```sh
curl --fail http://localhost:8000/activities/
```

## Acceso al panel

El login del frontend recibe JSON con `email` y `password` en
`POST /admin/users/login` y devuelve un token
JWT válido durante 60 minutos. Las operaciones protegidas requieren el encabezado
`Authorization: Bearer <token>`. En cada petición se verifica que el usuario siga
activo y se consulta su rol actual en la base.

- **Admin:** gestiona personas asociadas, registra usuarios y crea, consulta, edita
  o elimina actividades.
- **Editor:** consulta, edita y elimina actividades.

### Autenticarse en Swagger

1. Con la API levantada, abrí <http://localhost:8000/docs>.
2. Pulsá **Authorize** y usá el esquema **OAuth2PasswordBearer**.
3. En **username**, ingresá el **email** del usuario registrado; no su nombre o alias.
4. En **password**, ingresá su contraseña.
5. Dejá **client_id** y **client_secret** vacíos: esta aplicación no los requiere.
6. Pulsá **Authorize** y cerrá el cuadro. Swagger enviará el token automáticamente
   al ejecutar las operaciones protegidas con **Try it out** → **Execute**.

Swagger usa `POST /admin/users/token`, que recibe un formulario OAuth2 con
`username` y `password` (`application/x-www-form-urlencoded`). El frontend conserva
su endpoint JSON `POST /admin/users/login`. Ambos usan la misma validación de
credenciales y emiten tokens con los mismos permisos y vencimiento.

Podés verificar la sesión con `GET /admin/users/me`. Para crear otro usuario,
ejecutá `POST /admin/users/` con una sesión de rol admin. Un error `401` indica
credenciales inválidas, usuario inactivo o token inválido/vencido; un `403` indica
que el rol no tiene permiso. Para cambiar de cuenta, usá **Logout** en el cuadro
**Authorize** y autenticá al otro usuario. Cuando venza el token, repetí el login.

### Crear el primer administrador

No hay credenciales predeterminadas. El primer administrador se crea desde una
terminal, porque el endpoint de alta requiere un admin ya autenticado.

Antes de ejecutar el script, creá el entorno `.venv`, instalá las dependencias,
configurá `.env`, levantá PostgreSQL y aplicá las migraciones como se indica arriba.
Luego, desde `backend/`, ejecutá [first-admin.sh](first-admin.sh):

```sh
bash ./first-admin.sh
```

Desde la raíz del repositorio, primero entrá en la carpeta del backend:

```sh
cd backend
bash ./first-admin.sh
```

El script usa `.venv/bin/python`, por lo que no hace falta activar el entorno ni
dar permisos de ejecución al archivo al invocarlo con `bash`. Te pedirá nombre de
usuario, email y contraseña, y creará un usuario activo con rol `admin` en la base
configurada. Si el email ya existe, el alta se rechaza.

La contraseña debe tener al menos 8 caracteres y ocupar como máximo 72 bytes en
UTF-8. Se solicita de forma oculta y se almacena como hash bcrypt. El email debe
ser único y el nombre de usuario debe tener entre 1 y 20 caracteres. Después podés
usar ese email y contraseña tanto en Swagger como en `/login` del frontend.

## Pruebas y chequeos

Las pruebas habituales usan SQLite en memoria, con sesiones aisladas, sin conectar
con la base de la aplicación:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

La prueba de migración PostgreSQL se omite si no está definida
`AEM_TEST_POSTGRES_URL`. Para ejecutarla, asigná esa variable a una base PostgreSQL
vacía y descartable y volvé a ejecutar el comando anterior. La prueba crea tablas y
datos, que permanecen en esa base al terminar.

Para consultar el estado de las migraciones:

```sh
.venv/bin/alembic -c src/api/alembic.ini current
.venv/bin/alembic -c src/api/alembic.ini heads
```

## Estructura

```text
src/
├── api/
│   ├── main.py          # Aplicación, routers, CORS y errores
│   ├── endpoints/       # Rutas HTTP y dependencias de permisos
│   ├── services/        # Reglas de la aplicación
│   ├── repositories/    # Consultas y persistencia
│   ├── models/          # Modelos y esquemas de usuarios y personas asociadas
│   ├── security/        # JWT y hash de contraseñas
│   ├── exceptions/      # Errores de dominio
│   └── alembic/         # Migraciones
├── core/config.py       # Configuración desde entorno y .env
├── db/                  # Base ORM, sesiones y modelo de actividades
└── schemas/             # Esquemas de actividades

tests/                   # Pruebas de API, configuración y migración
```

El flujo principal es: endpoint → servicio → repositorio → base de datos.
Las versiones de las dependencias se consultan en [requirements.txt](requirements.txt).

## Newsletters

Las altas guardan el consentimiento de newsletter. La baja voluntaria verifica
email y documento, desactiva la asociación y revoca ese consentimiento.

El envío automático todavía no está implementado: no hay servicio de envío,
plantillas ni tareas programadas. Las variables `brevo_api_key`,
`brevo_sender_email` y `brevo_sender_name` están previstas en la configuración,
pero no generan correos. El campo `sent` de las actividades registra un estado;
no dispara un envío.

## Problemas frecuentes

- **`Cannot connect to the Docker daemon`:** iniciá Docker Desktop y esperá a que
  termine de arrancar.
- **`Connection refused` en `localhost:5450`:** levantá PostgreSQL con el comando
  de Compose y revisá el estado del contenedor antes de ejecutar Alembic.
- **Error de credenciales:** verificá que `.env` coincida con la base existente.
  Cambiar las credenciales de Compose no modifica las de un volumen ya inicializado.
- **Tablas o columnas inexistentes:** comprobá la conexión configurada y ejecutá
  `alembic upgrade head` con la ruta de configuración indicada arriba.
- **Error de CORS:** `frontend_url` debe coincidir con el origen del navegador,
  incluido el puerto. `localhost` y `127.0.0.1` son orígenes distintos.

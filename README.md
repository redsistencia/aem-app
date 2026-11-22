# aem-app

aem-app es una plataforma para **Argentinxs en Mallorca**. Permite asociarse,
solicitar la baja, consultar actividades y administrar las actividades y el listado
de personas asociadas desde un panel con acceso por roles.

El frontend usa **Svelte 5, SvelteKit y TypeScript**; el backend, **Python con FastAPI**;
y los datos se almacenan en **PostgreSQL**. El envío automático de newsletters es
una funcionalidad pendiente: actualmente se guarda y administra el consentimiento
para recibirlas.

## Estado actual

| Funcionalidad                 | Realizado                                                                                                                                         | Pendiente                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Asociación                    | Formulario conectado a la API, validación de datos, aceptación de privacidad y consentimiento opcional de newsletter. Persistencia en PostgreSQL. | —                                                                                                        |
| Baja voluntaria               | Verificación por email y documento, desactivación de la asociación y revocación del consentimiento de newsletter.                                 | —                                                                                                        |
| Actividades públicas          | Listado y detalle por slug, con datos de la API.                                                                                                  | —                                                                                                        |
| Administración de actividades | Creación, edición y eliminación desde el panel, con permisos por rol.                                                                             | —                                                                                                        |
| Personas asociadas            | Listado en el panel; consulta, actualización y eliminación disponibles en la API para administradores.                                            | Incorporar edición y eliminación de personas asociadas en la interfaz del panel.                         |
| Autenticación                 | Login con email y contraseña, tokens JWT, cierre de sesión y verificación de usuarios activos y roles.                                            | —                                                                                                        |
| Usuarios administrativos      | Alta del primer admin con `first-admin.sh` y creación de otros usuarios mediante la API autenticada.                                              | Interfaz de administración de usuarios.                                                                  |
| Swagger                       | Documentación interactiva y autenticación OAuth2 con email y contraseña desde **Authorize**.                                                      | —                                                                                                        |
| Newsletters                   | Registro del consentimiento y campo `sent` en las actividades. Variables de configuración de Brevo disponibles.                                   | Integración de envío, plantillas de correo, programación automática y actualización del estado de envío. |
| Base de datos                 | Configuración centralizada, migraciones Alembic y PostgreSQL local con Docker Compose y chequeo de disponibilidad.                                | —                                                                                                        |
| Frontend estático             | Build con fallback de SPA y configuración de Netlify incluida.                                                                                    | —                                                                                                        |
| Pruebas                       | Regresiones de la API, prueba de migración PostgreSQL y pruebas de lógica y componentes del frontend con Vitest y Chromium.                       | —                                                                                                        |

El campo `sent` no dispara un envío de correo. Tampoco hay plantillas Jinja2 ni
tareas programadas implementadas para newsletters.

## Roles

- **Admin:** consulta y gestiona personas asociadas mediante la API, registra
  usuarios y crea, consulta, edita o elimina actividades.
- **Editor:** consulta, edita y elimina actividades.

No hay usuario ni contraseña predeterminados. El primer administrador se crea
mediante el script [backend/first-admin.sh](backend/first-admin.sh), con la base en
marcha y las migraciones aplicadas:

```sh
cd backend
bash ./first-admin.sh
```

El script pide nombre de usuario, email y contraseña. Después se puede iniciar
sesión con ese email y contraseña tanto en el frontend como en Swagger.

## Desarrollo local

Configurá los entornos e instalá las dependencias siguiendo las guías de cada parte:

- [Backend: instalación, variables de entorno, Docker, migraciones y Swagger](backend/README.md).
- [Frontend: instalación, conexión con la API, pruebas y despliegue](frontend/README.md).

Con la configuración inicial completa y Docker iniciado, ejecutá desde `backend/`:

```sh
docker compose -f docker/docker-compose.yml up -d --wait db
.venv/bin/alembic -c src/api/alembic.ini upgrade head
.venv/bin/python -m uvicorn src.api.main:app --reload
```

En otra terminal, desde `frontend/`:

```sh
pnpm dev --open
```

| Servicio               | Dirección local habitual     |
| ---------------------- | ---------------------------- |
| Frontend en desarrollo | <http://localhost:5173>      |
| API                    | <http://localhost:8000>      |
| Swagger                | <http://localhost:8000/docs> |
| PostgreSQL de Docker   | `localhost:5450`             |

`PUBLIC_API_URL` en `frontend/.env` debe apuntar a la API. `frontend_url` en
`backend/.env` debe coincidir con el origen desde el que se abre el sitio para
permitir CORS. Si usás `pnpm preview`, el frontend normalmente corre en
`http://localhost:4173`; configurá ese origen en el backend y reiniciá la API.

## Estructura del repositorio

```text
backend/        API, modelos, migraciones, pruebas y configuración de PostgreSQL
frontend/       Sitio público, panel administrativo y pruebas de componentes
netlify.toml    Configuración del despliegue estático del frontend
```

Los comandos de pruebas, configuración y solución de problemas se detallan en los
README de [backend](backend/README.md#pruebas-y-chequeos) y
[frontend](frontend/README.md#chequeos-y-pruebas).

# Argentinxs en Mallorca — Frontend

Sitio de la plataforma, construido con Svelte 5, SvelteKit, TypeScript y Tailwind CSS.
Incluye asociación, baja voluntaria, actividades públicas y panel de administración.
Se publica como SPA estática y se comunica directamente con la API de Python.

Para preparar PostgreSQL, aplicar las migraciones y levantar la API, seguí el
[README del backend](../backend/README.md).

## Requisitos

- Node.js 22.12 o superior compatible con Vite 7.
- pnpm 10.24.0, versión indicada en `package.json`.
- Backend disponible para usar los formularios y los datos reales.

Los comandos siguientes se ejecutan desde `frontend/`, salvo indicación contraria.

## Configuración inicial

Desde la raíz del repositorio:

```sh
cd frontend
pnpm install
cp .env.example .env
```

Si ya tenés `.env`, conservá su configuración. La variable pública necesaria es:

```dotenv
PUBLIC_API_URL=http://localhost:8000
```

Debe apuntar al backend. Si no se configura, el cliente usa `http://localhost:8000`.
Las variables `PUBLIC_*` son visibles en el navegador; no contienen secretos.
Después de cambiar `.env`, reiniciá el servidor de desarrollo o generá un nuevo build.

Para desarrollo, el backend debe permitir `http://localhost:5173` en su variable
`frontend_url`. Usá el mismo hostname al abrir el sitio: `127.0.0.1` es otro origen.

## Desarrollo

Con la API y PostgreSQL en marcha, abrí otra terminal:

```sh
pnpm dev --open
```

El sitio estará normalmente en <http://localhost:5173>. Si Vite elige otro puerto,
actualizá también `frontend_url` en el backend y reiniciá la API.

| Ruta                        | Contenido                                        |
| --------------------------- | ------------------------------------------------ |
| `/`                         | Inicio                                           |
| `/asociarse`                | Alta y consentimiento de privacidad y newsletter |
| `/baja`                     | Baja mediante email y documento                  |
| `/actividades`              | Listado público de actividades                   |
| `/actividades/[slug]`       | Detalle de una actividad                         |
| `/login`                    | Acceso al panel                                  |
| `/admin`                    | Personas asociadas; requiere rol admin           |
| `/admin/actividades`        | Listado y eliminación de actividades             |
| `/admin/actividades/nueva`  | Creación de actividades; requiere rol admin      |
| `/admin/actividades/[slug]` | Edición de actividades                           |
| `/privacidad`               | Política de privacidad                           |

El login conserva el token en `sessionStorage`, por pestaña, y lo envía a la API
como Bearer token. El backend controla la vigencia de la sesión y los permisos;
el panel requiere un usuario previamente creado en la base. Para crear el primer
administrador o autenticarte en Swagger, consultá la sección
[Acceso al panel del backend](../backend/README.md#acceso-al-panel).

Los formularios muestran éxito cuando la API confirma la operación y conservan los
datos si falla el envío. Recibir newsletters es opcional al asociarse. El envío
automático de correos todavía no está implementado en el backend.

## Chequeos y pruebas

```sh
pnpm check
pnpm lint
pnpm test
```

- `check`: sincroniza SvelteKit y comprueba Svelte y TypeScript.
- `lint`: revisa el formato con Prettier y luego ejecuta ESLint.
- `test`: ejecuta Vitest una vez, con pruebas de lógica en Node.js y de componentes
  en Chromium mediante Playwright. Las pruebas de formularios simulan la API.

Instalá Chromium para Playwright antes de la primera ejecución:

```sh
pnpm exec playwright install chromium
```

Para dejar los tests en modo observación, usá `pnpm test:unit`. Para formatear el
proyecto con Prettier, usá `pnpm format`.

## Build y vista previa

```sh
pnpm build
pnpm preview --host localhost
```

El build estático se genera en `build/`. La vista previa usa normalmente el puerto
`4173`; para probar operaciones contra la API desde allí, configurá
`frontend_url=http://localhost:4173` en el backend y reinicialo.

El adaptador es `@sveltejs/adapter-static`, con `index.html` como fallback y SSR
desactivado. Los formularios llaman a la API desde el navegador; no usan acciones
de servidor de SvelteKit.

## Despliegue en Netlify

La configuración está en [netlify.toml](../netlify.toml), en la raíz del repositorio:

- Directorio base: `frontend`.
- Comando de build: `pnpm run build`.
- Directorio publicado: `build`.
- Fallback de rutas: `/*` → `/index.html` con estado `200`.

Definí `PUBLIC_API_URL` con la URL HTTPS del backend antes de generar el build.
El backend se despliega por separado y debe configurar `frontend_url` con el origen
público del sitio. El fallback permite abrir directamente rutas como `/actividades/slug`
o `/admin`.

## Tipos de OpenAPI

Con el backend en marcha, podés generar tipos TypeScript a partir de su esquema:

```sh
pnpm exec openapi-typescript http://localhost:8000/openapi.json \
  --output src/lib/api/generated.ts
```

Este paso es opcional: el cliente actual usa los tipos definidos en el repositorio.

## Estructura

```text
src/
├── lib/
│   ├── api/             # Cliente HTTP, token y manejo de errores
│   ├── components/      # Navegación, editor de actividades y componentes UI
│   ├── schemas/         # Validación de formularios con Zod
│   ├── types/           # Tipos de datos
│   ├── stores/          # Estado del tema visual
│   ├── styles/          # Tema y Tailwind CSS
│   ├── query/           # Configuración de TanStack Query
│   └── mocks/           # Datos de ejemplo; las pantallas usan la API
└── routes/              # Páginas, cargas de datos y layout del panel
```

Las pruebas están junto a los archivos que verifican, con extensión `.spec.ts`.

## Problemas frecuentes

- **No se pudo conectar con el servidor:** comprobá `PUBLIC_API_URL`, que la API
  esté levantada y que PostgreSQL esté disponible.
- **Error de CORS:** revisá `frontend_url` en el backend y el origen real del navegador.
- **Sesión vencida:** volvé a iniciar sesión. La API rechaza tokens vencidos y
  usuarios desactivados.
- **Error 403:** el usuario no tiene permiso para esa operación; el rol editor
  no puede crear actividades ni consultar personas asociadas.
- **Playwright no encuentra Chromium:** ejecutá el comando de instalación indicado
  en la sección de pruebas.

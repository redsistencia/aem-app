# Argentinxs en Mallorca — Frontend

Frontend del sitio web de **Argentinxs en Mallorca**, SPA construido con **SvelteKit + TypeScript**.

---

## Stack

- **SvelteKit**
- **TypeScript**
- **Vite**
- **pnpm**
- **ESLint + Prettier**
- **Vitest** (unit + component testing)
- **Playwright** (para component testing)
- **zod** (para validación de formularios)
- **@tanstack/svelte-query** (para conectarse al backend)
- **lucide-svelte** (para íconos)
- **openapi-ts** (para documentación de la API)
- **shadcn-svelte** + **tailwindcss** (para componentes diseñados)

---

## 📋 Requisitos

```txt
Node.js: >= 22.12 (22 o 24 recomendado)
pnpm:    >= 10.24.0
```

Dentro del directorio /frontend

## Copiar el archivo .env

cp .env.example .env

## Instalar librerías

```sh
pnpm install

```

## Chequear inconsistencias de svelte

```sh
pnpm svelte-check

```

## Levantar el servidor de desarrollo

```sh
pnpm run dev -- --open
```

## Building

```sh
pnpm run build
```

## Testing

Instalar navegadores para Playwright (una sola vez)

```sh
pnpm dlx playwright install
```

```sh
pnpm test
```

## Open API

Generar open api

```sh
pnpm openapi-typescript <http://localhost:8000/openapi.json> \
  --output src/lib/api/generated.ts
```

## Arquitectura

src/
├─ lib/
│  ├─ components/     # Componentes reutilizables
│  ├─ stores/         # Stores globales (theme, etc.)
│  ├─ styles/         # Theme y estilos globales
│  └─ utils/          # Helpers
│  ├─ api/            # fetchers
│  ├─ query/          # svelte-query hooks
│  ├─ schemas/        # zod schemas
├─ routes/
│  ├─ +layout.svelte  # Layout principal
│  ├─ +page.svelte    # Home
│  ├─ asociarse/      # Formulario de asociación
│  └─ login/          # Acceso admin

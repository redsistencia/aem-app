# Argentinxs en Mallorca — Frontend

Frontend del sitio web de **Argentinxs en Mallorca**, construido con **SvelteKit + TypeScript**.

Este frontend se encarga únicamente de:

- la interfaz de usuario
- navegación
- validaciones en cliente
- consumo de la API backend

**No maneja autenticación ni base de datos** (eso vive en el backend Python).

---

## Stack

- **SvelteKit**
- **TypeScript**
- **Vite**
- **pnpm**
- **ESLint + Prettier**
- **Vitest** (unit + component testing)
- **Playwright** (para component testing)

---

## 📋 Requisitos

```txt
Node.js: >= 22.12 (22 o 24 recomendado)
pnpm:    >= 10.24.0
```

Dentro del directorio /frontend

## Instalar librerías

```sh
pnpm install

```

## Levantar el servidor de desarrollo

```sh
npm run dev -- --open
```

## Building

```sh
npm run build
```

## Testing

Instalar navegadores para Playwright (una sola vez)

```sh
pnpm dlx playwright install
```

```sh
pnpm test
```

## Arquitectura

src/
├─ lib/
│  ├─ components/     # Componentes reutilizables
│  ├─ stores/         # Stores globales (theme, etc.)
│  ├─ styles/         # Theme y estilos globales
│  └─ utils/          # Helpers
├─ routes/
│  ├─ +layout.svelte  # Layout principal
│  ├─ +page.svelte    # Home
│  ├─ asociarse/      # Formulario de asociación
│  └─ login/          # Acceso admin

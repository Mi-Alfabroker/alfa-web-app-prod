# Frontend Architecture

## Overview

This document describes the architecture of the Alfabroker Admin Frontend, built with **SvelteKit** and **Tailwind CSS**. The architecture follows clean code principles, emphasizing separation of concerns, single responsibility, and maintainability.

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| SvelteKit | 2.x | Full-stack framework with SSR/SPA capabilities |
| Svelte | 4.x | Reactive UI framework |
| Tailwind CSS | 3.x | Utility-first CSS framework |
| TypeScript | 5.x | Type safety and developer experience |
| Vite | 5.x | Build tool and dev server |
| Node.js | 20.x | Runtime environment |

## Directory Structure

```
src/
├── lib/                    # Shared library code
│   ├── components/         # Reusable UI components
│   ├── config/             # Application configuration
│   ├── services/           # API communication layer
│   ├── stores/             # Global state management
│   ├── types/              # TypeScript type definitions
│   └── utils/              # Utility functions
├── routes/                 # SvelteKit file-based routing
├── app.css                 # Global styles with Tailwind
└── app.html                # HTML template
```

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                        ROUTES (Pages)                        │
│                    src/routes/+page.svelte                   │
├─────────────────────────────────────────────────────────────┤
│                        COMPONENTS                            │
│               src/lib/components/*.svelte                    │
├─────────────────────────────────────────────────────────────┤
│                         STORES                               │
│                   src/lib/stores/*.ts                        │
├─────────────────────────────────────────────────────────────┤
│                        SERVICES                              │
│                  src/lib/services/*.ts                       │
├─────────────────────────────────────────────────────────────┤
│                          TYPES                               │
│                   src/lib/types/*.ts                         │
└─────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Routes (`src/routes/`)

SvelteKit's file-based routing system. Each route is a page in the application.

```
routes/
├── +layout.svelte      # Root layout (wraps all pages)
├── +page.svelte        # Home page (/)
├── aseguradoras/
│   ├── +page.svelte    # List page (/aseguradoras)
│   └── [id]/
│       └── +page.svelte # Detail page (/aseguradoras/123)
└── clientes/
    └── +page.svelte    # Clients page (/clientes)
```

**Responsibilities:**
- Page composition and layout
- Route-specific data loading
- Navigation handling

### 2. Components (`src/lib/components/`)

Reusable UI components following the single responsibility principle.

| Component | Purpose |
|-----------|---------|
| `Button.svelte` | Styled button with variants (primary, secondary, danger, ghost) |
| `Card.svelte` | Container component with shadow and border |
| `Loading.svelte` | Loading spinner (inline and fullscreen) |
| `Notifications.svelte` | Toast notification system |

**Usage Pattern:**
```svelte
<script>
  import { Button, Card } from '$components';
</script>

<Card>
  <h2>Title</h2>
  <Button variant="primary" on:click={handleClick}>
    Click me
  </Button>
</Card>
```

### 3. Stores (`src/lib/stores/`)

Svelte stores for global state management. Follows the Observer pattern.

| Store | Purpose |
|-------|---------|
| `loading` | Global loading state with `withLoading()` helper |
| `notifications` | Toast notification queue with auto-dismiss |

**Usage Pattern:**
```typescript
import { loading, withLoading } from '$stores';
import { addNotification } from '$stores';

// Wrap async operations
const data = await withLoading(() => fetchData());

// Show notifications
addNotification({ type: 'success', message: 'Saved!' });
```

### 4. Services (`src/lib/services/`)

API communication layer. Implements the **Information Expert** principle - services know how to communicate with their respective API endpoints.

```
services/
├── api.ts                    # Base HTTP client (ApiService)
├── aseguradora.service.ts    # Aseguradora-specific operations
└── index.ts                  # Barrel export
```

**ApiService Class:**
```typescript
class ApiService {
  async get<T>(endpoint: string): Promise<T>
  async post<T>(endpoint: string, data?: unknown): Promise<T>
  async put<T>(endpoint: string, data?: unknown): Promise<T>
  async patch<T>(endpoint: string, data?: unknown): Promise<T>
  async delete<T>(endpoint: string): Promise<T>
}
```

**Domain Service Pattern:**
```typescript
// aseguradora.service.ts
export const aseguradoraService = {
  getAll(): Promise<Aseguradora[]>,
  getById(id: number): Promise<Aseguradora>,
  create(data: CreateAseguradoraDto): Promise<Aseguradora>,
  update(id: number, data: UpdateAseguradoraDto): Promise<Aseguradora>,
  delete(id: number): Promise<void>
};
```

### 5. Types (`src/lib/types/`)

TypeScript interfaces and type definitions for type safety.

```
types/
├── index.ts           # Common types (ApiResponse, PaginatedResponse, etc.)
└── aseguradora.ts     # Domain-specific types
```

**Type Hierarchy:**
```typescript
// Base entity with common fields
interface BaseEntity {
  id: number;
  createdAt?: string;
  updatedAt?: string;
}

// Domain entity extends base
interface Aseguradora extends BaseEntity {
  nombre: string;
  codigo?: string;
  activo: boolean;
}

// DTOs for create/update operations
interface CreateAseguradoraDto { ... }
interface UpdateAseguradoraDto { ... }
```

### 6. Utils (`src/lib/utils/`)

Pure utility functions with no side effects.

| Module | Functions |
|--------|-----------|
| `formatters.ts` | `formatDate()`, `formatDateTime()`, `formatCurrency()` |
| `timing.ts` | `debounce()`, `throttle()` |

## Path Aliases

Configured in `svelte.config.js` and `tsconfig.json`:

| Alias | Path |
|-------|------|
| `$lib` | `src/lib` |
| `$components` | `src/lib/components` |
| `$services` | `src/lib/services` |
| `$stores` | `src/lib/stores` |
| `$types` | `src/lib/types` |
| `$utils` | `src/lib/utils` |

## Configuration

### Environment Variables

Managed through Vite's env system. Variables prefixed with `VITE_` are exposed to the client.

```typescript
// src/lib/config/index.ts
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
export const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT;
```

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:5000` |
| `VITE_API_TIMEOUT` | Request timeout (ms) | `30000` |

## Styling Architecture

### Tailwind CSS Layers

```css
/* app.css */
@tailwind base;       /* Reset and base styles */
@tailwind components; /* Reusable component classes */
@tailwind utilities;  /* Utility classes */

@layer components {
  .btn { ... }        /* Custom button styles */
  .card { ... }       /* Custom card styles */
  .input { ... }      /* Custom input styles */
}
```

### Design Tokens

Custom colors defined in `tailwind.config.js`:

```javascript
colors: {
  primary: {
    50: '#eff6ff',
    // ... shades 100-950
  },
  secondary: {
    50: '#f8fafc',
    // ... shades 100-950
  }
}
```

## Docker Architecture

### Multi-Stage Dockerfile

```dockerfile
# Build stage - compiles TypeScript and bundles assets
FROM node:20-alpine AS builder

# Production stage - minimal runtime image
FROM node:20-alpine AS production

# Development stage - with hot reload
FROM node:20-alpine AS development
```

### Network Configuration

The frontend container connects to the shared `alfabroker_network`:

```yaml
# docker-compose.yml
networks:
  alfabroker_network:
    external: true  # Created by docker-compose-db.yml
```

**Container Communication:**
```
┌─────────────────────────────────────────────────────────────┐
│                    alfabroker_network                        │
├─────────────────┬─────────────────┬─────────────────────────┤
│   alfabroker-   │   alfabroker-   │      alfabroker-        │
│    frontend     │    backend      │          db             │
│   (port 3000)   │   (port 5000)   │      (port 5432)        │
└─────────────────┴─────────────────┴─────────────────────────┘
```

## Design Principles Applied

### 1. Single Responsibility Principle (SRP)
- Each service handles one domain (e.g., `aseguradoraService`)
- Each component has one purpose (e.g., `Button`, `Card`)
- Stores are focused on specific state concerns

### 2. Information Expert (GRASP)
- Services contain API knowledge for their domain
- Components manage their own presentation logic
- Stores handle their specific state mutations

### 3. Low Coupling
- Services depend on abstract `ApiService`, not fetch directly
- Components communicate via props and events
- Stores are independent and composable

### 4. High Cohesion
- Related functionality grouped in modules
- Barrel exports (`index.ts`) provide clean APIs
- Types co-located with their domain

## Adding New Features

### Adding a New Domain (e.g., Clientes)

1. **Create types:**
   ```typescript
   // src/lib/types/cliente.ts
   export interface Cliente extends BaseEntity { ... }
   ```

2. **Create service:**
   ```typescript
   // src/lib/services/cliente.service.ts
   export const clienteService = { ... };
   ```

3. **Create route:**
   ```
   src/routes/clientes/+page.svelte
   ```

4. **Update barrel exports:**
   ```typescript
   // src/lib/types/index.ts
   export * from './cliente';
   
   // src/lib/services/index.ts
   export { clienteService } from './cliente.service';
   ```

### Adding a New Component

1. Create component in `src/lib/components/`
2. Export from `src/lib/components/index.ts`
3. Use via `import { NewComponent } from '$components'`

## Testing Strategy (Future)

```
tests/
├── unit/           # Component and utility tests
├── integration/    # Service and store tests
└── e2e/            # End-to-end tests with Playwright
```

## Performance Considerations

- **Code Splitting**: SvelteKit automatically splits routes
- **Lazy Loading**: Use dynamic imports for heavy components
- **Caching**: API responses can be cached in stores
- **Preloading**: SvelteKit preloads links on hover

---

*Last updated: January 2026*

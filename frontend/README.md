# Alfabroker Admin Frontend

Frontend de administración para Alfabroker, desarrollado con SvelteKit y Tailwind CSS.

## 🛠️ Tech Stack

- **Framework**: SvelteKit 2.x
- **Styling**: Tailwind CSS 3.x
- **Language**: TypeScript
- **Build Tool**: Vite 5.x
- **Runtime**: Node.js 20

## 📁 Project Structure

```
src/
├── lib/
│   ├── components/     # Reusable UI components
│   ├── config/         # App configuration
│   ├── services/       # API services
│   ├── stores/         # Svelte stores (state management)
│   ├── types/          # TypeScript type definitions
│   └── utils/          # Utility functions
├── routes/             # SvelteKit routes (pages)
├── app.css             # Global styles with Tailwind
└── app.html            # HTML template
```

## 🚀 Getting Started

### Prerequisites

- Node.js 20+
- npm or pnpm
- Docker (optional, for containerized development)

### Local Development

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment variables**:
   ```bash
   cp _env .env
   # Edit .env with your values
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Open browser**: http://localhost:3000

### Docker Development

1. **Ensure the network exists** (from project root):
   ```bash
   docker-compose -f docker-compose-db.yml up -d
   ```

2. **Start the frontend container**:
   ```bash
   cd frontend
   docker-compose up -d
   ```

3. **Open browser**: http://localhost:3000

## 📜 Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run check` | Run TypeScript/Svelte checks |

## 🌐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:5000` |
| `VITE_API_TIMEOUT` | API request timeout (ms) | `30000` |
| `NODE_ENV` | Environment mode | `development` |

## 🏗️ Architecture

### Services Layer
Services handle all API communication using a centralized `ApiService` class:

```typescript
import { aseguradoraService } from '$lib/services';

const aseguradoras = await aseguradoraService.getAll();
```

### Stores (State Management)
Svelte stores manage global state:

- `loading`: Global loading state
- `notifications`: Toast notification system

### Components
Reusable UI components with Tailwind styling:

- `Button`: Styled button with variants
- `Card`: Container component
- `Loading`: Loading spinner
- `Notifications`: Toast notifications

## 🐳 Docker

The frontend runs in a Docker container connected to the `alfabroker_network`:

- **Development**: Uses `target: development` with hot reload
- **Production**: Uses `target: production` with optimized build

## 📝 License

Private - Alfabroker

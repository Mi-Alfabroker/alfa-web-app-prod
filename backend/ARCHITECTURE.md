# Alfa-Broker Architecture

## Overview

**Alfa-Broker** is a proposal generation system for an insurance agency. The application enables the creation, management, and delivery of insurance proposals to clients by integrating with multiple insurance providers.

## System Architecture

The application follows a **Layered Architecture** pattern with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer                              │
│                    (Blueprints)                             │
│  ┌─────────┐  ┌──────────────┐  ┌───────────┐  ┌────────┐  │
│  │ health  │  │   clientes   │  │aseguradoras│  │propuestas│ │
│  └────┬────┘  └──────┬───────┘  └─────┬─────┘  └────┬───┘  │
└───────┼──────────────┼────────────────┼─────────────┼──────┘
        │              │                │             │
        ▼              ▼                ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                      │
│                      (Services)                             │
│              ┌──────────────┐  ┌───────────┐  ┌───────────┐ │
│              │   clientes   │  │aseguradoras│  │propuestas │ │
│              └──────┬───────┘  └─────┬─────┘  └─────┬─────┘ │
└─────────────────────┼────────────────┼─────────────┼────────┘
                      │                │             │
                      ▼                ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Access Layer                         │
│                    (Repositories)                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Domain Layer                            │
│                      (Models)                               │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
app/
├── __init__.py              # Flask app factory
├── blueprints/              # API Layer - HTTP endpoints
│   ├── __init__.py
│   ├── health.py            # Health check endpoint
│   ├── clientes.py          # Client management endpoints
│   ├── aseguradoras.py      # Insurance providers endpoints
│   └── propuestas.py        # Proposal generation endpoints
│
├── services/                # Business Logic Layer
│   ├── clientes/            # Client business logic
│   ├── aseguradoras/        # Insurance providers logic & integrations
│   └── propuestas/          # Proposal generation & processing
│
├── repositories/            # Data Access Layer
│   └── ...                  # Database operations
│
└── models/                  # Domain Layer
    └── ...                  # Entity definitions
```

## Layer Responsibilities

### 1. Blueprints (API Layer)
- Handle HTTP requests/responses
- Input validation and serialization
- Route definitions
- **Call corresponding service modules**
- No business logic here

### 2. Services (Business Logic Layer)
- Core business rules and workflows
- Orchestration of operations
- External integrations (insurance provider APIs)
- Each domain has its own service folder

### 3. Repositories (Data Access Layer)
- Database CRUD operations
- Query building
- Data persistence abstraction

### 4. Models (Domain Layer)
- Entity definitions
- Domain objects
- Data structures

## Data Flow

```
HTTP Request
     │
     ▼
Blueprint (validates input, extracts data)
     │
     ▼
Service (executes business logic)
     │
     ▼
Repository (persists/retrieves data)
     │
     ▼
Model (domain entity)
```

## Business Domains

### Clientes (Clients)
Management of insurance agency clients:
- Client registration and profiles
- Contact information
- Insurance history

### Aseguradoras (Insurance Providers)
Integration with insurance companies:
- Provider catalog
- API integrations for quotes
- Product/coverage information

### Propuestas (Proposals)
Core functionality - proposal generation:
- Create proposals based on client needs
- Request quotes from multiple providers
- Compare and present options
- Track proposal status

## Design Principles

This project follows the **Hierarchy of Design** approach:

1. **Kent Beck's 4 Rules** - Simple, expressive code first
2. **SOLID + GRASP** - When complexity grows
3. **GoF Patterns** - Only when the problem demands it

Key principles applied:
- **SRP**: Each layer has a single responsibility
- **Low Coupling**: Layers communicate through defined interfaces
- **Information Expert**: Logic lives where the data is

## Running the Application

```bash
# Development
docker-compose up -d --build

# Health check
curl http://localhost:5000/health
```

## Tech Stack

- **Python 3.11**
- **Flask** - Web framework
- **Docker** - Containerization
- **Network**: `alfabroker_network`

## Authentication and RBAC

The API now includes token-based authentication and role-based access control.

- Public endpoints:
     - `GET /health`
     - `GET /health/db`
     - `GET /health/full`
     - `POST /api/auth/login`
     - `POST /api/auth/refresh`
- Protected endpoint:
     - `GET /api/auth/me`

### Roles

- `SUPERADMIN` and `ADMINISTRADOR`: administrative access
- `AGENTE`: operational access
- `CLIENTE`: authenticated but restricted from panel operations

### Initial Authorization Matrix

- `/api/aseguradoras`
     - `GET`: `AGENTE`, `ADMINISTRADOR`, `SUPERADMIN`
     - `POST/PUT/DELETE`: `ADMINISTRADOR`, `SUPERADMIN`
- `/api/usuarios`
     - `GET`: `AGENTE`, `ADMINISTRADOR`, `SUPERADMIN`
     - `POST/PUT/DELETE`: `ADMINISTRADOR`, `SUPERADMIN`
- `/api/bienes`
     - `GET/POST/PUT`: `AGENTE`, `ADMINISTRADOR`, `SUPERADMIN`
     - `DELETE`: `ADMINISTRADOR`, `SUPERADMIN`
- `/api/polizas`
     - `GET/POST/PUT/PATCH`: `AGENTE`, `ADMINISTRADOR`, `SUPERADMIN`
     - `DELETE`: `ADMINISTRADOR`, `SUPERADMIN`
- `/api/propuestas`
     - `GET/POST`: `AGENTE`, `ADMINISTRADOR`, `SUPERADMIN`

## Auth Error Contract (401/403)

All authentication/authorization failures follow this payload:

```json
{
     "success": false,
     "error": {
          "code": "AUTH_UNAUTHORIZED",
          "message": "Authentication required"
     }
}
```

Rules:

- `401` with code `AUTH_UNAUTHORIZED`:
     - Missing bearer token
     - Invalid/expired token
     - Invalid credentials at login
- `403` with code `AUTH_FORBIDDEN`:
     - Authenticated user lacks required role

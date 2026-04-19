# Micro-SaaS Platform

A full-stack, robust, production-ready Micro-SaaS platform. This project is built using a modern architecture, utilizing a **Vue 3 + Vite** frontend and a **FastAPI + PostgreSQL + Redis** backend.

It is designed with scale and security in mind, demonstrating professional software engineering practices including role-based access control, caching, background task processing, and responsive modern web design.

## Architecture Overview

This platform is divided into two main sub-projects:

- **[Frontend](./frontend/README.md):** A responsive, lightning-fast Single Page Application (SPA) built with Vue 3 (Composition API), Vite, Pinia for state management, and Vue Router for routing. 
- **[Backend](./backend/README.md):** A high-performance Python backend built with FastAPI, utilizing asyncpg for asynchronous PostgreSQL interactions, SQLAlchemy 2.0 as the ORM, and Redis with ARQ for background tasks and distributed caching.

## Key System Features

- **Granular Role-Based Access Control (RBAC):** Comprehensive permission definitions for `ADMIN` and `USER` roles throughout the application.
- **Robust Authentication flows:** JWT-based stateless authentication with secure refresh tokens and email verification.
- **Enterprise-Grade Data Integrity:** Implementations of soft deletes on critical models (users, orgs) preserving historical references and audit logs.
- **High-Performance Architecture:** Redis-backed distributed rate limiting and caching. Asynchronous execution from the API down to the database level.
- **Seamless User Experience:** Silent token refreshes, dynamic SEO rendering, and rich state-driven loading screens using Pinia.

## Getting Started

To spin up the entire application locally, you will need to start both the backend and frontend development servers.

### 1. Database & Infrastructure

Before running the application, ensure you have the following running locally:
- **PostgreSQL** Database 
- **Redis** Server (Used for caching and background tasks)

### 2. Backend Setup

Open a terminal and navigate to the `backend/` directory:

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # On Windows
# source .venv/bin/activate    # On Mac/Linux

pip install -r requirements.txt
```

Set up your environment variables by copying `.env.example` to `.env` and adjusting to match your local database and Redis paths. Then run migrations and start the server:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

*In a separate backend terminal, start the background worker:*
```bash
arq app.core.worker.WorkerSettings
```

*(For more details, see the [Backend README](./backend/README.md))*

### 3. Frontend Setup

Open a new terminal and navigate to the `frontend/` directory:

```bash
cd frontend
npm install
npm run dev
```

*(For more details, see the [Frontend README](./frontend/README.md))*

## Documentation

Once your backend is running, the interactive API documentation will be available at:
- **Swagger / OpenAPI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Testing

Both projects employ their own specific test suites. Make sure to run tests inside their respective directories:

- **Backend:** Uses `pytest` with `pytest-asyncio`. Run `pytest --cov=app tests/`.
- **Frontend:** Follow the tools in the frontend directory (e.g. Vitest if customized later).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
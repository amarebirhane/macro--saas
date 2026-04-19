# Micro-SaaS Platform - Backend

A robust, production-ready Micro-SaaS platform backend built with FastAPI, PostgreSQL, and Redis. It provides a secure, scalable, and high-performance foundation for building modern web applications.

## Key Features

- **FastAPI & Async PostgreSQL**: High-performance REST API with asynchronous database operations using SQLAlchemy 2.0 and asyncpg.
- **Robust Authentication**: JWT-based authentication with refresh token support, secure bcrypt password hashing, and email verification workflows.
- **Granular RBAC**: Comprehensive Role-Based Access Control allowing highly specific permission definitions for administrative and user roles.
- **Distributed Caching & Rate Limiting**: Redis integration for high-speed read caching and distributed rate limiting to protect endpoints against abuse.
- **Background Task Processing**: Asynchronous worker queues powered by ARQ (Redis) for handling heavy lifting like sending emails and processing image uploads without blocking the main API thread.
- **Audit Logging**: Comprehensive tracking of all administrative actions for compliance and monitoring.
- **Data Integrity**: Soft deletes for users and organizations to prevent accidental data loss.
- **Security First**: Comprehensive CORS policies, professional security headers middleware, and built-in protection against common vulnerabilities.

## Technology Stack

- **Framework**: FastAPI (Python 3.12+)
- **Database & ORM**: PostgreSQL, SQLAlchemy 2.0, Alembic (Migrations)
- **Caching & Queues**: Redis, ARQ, fastapi-cache2
- **Authentication**: PyJWT, passlib (bcrypt)
- **Validation**: Pydantic v2
- **Testing**: Pytest, httpx, pytest-asyncio
- **Formatting**: Black, Ruff

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL
- Redis Server

### Installation

1. **Clone the repository and navigate to backend**
   ```bash
   git clone <repository-url>
   cd Micro-SaaS/backend
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file based on `.env.example`. Key variables include:
   ```env
   DATABASE_URL="postgresql+asyncpg://user:password@host:port/dbname"
   REDIS_URL="redis://localhost:6379/0"
   SECRET_KEY="your-super-secret-jwt-key"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Database Initialization**
   Run Alembic migrations to set up your tables:
   ```bash
   alembic upgrade head
   ```

6. **Start the Application**
   Run the main API server locally:
   ```bash
   uvicorn app.main:app --reload
   ```
   Start the ARQ background worker (in a separate terminal):
   ```bash
   arq app.core.worker.WorkerSettings
   ```

## API Documentation

Once the server is running, interactive API documentation is automatically generated:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Testing

Ensure your test database URL is configured, then run:
```bash
pytest
```
To run tests with coverage:
```bash
pytest --cov=app tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
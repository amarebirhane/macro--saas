from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, users, admin
from app.core.config import settings
from app.core.database import init_db
from app.core.logging_config import setup_logging
from app.api.middleware import GlobalExceptionHandlerMiddleware

# Initialize Logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json"
)

# Add Middleware
app.add_middleware(GlobalExceptionHandlerMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
def root():
    return {
        "message": "Welcome to the Micro-SaaS API",
        "docs": "/docs",
        "version": "1.0.0"
    }

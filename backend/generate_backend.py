import os

base = r"c:\Users\ASHROCK\Desktop\Micro-SaaS\backend"

def write(path, content):
    os.makedirs(os.path.dirname(os.path.join(base, path)), exist_ok=True)
    with open(os.path.join(base, path), "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

write("requirements.txt", """
fastapi==0.110.0
uvicorn==0.28.0
sqlalchemy==2.0.28
pydantic==2.6.4
pydantic-settings==2.2.1
asyncpg==0.29.0
alembic==1.13.1
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.9
""")

write(".env", """
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/microsaas
SECRET_KEY=super_secret_jwt_key_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
""")

write("app/core/config.py", """
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Micro-SaaS API"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
""")

write("app/core/database.py", """
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
""")

write("app/models/user.py", """
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
from uuid import uuid4

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="USER", nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
""")

write("app/schemas/user.py", """
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserAdminUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
""")

write("app/schemas/auth.py", """
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
""")

write("app/utils/hashing.py", """
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
""")

write("app/core/security.py", """
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
""")

write("app/models/__init__.py", """
from app.models.user import User
""")

write("app/api/deps.py", """
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.schemas.auth import TokenData
from app.services.user_service import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except JWTError:
        raise credentials_exception
        
    user = await get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_role(required_role: str):
    async def role_checker(current_user = Depends(get_current_active_user)):
        if current_user.role != required_role and current_user.role != "ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not enough permissions"
            )
        return current_user
    return role_checker
""")

write("app/services/user_service.py", """
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserAdminUpdate
from app.utils.hashing import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def create_user(db: AsyncSession, user_in: UserCreate, initial_role="USER"):
    if await get_user_by_email(db, user_in.email):
        return None
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=initial_role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user: User, user_in: UserUpdate):
    for field, value in user_in.model_dump(exclude_unset=True).items():
        if field == "password":
            user.hashed_password = get_password_hash(value)
        else:
            setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user

async def admin_update_user(db: AsyncSession, user_id: str, user_in: UserAdminUpdate):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: str):
    user = await get_user_by_id(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
        return True
    return False
""")

write("app/services/auth_service.py", """
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import get_user_by_email
from app.utils.hashing import verify_password

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
""")

write("app/api/v1/endpoints/auth.py", """
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import authenticate_user
from app.services.user_service import create_user
from app.core.security import create_access_token
from app.api.deps import get_current_active_user

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, user_in)
    if not user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user
""")

write("app/api/v1/endpoints/users.py", """
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserOut, UserUpdate
from app.api.deps import get_current_active_user
from app.services.user_service import update_user

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_user_me(current_user = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserOut)
async def update_user_me(
    user_in: UserUpdate, 
    current_user = Depends(get_current_active_user), 
    db: AsyncSession = Depends(get_db)
):
    return await update_user(db, current_user, user_in)
""")

write("app/api/v1/endpoints/admin.py", """
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.user import UserOut, UserAdminUpdate
from app.api.deps import require_role
from app.services.user_service import get_all_users, admin_update_user, delete_user

router = APIRouter()

@router.get("/users", response_model=List[UserOut], dependencies=[Depends(require_role("ADMIN"))])
async def read_all_users(db: AsyncSession = Depends(get_db)):
    return await get_all_users(db)

@router.put("/users/{user_id}", response_model=UserOut, dependencies=[Depends(require_role("ADMIN"))])
async def update_user_by_admin(
    user_id: str, 
    user_in: UserAdminUpdate, 
    db: AsyncSession = Depends(get_db)
):
    user = await admin_update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", dependencies=[Depends(require_role("ADMIN"))])
async def delete_user_by_admin(user_id: str, db: AsyncSession = Depends(get_db)):
    success = await delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

@router.get("/analytics", dependencies=[Depends(require_role("ADMIN"))])
async def get_analytics(db: AsyncSession = Depends(get_db)):
    users = await get_all_users(db)
    return {
        "total_users": len(users),
        "active_users": len([u for u in users if u.is_active]),
        "admins": len([u for u in users if u.role == "ADMIN"]),
        "regular_users": len([u for u in users if u.role == "USER"])
    }
""")

write("app/api/v1/api.py", """
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
""")

write("app/main.py", """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import Base, engine

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Only for development without alembic. 
    # Use alembic for production migrations!
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Micro-SaaS API",
        "docs": "/docs",
    }
""")

print("Successfully generated backend codebase.")

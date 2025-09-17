"""
Authentication module using Prisma ORM
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from pydantic import BaseModel
from .database_prisma import get_db
from .models_prisma import UserCreate, UserLogin, UserResponse

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()

router = APIRouter()

# Token response model
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user_by_username(prisma, username: str):
    """Get user by username"""
    return await prisma.user.find_unique(where={"username": username})

async def get_user_by_email(prisma, email: str):
    """Get user by email"""
    return await prisma.user.find_unique(where={"email": email})

async def authenticate_user(prisma, username: str, password: str):
    """Authenticate user with username and password"""
    user = await get_user_by_username(prisma, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    prisma = Depends(get_db)
):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_username(prisma, username=username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate, prisma = Depends(get_db)):
    """User signup endpoint"""
    # Check if user already exists
    existing_user = await get_user_by_username(prisma, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    existing_email = await get_user_by_email(prisma, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = await prisma.user.create(
        data={
            "username": user_data.username,
            "email": user_data.email,
            "password": hashed_password
        }
    )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**db_user.dict())
    }

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, prisma = Depends(get_db)):
    """User login endpoint"""
    user = await authenticate_user(prisma, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(**user.dict())
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(**current_user.dict())

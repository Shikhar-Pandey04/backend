from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from contextlib import asynccontextmanager

from .database_prisma import connect_db, disconnect_db, get_db
from .auth_prisma import get_current_user
from .routes.contracts_prisma import router as contracts_router
from .routes.upload_prisma import router as upload_router
from .routes.query_prisma import router as query_router
from .models_prisma import UserResponse

# Lifespan event handler for database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting up the application...")
    await connect_db()
    yield
    # Shutdown
    print("🔄 Shutting down the application...")
    await disconnect_db()

app = FastAPI(
    title="Contract Management SaaS",
    description="A full-stack SaaS prototype for contract management with AI-powered insights",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Auth routes
from .auth_prisma import router as auth_router
app.include_router(auth_router, prefix="/auth", tags=["authentication"])

# API routes
app.include_router(contracts_router, prefix="/api", tags=["contracts"])
app.include_router(upload_router, prefix="/api", tags=["upload"])
app.include_router(query_router, prefix="/api", tags=["query"])

@app.get("/")
async def root():
    return {"message": "Contract Management SaaS API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Contract Management SaaS",
    description="A simple backend for testing login functionality",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple models
class UserLogin(BaseModel):
    username: str
    password: str

class UserSignup(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

# Mock user storage (in real app, this would be in database)
mock_users = {
    "demo": {
        "username": "demo",
        "email": "demo@example.com",
        "password": "demo123"  # In real app, this would be hashed
    }
}

@app.get("/")
async def root():
    return {"message": "Contract Management SaaS API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/auth/login")
async def login(user_data: UserLogin):
    """User login endpoint"""
    username = user_data.username
    password = user_data.password
    
    # Check if user exists and password matches
    if username in mock_users and mock_users[username]["password"] == password:
        return {
            "access_token": f"mock_token_{username}",
            "token_type": "bearer",
            "user": {
                "username": username,
                "email": mock_users[username]["email"]
            }
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

@app.post("/auth/signup")
async def signup(user_data: UserSignup):
    """User signup endpoint"""
    username = user_data.username
    email = user_data.email
    password = user_data.password
    
    # Check if user already exists
    if username in mock_users:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Add new user
    mock_users[username] = {
        "username": username,
        "email": email,
        "password": password  # In real app, this would be hashed
    }
    
    return {
        "access_token": f"mock_token_{username}",
        "token_type": "bearer",
        "user": {
            "username": username,
            "email": email
        }
    }

@app.get("/api/contracts")
async def get_contracts():
    """Mock contracts endpoint"""
    return {
        "contracts": [
            {
                "id": "1",
                "title": "Sample Contract 1",
                "status": "active",
                "createdAt": "2024-01-01T00:00:00Z"
            },
            {
                "id": "2", 
                "title": "Sample Contract 2",
                "status": "draft",
                "createdAt": "2024-01-02T00:00:00Z"
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run("app.main_simple:app", host="127.0.0.1", port=8000, reload=True)

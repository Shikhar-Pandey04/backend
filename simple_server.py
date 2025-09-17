from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# CORS middleware - VERY IMPORTANT for frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UserLogin(BaseModel):
    username: str
    password: str

class UserSignup(BaseModel):
    username: str
    email: str
    password: str

# Mock users
users = {
    "demo": {"username": "demo", "email": "demo@example.com", "password": "demo123"}
}

@app.get("/")
async def root():
    return {"message": "Backend is running!"}

@app.get("/api/contracts")
async def get_contracts():
    """Mock contracts endpoint"""
    return {
        "documents": [
            {
                "doc_id": "1",
                "contract_name": "Master Service Agreement",
                "parties": "Acme Corp, TechStart Inc",
                "expiry_date": "2024-12-31",
                "status": "Active",
                "risk_score": "Low",
                "uploaded_on": "2024-01-01T00:00:00Z"
            },
            {
                "doc_id": "2", 
                "contract_name": "Non-Disclosure Agreement",
                "parties": "Global Solutions Ltd, Innovation Partners",
                "expiry_date": "2024-06-30",
                "status": "Renewal Due",
                "risk_score": "Medium",
                "uploaded_on": "2024-01-02T00:00:00Z"
            },
            {
                "doc_id": "3",
                "contract_name": "Software License Agreement",
                "parties": "Digital Dynamics, Client Corp",
                "expiry_date": "2024-03-15",
                "status": "Expired",
                "risk_score": "High",
                "uploaded_on": "2024-01-03T00:00:00Z"
            },
            {
                "doc_id": "4",
                "contract_name": "Employment Contract",
                "parties": "TechCorp, John Doe",
                "expiry_date": "2025-01-31",
                "status": "Active",
                "risk_score": "Low",
                "uploaded_on": "2024-01-04T00:00:00Z"
            },
            {
                "doc_id": "5",
                "contract_name": "Vendor Agreement",
                "parties": "Supply Chain Ltd, Manufacturing Co",
                "expiry_date": "2024-08-15",
                "status": "Active",
                "risk_score": "Medium",
                "uploaded_on": "2024-01-05T00:00:00Z"
            }
        ],
        "total": 5,
        "page": 1,
        "per_page": 100
    }

@app.post("/api/upload")
async def upload_contract():
    """Mock upload endpoint"""
    return {
        "message": "File uploaded successfully",
        "contract_id": "mock_contract_123",
        "status": "success"
    }

@app.post("/api/query")
async def query_contracts():
    """Mock query endpoint"""
    return {
        "results": [
            {
                "id": "1",
                "title": "Sample Contract 1",
                "content": "This is a sample contract with termination clauses...",
                "relevance": 0.95
            }
        ],
        "total": 1,
        "query": "sample query"
    }

@app.get("/api/analytics")
async def get_analytics():
    """Mock analytics endpoint"""
    return {
        "total_contracts": 25,
        "active_contracts": 18,
        "expiring_soon": 3,
        "high_risk": 2,
        "monthly_uploads": [5, 8, 12, 15, 10, 8, 7],
        "risk_distribution": {
            "low": 15,
            "medium": 8,
            "high": 2
        }
    }

@app.get("/api/insights")
async def get_insights():
    """Mock insights endpoint"""
    return {
        "insights": [
            {
                "type": "risk",
                "title": "High Risk Contracts Detected",
                "description": "2 contracts have been flagged as high risk due to unfavorable terms",
                "severity": "high",
                "count": 2
            },
            {
                "type": "expiry",
                "title": "Contracts Expiring Soon",
                "description": "3 contracts are expiring within the next 30 days",
                "severity": "medium",
                "count": 3
            },
            {
                "type": "opportunity",
                "title": "Renewal Opportunities",
                "description": "5 contracts are eligible for renewal with better terms",
                "severity": "low",
                "count": 5
            }
        ]
    }

@app.get("/api/reports")
async def get_reports():
    """Mock reports endpoint"""
    return {
        "reports": [
            {
                "id": "1",
                "title": "Monthly Contract Summary",
                "type": "summary",
                "generated_at": "2024-01-15T10:30:00Z",
                "status": "ready"
            },
            {
                "id": "2",
                "title": "Risk Analysis Report",
                "type": "risk",
                "generated_at": "2024-01-14T15:45:00Z",
                "status": "ready"
            },
            {
                "id": "3",
                "title": "Compliance Audit",
                "type": "compliance",
                "generated_at": "2024-01-13T09:15:00Z",
                "status": "ready"
            }
        ]
    }

@app.post("/auth/login")
async def login(user_data: UserLogin):
    username = user_data.username
    password = user_data.password
    
    if username in users and users[username]["password"] == password:
        return {
            "access_token": f"token_{username}",
            "token_type": "bearer",
            "user": {
                "username": username,
                "email": users[username]["email"]
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/auth/signup")
async def signup(user_data: UserSignup):
    username = user_data.username
    
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    users[username] = {
        "username": username,
        "email": user_data.email,
        "password": user_data.password
    }
    
    return {
        "access_token": f"token_{username}",
        "token_type": "bearer",
        "user": {
            "username": username,
            "email": user_data.email
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Pydantic models for API requests/responses using Prisma
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Models
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    createdAt: datetime
    updatedAt: datetime

# Contract Models
class ContractCreate(BaseModel):
    title: str
    content: str
    status: Optional[str] = "draft"

class ContractUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None

class ContractResponse(BaseModel):
    id: str
    title: str
    content: str
    status: str
    filePath: Optional[str] = None
    fileSize: Optional[int] = None
    mimeType: Optional[str] = None
    userId: str
    createdAt: datetime
    updatedAt: datetime

# Contract Analysis Models
class ContractAnalysisCreate(BaseModel):
    contractId: str
    summary: Optional[str] = None
    keyTerms: List[str] = []
    risks: List[str] = []
    obligations: List[str] = []
    embedding: Optional[str] = None

class ContractAnalysisResponse(BaseModel):
    id: str
    contractId: str
    summary: Optional[str] = None
    keyTerms: List[str] = []
    risks: List[str] = []
    obligations: List[str] = []
    embedding: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

# Combined Models
class ContractWithAnalysis(ContractResponse):
    analysis: Optional[ContractAnalysisResponse] = None

# Query Models
class QueryRequest(BaseModel):
    query: str
    limit: Optional[int] = 10

class QueryResponse(BaseModel):
    results: List[ContractResponse]
    total: int
    query: str

# File Upload Models
class FileUploadResponse(BaseModel):
    message: str
    contract_id: str
    filename: str
    file_size: int

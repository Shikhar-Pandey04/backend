from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

# User schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Document schemas
class DocumentCreate(BaseModel):
    filename: str
    contract_name: Optional[str] = None
    parties: Optional[str] = None
    expiry_date: Optional[datetime] = None

class DocumentResponse(BaseModel):
    doc_id: UUID
    user_id: UUID
    filename: str
    original_filename: str
    file_size: Optional[int]
    file_type: Optional[str]
    uploaded_on: datetime
    contract_name: Optional[str]
    parties: Optional[str]
    expiry_date: Optional[datetime]
    status: str
    risk_score: str
    processing_status: str
    
    class Config:
        from_attributes = True

class DocumentList(BaseModel):
    documents: List[DocumentResponse]
    total: int
    page: int
    per_page: int

# Chunk schemas
class ChunkResponse(BaseModel):
    chunk_id: UUID
    doc_id: UUID
    text_chunk: str
    page_number: Optional[int]
    chunk_index: Optional[int]
    confidence_score: Optional[float]
    metadata: Optional[str]
    
    class Config:
        from_attributes = True

# Upload schemas
class UploadResponse(BaseModel):
    doc_id: UUID
    filename: str
    status: str
    message: str
    chunks_created: int

# Query schemas
class QueryRequest(BaseModel):
    question: str
    limit: Optional[int] = 5

class QueryResult(BaseModel):
    chunk_id: UUID
    doc_id: UUID
    text_chunk: str
    relevance_score: float
    page_number: Optional[int]
    contract_name: Optional[str]
    metadata: Optional[Dict[str, Any]]

class QueryResponse(BaseModel):
    question: str
    answer: str
    results: List[QueryResult]
    total_results: int

# Contract detail schemas
class ContractInsight(BaseModel):
    type: str  # "risk" or "recommendation"
    title: str
    description: str
    severity: Optional[str] = None

class ContractClause(BaseModel):
    title: str
    text: str
    confidence: float
    page_number: Optional[int]

class ContractDetail(BaseModel):
    document: DocumentResponse
    clauses: List[ContractClause]
    insights: List[ContractInsight]
    total_chunks: int

# Error schemas
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

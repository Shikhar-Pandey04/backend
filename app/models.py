from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    chunks = relationship("Chunk", back_populates="user", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"
    
    doc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(10))
    uploaded_on = Column(DateTime, default=datetime.utcnow)
    
    # Contract-specific fields
    contract_name = Column(String(255))
    parties = Column(Text)  # JSON string of parties involved
    expiry_date = Column(DateTime)
    status = Column(String(20), default="Active")  # Active, Renewal Due, Expired
    risk_score = Column(String(10), default="Low")  # Low, Medium, High
    
    # Processing status
    processing_status = Column(String(20), default="pending")  # pending, processing, completed, failed
    
    # Relationships
    user = relationship("User", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"
    
    chunk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id = Column(UUID(as_uuid=True), ForeignKey("documents.doc_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    text_chunk = Column(Text, nullable=False)
    embedding = Column(Vector(384))  # 384-dimensional vector for embeddings
    
    # Metadata
    page_number = Column(Integer)
    chunk_index = Column(Integer)
    confidence_score = Column(Float, default=0.0)
    
    # Additional metadata as JSON string
    chunk_metadata = Column(Text)  # JSON string for flexible metadata
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    user = relationship("User", back_populates="chunks")

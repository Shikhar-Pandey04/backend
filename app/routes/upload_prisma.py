"""
File upload routes using Prisma ORM
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Optional
import os
import uuid
from pathlib import Path

from ..database_prisma import get_db
from ..auth_prisma import get_current_user
from ..models_prisma import ContractResponse, FileUploadResponse

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload", response_model=FileUploadResponse)
async def upload_contract_file(
    file: UploadFile = File(...),
    title: Optional[str] = None,
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Upload a contract file and create a contract record"""
    
    # Validate file type
    allowed_types = ["application/pdf", "text/plain", "application/msword", 
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail="File type not supported. Please upload PDF, DOC, DOCX, or TXT files."
        )
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        # Save file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Extract text content (simplified for demo)
        if file.content_type == "text/plain":
            file_content = content.decode("utf-8")
        else:
            # For other file types, use filename as content for now
            file_content = f"Content extracted from {file.filename}"
        
        # Create contract record
        contract = await prisma.contract.create(
            data={
                "title": title or file.filename,
                "content": file_content,
                "status": "uploaded",
                "filePath": str(file_path),
                "fileSize": len(content),
                "mimeType": file.content_type,
                "userId": current_user.id
            }
        )
        
        return FileUploadResponse(
            message="File uploaded successfully",
            contract_id=contract.id,
            filename=file.filename,
            file_size=len(content)
        )
        
    except Exception as e:
        # Clean up file if database operation fails
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/upload/status/{contract_id}")
async def get_upload_status(
    contract_id: str,
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Get upload and processing status of a contract"""
    
    contract = await prisma.contract.find_unique(
        where={"id": contract_id}
    )
    
    if not contract or contract.userId != current_user.id:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    return {
        "contract_id": contract.id,
        "status": contract.status,
        "title": contract.title,
        "file_size": contract.fileSize,
        "mime_type": contract.mimeType,
        "uploaded_at": contract.createdAt
    }

"""
Contract routes using Prisma ORM
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
import json

from ..database_prisma import get_db
from ..auth_prisma import get_current_user
from ..models_prisma import (
    ContractCreate, ContractUpdate, ContractResponse, 
    ContractWithAnalysis, QueryRequest, QueryResponse
)

router = APIRouter()

@router.get("/contracts", response_model=List[ContractResponse])
async def get_contracts(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("createdAt"),
    sort_order: Optional[str] = Query("desc"),
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Get paginated list of contracts for current user"""
    
    # Build where clause
    where_clause = {"userId": current_user.id}
    
    # Apply search filter
    if search:
        where_clause["OR"] = [
            {"title": {"contains": search, "mode": "insensitive"}},
            {"content": {"contains": search, "mode": "insensitive"}}
        ]
    
    # Apply status filter
    if status_filter:
        where_clause["status"] = status_filter
    
    # Build order by clause
    order_by = {}
    if sort_by == "createdAt":
        order_by["createdAt"] = sort_order
    elif sort_by == "title":
        order_by["title"] = sort_order
    elif sort_by == "updatedAt":
        order_by["updatedAt"] = sort_order
    else:
        order_by["createdAt"] = "desc"
    
    # Get total count
    total = await prisma.contract.count(where=where_clause)
    
    # Apply pagination
    skip = (page - 1) * per_page
    contracts = await prisma.contract.find_many(
        where=where_clause,
        order_by=order_by,
        skip=skip,
        take=per_page
    )
    
    return [ContractResponse(**contract.dict()) for contract in contracts]

@router.get("/contracts/{contract_id}", response_model=ContractWithAnalysis)
async def get_contract_detail(
    contract_id: str,
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Get detailed information about a specific contract"""
    
    # Get contract with analysis
    contract = await prisma.contract.find_unique(
        where={"id": contract_id},
        include={"analysis": True}
    )
    
    if not contract or contract.userId != current_user.id:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    return ContractWithAnalysis(**contract.dict())

@router.post("/contracts", response_model=ContractResponse)
async def create_contract(
    contract_data: ContractCreate,
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Create a new contract"""
    
    contract = await prisma.contract.create(
        data={
            "title": contract_data.title,
            "content": contract_data.content,
            "status": contract_data.status,
            "userId": current_user.id
        }
    )
    
    return ContractResponse(**contract.dict())

@router.put("/contracts/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: str,
    contract_data: ContractUpdate,
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Update an existing contract"""
    
    # Check if contract exists and belongs to user
    existing_contract = await prisma.contract.find_unique(
        where={"id": contract_id}
    )
    
    if not existing_contract or existing_contract.userId != current_user.id:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Build update data
    update_data = {}
    if contract_data.title is not None:
        update_data["title"] = contract_data.title
    if contract_data.content is not None:
        update_data["content"] = contract_data.content
    if contract_data.status is not None:
        update_data["status"] = contract_data.status
    
    # Update contract
    contract = await prisma.contract.update(
        where={"id": contract_id},
        data=update_data
    )
    
    return ContractResponse(**contract.dict())

@router.delete("/contracts/{contract_id}")
async def delete_contract(
    contract_id: str,
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Delete a contract and all its analysis"""
    
    # Check if contract exists and belongs to user
    contract = await prisma.contract.find_unique(
        where={"id": contract_id}
    )
    
    if not contract or contract.userId != current_user.id:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Delete contract (analysis will be deleted due to cascade)
    await prisma.contract.delete(
        where={"id": contract_id}
    )
    
    return {"message": "Contract deleted successfully"}

@router.get("/contracts/{contract_id}/analysis")
async def get_contract_analysis(
    contract_id: str,
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Get AI analysis for a specific contract"""
    
    # Check if contract exists and belongs to user
    contract = await prisma.contract.find_unique(
        where={"id": contract_id}
    )
    
    if not contract or contract.userId != current_user.id:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    # Get analysis
    analysis = await prisma.contractanalysis.find_unique(
        where={"contractId": contract_id}
    )
    
    if not analysis:
        # Generate mock analysis if none exists
        mock_analysis = {
            "summary": "This is a standard service agreement with typical terms and conditions.",
            "keyTerms": ["Payment terms", "Termination clause", "Liability limitation", "Confidentiality"],
            "risks": ["Auto-renewal clause", "Limited liability cap", "Short termination notice"],
            "obligations": ["Monthly payments", "Service level maintenance", "Data protection compliance"]
        }
        return mock_analysis
    
    return {
        "summary": analysis.summary,
        "keyTerms": analysis.keyTerms,
        "risks": analysis.risks,
        "obligations": analysis.obligations
    }

@router.post("/contracts/search", response_model=QueryResponse)
async def search_contracts(
    query_data: QueryRequest,
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Search contracts using text query"""
    
    # Simple text search for now (can be enhanced with vector search later)
    contracts = await prisma.contract.find_many(
        where={
            "userId": current_user.id,
            "OR": [
                {"title": {"contains": query_data.query, "mode": "insensitive"}},
                {"content": {"contains": query_data.query, "mode": "insensitive"}}
            ]
        },
        take=query_data.limit,
        order_by={"createdAt": "desc"}
    )
    
    return QueryResponse(
        results=[ContractResponse(**contract.dict()) for contract in contracts],
        total=len(contracts),
        query=query_data.query
    )

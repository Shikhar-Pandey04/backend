"""
Query routes using Prisma ORM
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..database_prisma import get_db
from ..auth_prisma import get_current_user
from ..models_prisma import QueryRequest, QueryResponse, ContractResponse

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_contracts(
    query_data: QueryRequest,
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Query contracts using natural language"""
    
    # Simple text search implementation
    # In a real application, this would use vector embeddings and semantic search
    
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

@router.get("/query/suggestions")
async def get_query_suggestions(
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Get query suggestions based on user's contracts"""
    
    # Get user's contracts to generate suggestions
    contracts = await prisma.contract.find_many(
        where={"userId": current_user.id},
        take=5,
        order_by={"createdAt": "desc"}
    )
    
    # Generate mock suggestions
    suggestions = [
        "Show me all contracts expiring this month",
        "Find contracts with payment terms",
        "Show high-risk contracts",
        "Find contracts with termination clauses",
        "Show all draft contracts"
    ]
    
    # Add contract-specific suggestions
    for contract in contracts:
        suggestions.append(f"Find contracts similar to {contract.title}")
    
    return {"suggestions": suggestions[:8]}  # Limit to 8 suggestions

@router.get("/analytics")
async def get_contract_analytics(
    current_user = Depends(get_current_user),
    prisma = Depends(get_db)
):
    """Get analytics about user's contracts"""
    
    # Get all contracts for the user
    contracts = await prisma.contract.find_many(
        where={"userId": current_user.id}
    )
    
    # Calculate analytics
    total_contracts = len(contracts)
    status_counts = {}
    
    for contract in contracts:
        status = contract.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Mock risk analysis
    risk_analysis = {
        "high_risk": total_contracts // 4,
        "medium_risk": total_contracts // 2,
        "low_risk": total_contracts - (total_contracts // 4) - (total_contracts // 2)
    }
    
    return {
        "total_contracts": total_contracts,
        "status_breakdown": status_counts,
        "risk_analysis": risk_analysis,
        "recent_activity": len([c for c in contracts if c.status == "uploaded"])
    }

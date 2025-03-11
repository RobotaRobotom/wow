from typing import Dict, List, Any
from fastapi import APIRouter, Depends, Query

from app.dependencies import get_search_service
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/", response_model=Dict[str, List[Dict[str, Any]]])
async def search(
    query: str = Query(..., description="Search query string"),
    search_service: SearchService = Depends(get_search_service)
):
    """
    Search across teams, services, and runtime components.
    
    - **query**: The search query string
    
    Returns a dictionary with search results categorized by type:
    - **teams**: List of teams matching the query
    - **services**: List of services matching the query
    - **runtime_components**: List of runtime components matching the query
    """
    return search_service.search(query)

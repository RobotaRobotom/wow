from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query

from app.dependencies import get_service_service
from app.services.service_service import ServiceService
from app.models.service import Service

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/", response_model=List[Dict[str, Any]])
async def get_services(
    team_id: Optional[str] = Query(None, description="Filter by team ID"),
    team_name: Optional[str] = Query(None, description="Filter by team name"),
    business_segment: Optional[str] = Query(None, description="Filter by business segment"),
    value_stream_name: Optional[str] = Query(None, description="Filter by value stream name"),
    sla: Optional[str] = Query(None, description="Filter by SLA"),
    service_service: ServiceService = Depends(get_service_service)
):
    """
    Get all services, optionally filtered by various criteria.
    
    - **team_id**: Filter services by team ID
    - **team_name**: Filter services by team name
    - **business_segment**: Filter services by business segment
    - **value_stream_name**: Filter services by value stream name
    - **sla**: Filter services by SLA
    """
    return service_service.get_all_services(
        team_id=team_id,
        team_name=team_name,
        business_segment=business_segment,
        value_stream_name=value_stream_name,
        sla=sla
    )


@router.get("/{service_name}", response_model=Dict[str, Any])
async def get_service(service_name: str, service_service: ServiceService = Depends(get_service_service)):
    """
    Get a service by its name.
    
    - **service_name**: The name of the service to retrieve
    """
    service = service_service.get_service_by_name(service_name)
    if not service:
        raise HTTPException(status_code=404, detail=f"Service with name {service_name} not found")
    return service

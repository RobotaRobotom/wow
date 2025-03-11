from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query

from app.dependencies import get_runtime_component_service
from app.services.runtime_component_service import RuntimeComponentService

router = APIRouter(prefix="/runtime-components", tags=["runtime-components"])


@router.get("/", response_model=List[Dict[str, Any]])
async def get_runtime_components(
    component_name: Optional[str] = Query(None, description="Filter by component name (partial match)"),
    service_name: Optional[str] = Query(None, description="Filter by service name"),
    runtime_component_service: RuntimeComponentService = Depends(get_runtime_component_service)
):
    """
    Get all runtime components, optionally filtered by component name or service name.
    
    - **component_name**: Filter components by name (partial match)
    - **service_name**: Filter components by service name
    """
    return runtime_component_service.get_all_runtime_components(
        component_name=component_name,
        service_name=service_name
    )


@router.get("/{component_name}", response_model=Dict[str, Any])
async def get_runtime_component(
    component_name: str, 
    runtime_component_service: RuntimeComponentService = Depends(get_runtime_component_service)
):
    """
    Get a runtime component by its name.
    
    - **component_name**: The name of the runtime component to retrieve
    """
    component = runtime_component_service.get_runtime_component_by_name(component_name)
    if not component:
        raise HTTPException(
            status_code=404, 
            detail=f"Runtime component with name {component_name} not found"
        )
    return component

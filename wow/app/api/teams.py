from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query

from app.dependencies import get_team_service
from app.services.team_service import TeamService
from app.models.team import Team

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=List[Team])
async def get_teams(
    business_segment: Optional[str] = Query(None, description="Filter by business segment"),
    value_stream_name: Optional[str] = Query(None, description="Filter by value stream name"),
    team_service: TeamService = Depends(get_team_service)
):
    """
    Get all teams, optionally filtered by business segment or value stream.
    
    - **business_segment**: Filter teams by business segment
    - **value_stream_name**: Filter teams by value stream name
    """
    return team_service.get_all_teams(business_segment, value_stream_name)


@router.get("/{team_id}", response_model=Team)
async def get_team(team_id: str, team_service: TeamService = Depends(get_team_service)):
    """
    Get a team by its ID.
    
    - **team_id**: The ID of the team to retrieve
    """
    team = team_service.get_team_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail=f"Team with ID {team_id} not found")
    return team

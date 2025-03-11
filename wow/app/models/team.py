from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.service import Service
from app.models.value_stream import ValueStream


class TeamAPI(BaseModel):
    """
    Represents the Team API information, inspired by Team Topologies.
    """
    team_mission: str
    contact_channels: Dict[str, str]
    team_type: str
    collaboration_preferences: str


class Team(BaseModel):
    """
    Represents a team that owns services and is aligned with value streams.
    """
    team_id: str
    team_name: str
    business_segment: str
    value_streams: List[ValueStream]
    services_applications: List[Service]
    team_api: TeamAPI


class ChangeHistory(BaseModel):
    """
    Represents a change in the version history of the data.
    """
    version: str
    date: datetime
    description: str


class Metadata(BaseModel):
    """
    Represents metadata about the data file, including version and change history.
    """
    version: str
    last_updated: datetime
    change_history: List[ChangeHistory]


class TeamList(BaseModel):
    """
    Represents the top-level structure of the data file, containing metadata and a list of teams.
    """
    metadata: Metadata
    teams: List[Team]

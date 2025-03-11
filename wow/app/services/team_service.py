from typing import List, Optional, Dict, Any
from app.data.json_loader import JsonLoader
from app.models.team import Team


class TeamService:
    """
    Service for retrieving and filtering team data.
    """
    def __init__(self, json_loader: JsonLoader):
        self.json_loader = json_loader
        
    def get_all_teams(self, 
                     business_segment: Optional[str] = None,
                     value_stream_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all teams, optionally filtered by business segment or value stream.
        
        Args:
            business_segment: Optional filter by business segment.
            value_stream_name: Optional filter by value stream name.
            
        Returns:
            List of teams matching the filters.
        """
        data = self.json_loader.get_data()
        teams = data.get("teams", [])
        
        if business_segment:
            teams = [t for t in teams if t["business_segment"] == business_segment]
            
        if value_stream_name:
            teams = [t for t in teams if any(vs["value_stream_name"] == value_stream_name 
                                           for vs in t["value_streams"])]
                                           
        return teams
        
    def get_team_by_id(self, team_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a team by its ID.
        
        Args:
            team_id: The ID of the team to retrieve.
            
        Returns:
            The team with the specified ID, or None if not found.
        """
        data = self.json_loader.get_data()
        teams = data.get("teams", [])
        
        for team in teams:
            if team["team_id"] == team_id:
                return team
                
        return None

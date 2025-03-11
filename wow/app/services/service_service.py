from typing import List, Optional, Dict, Any
from app.data.json_loader import JsonLoader


class ServiceService:
    """
    Service for retrieving and filtering service data.
    """
    def __init__(self, json_loader: JsonLoader):
        self.json_loader = json_loader
        
    def get_all_services(self,
                        team_id: Optional[str] = None,
                        team_name: Optional[str] = None,
                        business_segment: Optional[str] = None,
                        value_stream_name: Optional[str] = None,
                        sla: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all services, optionally filtered by various criteria.
        
        Args:
            team_id: Optional filter by team ID.
            team_name: Optional filter by team name.
            business_segment: Optional filter by business segment.
            value_stream_name: Optional filter by value stream name.
            sla: Optional filter by SLA.
            
        Returns:
            List of services matching the filters.
        """
        data = self.json_loader.get_data()
        teams = data.get("teams", [])
        all_services = []
        
        for team in teams:
            # Apply team-level filters
            if team_id and team["team_id"] != team_id:
                continue
                
            if team_name and team["team_name"] != team_name:
                continue
                
            if business_segment and team["business_segment"] != business_segment:
                continue
                
            if value_stream_name and not any(vs["value_stream_name"] == value_stream_name 
                                           for vs in team["value_streams"]):
                continue
                
            # Add team context to each service
            for service in team["services_applications"]:
                service_with_context = service.copy()
                service_with_context["team_id"] = team["team_id"]
                service_with_context["team_name"] = team["team_name"]
                service_with_context["business_segment"] = team["business_segment"]
                
                # Apply service-level filters
                if value_stream_name and value_stream_name not in service["value_stream_segments"]:
                    continue
                    
                if sla and service["business_criticality"]["sla"] != sla:
                    continue
                    
                all_services.append(service_with_context)
                
        return all_services
        
    def get_service_by_name(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a service by its name.
        
        Args:
            service_name: The name of the service to retrieve.
            
        Returns:
            The service with the specified name, or None if not found.
        """
        data = self.json_loader.get_data()
        teams = data.get("teams", [])
        
        for team in teams:
            for service in team["services_applications"]:
                if service["service_name"] == service_name:
                    service_with_context = service.copy()
                    service_with_context["team_id"] = team["team_id"]
                    service_with_context["team_name"] = team["team_name"]
                    service_with_context["business_segment"] = team["business_segment"]
                    return service_with_context
                    
        return None

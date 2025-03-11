from typing import List, Dict, Any
from app.data.json_loader import JsonLoader


class SearchService:
    """
    Service for searching across teams, services, and runtime components.
    """
    def __init__(self, json_loader: JsonLoader):
        self.json_loader = json_loader
        
    def search(self, query: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search across teams, services, and runtime components.
        
        Args:
            query: The search query string.
            
        Returns:
            Dictionary with search results categorized by type.
        """
        if not query or len(query.strip()) == 0:
            return {
                "teams": [],
                "services": [],
                "runtime_components": []
            }
            
        query = query.lower()
        data = self.json_loader.get_data()
        teams = data.get("teams", [])
        
        team_results = []
        service_results = []
        component_results = []
        
        for team in teams:
            # Search in team fields
            team_match = (
                query in team["team_id"].lower() or
                query in team["team_name"].lower() or
                query in team["business_segment"].lower() or
                query in team["team_api"]["team_mission"].lower()
            )
            
            if team_match:
                team_results.append(team)
                
            # Search in value streams
            for value_stream in team["value_streams"]:
                if (query in value_stream["value_stream_name"].lower() or
                    query in value_stream["value_stream_description"].lower()):
                    if team not in team_results:
                        team_results.append(team)
                        
            # Search in services
            for service in team["services_applications"]:
                service_match = (
                    query in service["service_name"].lower() or
                    query in service["tech_stack"].lower()
                )
                
                if service_match:
                    service_with_context = service.copy()
                    service_with_context["team_id"] = team["team_id"]
                    service_with_context["team_name"] = team["team_name"]
                    service_with_context["business_segment"] = team["business_segment"]
                    service_results.append(service_with_context)
                    
                # Search in runtime components
                for component in service["runtime_components"]:
                    if query in component.lower():
                        component_with_context = {
                            "component_name": component,
                            "service_name": service["service_name"],
                            "team_id": team["team_id"],
                            "team_name": team["team_name"],
                            "business_segment": team["business_segment"],
                            "tech_stack": service["tech_stack"]
                        }
                        component_results.append(component_with_context)
                        
        return {
            "teams": team_results,
            "services": service_results,
            "runtime_components": component_results
        }

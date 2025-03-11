from typing import List, Optional, Dict, Any
from app.data.json_loader import JsonLoader


class RuntimeComponentService:
    """
    Service for retrieving and filtering runtime component data.
    """
    def __init__(self, json_loader: JsonLoader):
        self.json_loader = json_loader
        
    def get_all_runtime_components(self,
                                  component_name: Optional[str] = None,
                                  service_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all runtime components, optionally filtered by component name or service name.
        
        Args:
            component_name: Optional filter by component name (partial match).
            service_name: Optional filter by service name.
            
        Returns:
            List of runtime components matching the filters.
        """
        data = self.json_loader.get_data()
        teams = data.get("teams", [])
        all_components = []
        
        for team in teams:
            for service in team["services_applications"]:
                # Apply service-level filter
                if service_name and service["service_name"] != service_name:
                    continue
                    
                for component in service["runtime_components"]:
                    # Apply component-level filter
                    if component_name and component_name.lower() not in component.lower():
                        continue
                        
                    component_with_context = {
                        "component_name": component,
                        "service_name": service["service_name"],
                        "team_id": team["team_id"],
                        "team_name": team["team_name"],
                        "business_segment": team["business_segment"],
                        "tech_stack": service["tech_stack"]
                    }
                    
                    all_components.append(component_with_context)
                    
        return all_components
        
    def get_runtime_component_by_name(self, component_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a runtime component by its exact name.
        
        Args:
            component_name: The name of the runtime component to retrieve.
            
        Returns:
            The runtime component with the specified name, or None if not found.
        """
        data = self.json_loader.get_data()
        teams = data.get("teams", [])
        
        for team in teams:
            for service in team["services_applications"]:
                for component in service["runtime_components"]:
                    if component == component_name:
                        component_with_context = {
                            "component_name": component,
                            "service_name": service["service_name"],
                            "team_id": team["team_id"],
                            "team_name": team["team_name"],
                            "business_segment": team["business_segment"],
                            "tech_stack": service["tech_stack"],
                            "business_criticality": service["business_criticality"]
                        }
                        return component_with_context
                        
        return None

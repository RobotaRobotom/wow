import os
from fastapi import Depends

from app.data.json_loader import JsonLoader
from app.services.team_service import TeamService
from app.services.service_service import ServiceService
from app.services.runtime_component_service import RuntimeComponentService
from app.services.search_service import SearchService

# Data file path
DATA_FILE = os.environ.get("WOW_DATA_FILE", "app/data/wow_data.json")

def get_json_loader():
    return JsonLoader(DATA_FILE)

def get_team_service(json_loader: JsonLoader = Depends(get_json_loader)):
    return TeamService(json_loader)

def get_service_service(json_loader: JsonLoader = Depends(get_json_loader)):
    return ServiceService(json_loader)

def get_runtime_component_service(json_loader: JsonLoader = Depends(get_json_loader)):
    return RuntimeComponentService(json_loader)

def get_search_service(json_loader: JsonLoader = Depends(get_json_loader)):
    return SearchService(json_loader)

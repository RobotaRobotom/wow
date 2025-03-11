from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class BusinessCriticality(BaseModel):
    """
    Represents the business criticality of a service, including SLA and SLO.
    """
    sla: str
    slo: str


class Service(BaseModel):
    """
    Represents a service or application owned by a team.
    """
    service_name: str
    value_stream_segments: List[str]
    tech_stack: str
    business_criticality: BusinessCriticality
    runtime_components: List[str]
    repository_url: str

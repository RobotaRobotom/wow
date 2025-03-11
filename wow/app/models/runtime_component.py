from typing import Optional
from pydantic import BaseModel


class RuntimeComponent(BaseModel):
    """
    Represents a runtime component that is created when a service is built and running.
    """
    component_name: str
    service_name: str
    description: Optional[str] = None

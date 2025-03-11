from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class ValueStreamBreakdown(BaseModel):
    """
    Represents a breakdown of a value stream, such as countries or product lines.
    This is a flexible structure that can contain any key-value pairs.
    """
    countries: Optional[List[str]] = None
    product_lines: Optional[List[str]] = None
    # Additional fields can be added as needed


class ValueStream(BaseModel):
    """
    Represents a value stream segment that a team is aligned with.
    """
    value_stream_name: str
    value_stream_description: str
    value_stream_breakdown: Optional[ValueStreamBreakdown] = None

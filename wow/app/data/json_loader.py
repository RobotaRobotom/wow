import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import ValidationError

from app.models.team import TeamList


class JsonLoader:
    """
    Responsible for loading and validating the JSON data file.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._data: Optional[Dict[str, Any]] = None
        self._last_loaded: Optional[datetime] = None
        
    def load(self) -> Dict[str, Any]:
        """
        Load JSON data from file and validate against schema.
        
        Returns:
            Dict[str, Any]: The loaded and validated JSON data.
            
        Raises:
            FileNotFoundError: If the JSON file does not exist.
            ValueError: If the JSON data is invalid.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"JSON file not found: {self.file_path}")
            
        with open(self.file_path, 'r') as f:
            raw_data = json.load(f)
            
        # Validate data against Pydantic model
        try:
            TeamList.model_validate(raw_data)
        except Exception as e:
            raise ValueError(f"Invalid JSON data: {str(e)}")
            
        self._data = raw_data
        self._last_loaded = datetime.now()
        return raw_data
        
    def get_data(self) -> Dict[str, Any]:
        """
        Get cached data or load if not loaded yet.
        
        Returns:
            Dict[str, Any]: The loaded and validated JSON data.
        """
        if self._data is None:
            return self.load()
        return self._data

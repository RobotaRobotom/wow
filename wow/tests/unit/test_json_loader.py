import os
import json
import pytest
from datetime import datetime
from unittest.mock import patch, mock_open

from app.data.json_loader import JsonLoader
from app.models.team import TeamList


@pytest.fixture
def valid_json_data():
    """
    Fixture providing valid JSON data for testing.
    """
    return {
        "metadata": {
            "version": "1.0.0",
            "last_updated": "2025-03-11T08:30:00Z",
            "change_history": [
                {
                    "version": "1.0.0",
                    "date": "2025-03-11T08:30:00Z",
                    "description": "Initial version"
                }
            ]
        },
        "teams": [
            {
                "team_id": "team_alpha",
                "team_name": "Alpha Squad",
                "business_segment": "Internet Banking Division",
                "value_streams": [
                    {
                        "value_stream_name": "Mortgage Application",
                        "value_stream_description": "End-to-end mortgage process",
                        "value_stream_breakdown": {
                            "countries": ["US", "UK"],
                            "product_lines": ["Mortgage", "Home Equity"]
                        }
                    }
                ],
                "services_applications": [
                    {
                        "service_name": "mortgage-processing",
                        "value_stream_segments": [
                            "Mortgage Application"
                        ],
                        "tech_stack": "Java",
                        "business_criticality": {
                            "sla": "99.9%",
                            "slo": "99.95%"
                        },
                        "runtime_components": [
                            "mortgage-processing-backend",
                            "mortgage-processing-reporting"
                        ],
                        "repository_url": "https://github.com/YourOrg/mortgage-processing"
                    }
                ],
                "team_api": {
                    "team_mission": "Deliver secure and scalable banking solutions.",
                    "contact_channels": {
                        "slack_channel": "#alpha-squad-support",
                        "email": "alpha-squad@examplebank.com"
                    },
                    "team_type": "stream-aligned",
                    "collaboration_preferences": "We prefer asynchronous communication via Slack or tickets."
                }
            }
        ]
    }


@pytest.fixture
def invalid_json_data():
    """
    Fixture providing invalid JSON data for testing.
    """
    return {
        "metadata": {
            "version": "1.0.0",
            "last_updated": "2025-03-11T08:30:00Z",
            "change_history": [
                {
                    "version": "1.0.0",
                    "date": "2025-03-11T08:30:00Z",
                    "description": "Initial version"
                }
            ]
        },
        # Missing "teams" key
    }


class TestJsonLoader:
    """
    Tests for the JsonLoader class.
    """

    def test_init(self):
        """
        Test that the JsonLoader initializes correctly.
        """
        loader = JsonLoader("test.json")
        assert loader.file_path == "test.json"
        assert loader._data is None
        assert loader._last_loaded is None

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"metadata": {}, "teams": []}))
    @patch("app.models.team.TeamList.model_validate")
    def test_load_valid_json(self, mock_validate, mock_file, mock_exists, valid_json_data):
        """
        Test loading valid JSON data.
        """
        mock_exists.return_value = True
        mock_validate.return_value = TeamList(**valid_json_data)
        
        loader = JsonLoader("test.json")
        data = loader.load()
        
        assert data == {"metadata": {}, "teams": []}
        assert loader._data == {"metadata": {}, "teams": []}
        assert loader._last_loaded is not None
        mock_exists.assert_called_once_with("test.json")
        mock_file.assert_called_once_with("test.json", "r")
        mock_validate.assert_called_once()

    @patch("os.path.exists")
    def test_load_file_not_found(self, mock_exists):
        """
        Test loading a file that doesn't exist.
        """
        mock_exists.return_value = False
        
        loader = JsonLoader("test.json")
        with pytest.raises(FileNotFoundError):
            loader.load()
            
        mock_exists.assert_called_once_with("test.json")

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"invalid": "data"}))
    @patch("app.models.team.TeamList.model_validate")
    def test_load_invalid_json(self, mock_validate, mock_file, mock_exists):
        """
        Test loading invalid JSON data.
        """
        mock_exists.return_value = True
        mock_validate.side_effect = Exception("Invalid JSON data")
        
        loader = JsonLoader("test.json")
        with pytest.raises(ValueError):
            loader.load()
            
        mock_exists.assert_called_once_with("test.json")
        mock_file.assert_called_once_with("test.json", "r")
        mock_validate.assert_called_once()

    @patch.object(JsonLoader, "load")
    def test_get_data_not_loaded(self, mock_load, valid_json_data):
        """
        Test getting data when it hasn't been loaded yet.
        """
        mock_load.return_value = valid_json_data
        
        loader = JsonLoader("test.json")
        data = loader.get_data()
        
        assert data == valid_json_data
        mock_load.assert_called_once()

    @patch.object(JsonLoader, "load")
    def test_get_data_already_loaded(self, mock_load, valid_json_data):
        """
        Test getting data when it has already been loaded.
        """
        loader = JsonLoader("test.json")
        loader._data = valid_json_data
        loader._last_loaded = datetime.now()
        
        data = loader.get_data()
        
        assert data == valid_json_data
        mock_load.assert_not_called()

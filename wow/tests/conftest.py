"""
Shared pytest fixtures for the WOW application tests.
"""
import os
import sys
import pytest
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.data.json_loader import JsonLoader
from app.services.team_service import TeamService
from app.services.service_service import ServiceService
from app.services.runtime_component_service import RuntimeComponentService
from app.services.search_service import SearchService


@pytest.fixture
def test_data_dir():
    """
    Fixture providing the path to the test data directory.
    """
    return Path(__file__).parent / "test_data"


@pytest.fixture
def test_data_file(test_data_dir):
    """
    Fixture providing the path to the test data file.
    """
    return test_data_dir / "test_wow_data.json"


@pytest.fixture
def sample_json_data():
    """
    Fixture providing sample JSON data for testing.
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
def json_loader(test_data_file, sample_json_data, monkeypatch):
    """
    Fixture providing a JsonLoader instance with mocked data.
    """
    # Ensure the test data directory exists
    test_data_file.parent.mkdir(exist_ok=True)
    
    # Write sample data to the test file
    with open(test_data_file, "w") as f:
        json.dump(sample_json_data, f)
        
    # Create a JsonLoader instance
    loader = JsonLoader(str(test_data_file))
    
    # Monkeypatch the loader to return the sample data
    monkeypatch.setattr(loader, "get_data", lambda: sample_json_data)
    
    return loader


@pytest.fixture
def team_service(json_loader):
    """
    Fixture providing a TeamService instance.
    """
    return TeamService(json_loader)


@pytest.fixture
def service_service(json_loader):
    """
    Fixture providing a ServiceService instance.
    """
    return ServiceService(json_loader)


@pytest.fixture
def runtime_component_service(json_loader):
    """
    Fixture providing a RuntimeComponentService instance.
    """
    return RuntimeComponentService(json_loader)


@pytest.fixture
def search_service(json_loader):
    """
    Fixture providing a SearchService instance.
    """
    return SearchService(json_loader)

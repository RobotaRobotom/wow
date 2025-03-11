# WOW (Who Owns What) API

A backend Python application that serves as a single source of truth regarding software services ownership by DevOps teams.

## Overview

WOW (Who Owns What) is a FastAPI-based application that provides a RESTful API for querying information about teams, services, and runtime components. It uses a JSON file as the data source and provides flexible query capabilities.

## Features

- Query teams by business segment or value stream
- Query services by team, business segment, value stream, or SLA
- Query runtime components by name or service
- Search across teams, services, and runtime components

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd wow
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

On Windows:
```bash
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:
```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

For development, install development dependencies:

```bash
pip install -r requirements-dev.txt
```

### Running the Application

#### Using Python

```bash
uvicorn app.main:app --reload --port 8001
```

The API will be available at http://localhost:8001.

#### Using Docker

```bash
docker-compose up
```

The API will be available at http://localhost:8001.

## API Documentation

Once the application is running, you can access the Swagger UI documentation at http://localhost:8001/docs.

### Endpoints

- `/teams` - Get all teams or filter by business segment or value stream
- `/teams/{team_id}` - Get a specific team by ID
- `/services` - Get all services or filter by team, business segment, value stream, or SLA
- `/services/{service_name}` - Get a specific service by name
- `/runtime-components` - Get all runtime components or filter by name or service
- `/runtime-components/{component_name}` - Get a specific runtime component by name
- `/search` - Search across teams, services, and runtime components

## Data Structure

The application uses a JSON file as the data source. By default, the file is located at `app/data/wow_data.json`. You can override this location by setting the `WOW_DATA_FILE` environment variable.

The JSON file should follow the structure defined in the models.

### Example JSON Structure

```json
{
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
```

## Development

### Project Structure

```
wow/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application entry point
│   ├── models/                # Pydantic models
│   ├── data/                  # Data access layer
│   ├── services/              # Business logic
│   └── api/                   # API endpoints
├── tests/
│   ├── unit/                  # Unit tests
│   └── features/              # BDD tests
├── Dockerfile                 # For containerization
├── docker-compose.yml         # For local development
├── requirements.txt           # Dependencies
├── requirements-dev.txt       # Development dependencies
└── README.md                  # Documentation
```

### Testing Approach

The WOW application uses two types of testing:

1. **Unit Tests**: Located in the `tests/unit/` directory, these tests verify the functionality of individual components in isolation. They use pytest and mock external dependencies.

2. **Behavior-Driven Development (BDD) Tests**: Located in the `tests/features/` directory, these tests verify the behavior of the application from an end-user perspective. They use the Behave framework and are written in Gherkin syntax.

#### Test Scenarios

BDD test scenarios are stored in the `tests/features/scenarios/` directory. Each feature file contains multiple scenarios that describe the expected behavior of the application. For example:

- `teams.feature`: Tests for team-related endpoints
- `services.feature`: Tests for service-related endpoints
- `runtime_components.feature`: Tests for runtime component-related endpoints
- `search.feature`: Tests for search functionality

#### Running Tests

To run unit tests:

```powershell
cd wow
.\.venv\Scripts\Activate.ps1
pytest tests/unit
```

To run BDD tests (make sure the application is running on port 8001 first):

```powershell
cd wow
.\.venv\Scripts\Activate.ps1
behave tests/features
```

To run a specific feature file:

```powershell
behave tests/features/scenarios/teams.feature
```

## License

[MIT License](LICENSE)

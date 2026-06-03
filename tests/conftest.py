"""
Pytest configuration and shared fixtures for FastAPI tests.

This module provides fixtures that set up a clean test environment for each test,
including a fresh FastAPI TestClient and reset in-memory database.
"""

import pytest
from copy import deepcopy
from starlette.testclient import TestClient
from src.app import app, activities


# Original state of the activities database (to reset between tests)
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team training and competitive soccer matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "nina@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Practice skills and play pickup basketball games",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["maria@mergington.edu", "isaac@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and mixed media projects",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["lily@mergington.edu", "omar@mergington.edu"]
    },
    "Drama Club": {
        "description": "Practice acting, stagecraft, and prepare performances",
        "schedule": "Tuesdays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["chloe@mergington.edu", "tyler@mergington.edu"]
    },
    "Book Club": {
        "description": "Discuss fiction and non-fiction books with fellow readers",
        "schedule": "Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["sarah@mergington.edu", "matt@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["rachel@mergington.edu", "noah@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """
    Provide a TestClient with a fresh activities database state.
    
    This fixture resets the in-memory activities database to its original state
    before each test, ensuring test isolation and reproducibility.
    """
    # Arrange: Reset activities to original state
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    
    # Return a TestClient for making requests to the app
    yield TestClient(app)

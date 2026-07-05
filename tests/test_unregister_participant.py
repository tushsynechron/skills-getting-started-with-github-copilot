import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def restore_activities_state():
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_unregister_participant_removes_them_from_activity(client):
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/Chess Club/participants/{email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"

    updated = client.get("/activities")
    assert email not in updated.json()["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in updated.json()["Chess Club"]["participants"]

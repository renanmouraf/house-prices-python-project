from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_status():
    response = client.get("/api/security/status")
    assert response.status_code == 200
    assert "OK" in response.json()

@pytest.mark.usefixtures("setup_user")
def test_token_successful():
    response = client.post("/api/security/token", dict(username="user2", password="pass2"))
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.usefixtures("setup_user")
def test_token_unauthorized():
    response = client.post("/api/security/token", dict(username="user2", password="pass"))
    assert response.status_code == 401

@pytest.mark.usefixtures("setup_user")
def test_token_valid(helpers):
    jwt_token = helpers.get_jwt_token()

    payload = {"token": jwt_token}
    response = client.post("/api/security/token/validate", json=payload)

    assert response.status_code == 200
    assert response.json()["valid"] == "true"


def test_token_invalid():
    payload = {"token": "TEST_TOKEN"}
    response = client.post("/api/security/token/validate", json=payload)

    assert response.status_code == 200
    assert response.json()["valid"] == "false"

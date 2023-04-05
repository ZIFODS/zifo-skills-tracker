from fastapi.testclient import TestClient
import pytest

from app import main

test_client = TestClient(main.app)


@pytest.fixture(scope="session")
def health_response():
    return test_client.get("/health")


class TestHealthAPI:
    def test_api_health(self, health_response):
        assert health_response.status_code == 200
        assert health_response.json()["message"] == "Server is healthy"

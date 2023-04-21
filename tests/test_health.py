from fastapi.testclient import TestClient
import pytest

from app import main

test_client = TestClient(main.app)


@pytest.mark.order(1)
class TestHealthAPI:
    def test_api_health(self):
        health_response = test_client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["message"] == "Server is healthy"

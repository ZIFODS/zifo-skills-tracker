from fastapi.testclient import TestClient

from app import main
from tests.expected_results.expected_categories import CATEGORIES

test_client = TestClient(main.app)


class TestCategories:
    def test_get_all_categories(self):
        response = test_client.get("/categories")
        assert response.status_code == 200
        assert response.json() == CATEGORIES

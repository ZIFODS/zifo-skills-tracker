from fastapi.testclient import TestClient

from app import main
from tests.expected_results import categories_test_data

test_client = TestClient(main.app)


class TestCategories:
    def test_get_all_categories(self):
        response = test_client.get(categories_test_data.GetAllCategories.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == categories_test_data.GetAllCategories.CATEGORIES

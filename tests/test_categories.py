from fastapi.testclient import TestClient
import pytest

from app import main
import tests.expected_results.categories_testdata as expected

test_client = TestClient(main.app)


@pytest.mark.order(2)
class TestCategories:
    def test_get_all_categories(self):
        response = test_client.get("/categories")
        assert response.status_code == 200
        assert response.json() == expected.GetAllCategories.CATEGORIES


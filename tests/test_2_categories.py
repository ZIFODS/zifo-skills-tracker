from fastapi.testclient import TestClient
from tests.expected_results.expected_categories import CATEGORIES
import pytest

from app import main

test_client = TestClient(main.app)


@pytest.fixture(scope="session")
def categories_response():
    return test_client.get("/categories")


class TestCategories:
    def test_get_all_categories(self, categories_response):
        assert categories_response.status_code == 200
        assert categories_response.json() == CATEGORIES

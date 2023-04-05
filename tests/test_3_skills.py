from fastapi.testclient import TestClient
from tests.expected_results.expected_skills import Skills
from tests.expected_results.expected_categories import CATEGORIES
import pytest

from app import main

test_client = TestClient(main.app)

example_category = "Data_Management"
existing_skill = "CDISC Study Data Tabulation Model"
unknown_skill = "TEST SKILL"
expected_new_skill_json = {
    "name": unknown_skill,
    "category": example_category,
    "type": "Skill"
}


@pytest.fixture(scope="session")
def skills_response():
    return test_client.get(f"/skills/?category={example_category}")


class TestCategories:
    def test_get_skills_per_category(self, skills_response):
        assert skills_response.status_code == 200
        assert skills_response.json() == Skills.DATA_MANAGEMENT_SKILLS

    def test_get_single_skill(self):
        response = test_client.get(f"/skills/{existing_skill}")
        assert response.status_code == 200
        assert response.json()["name"] == existing_skill and response.json()["type"] == "Skill"

    def test_get_single_skill_not_found(self):
        response = test_client.get(f"/skills/{unknown_skill}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Skill not found"

    def test_create_duplicate_skill(self):
        response = test_client.post(
            "/skills/",
            json={"name": existing_skill, "category": example_category},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Skill already exists"

    def test_delete_skill_not_found(self):
        response = test_client.delete(f"/skills/{unknown_skill}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Skill not found"

    def test_create_skill(self):
        response = test_client.post(
            "/skills/",
            json={"name": unknown_skill, "category": example_category},
        )
        assert response.status_code == 200
        assert response.json() == expected_new_skill_json

        double_check = test_client.get(f"/skills/{unknown_skill}")
        assert double_check.status_code == 200
        assert double_check.json() == expected_new_skill_json

    def test_delete_skill(self):
        response = test_client.delete(f"/skills/{unknown_skill}")
        assert response.status_code == 200
        assert response.json()["message"] == f"Deleted skill {unknown_skill}"

        double_check = test_client.get(f"/skills/{unknown_skill}")
        assert double_check.status_code == 404
        assert double_check.json()["detail"] == "Skill not found"




import pytest
from fastapi.testclient import TestClient

from app import main
from tests.expected_results.expected_skills import Skills

test_client = TestClient(main.app)

# Set delete_skill - Delete either unknown_skill or existing_skill (in Skills class)
# unknown_skill: is created before the delete test - DB data will be in inital state if create and delete tests pass,
#                but delete test will depend on successful create test
# existing_skill: deletion will result in changed DB data after passed tests - mock data will have to be reloaded
#                 before next test, but delete test will be independent of create test
delete_skill = Skills.existing_skill


class TestCategories:
    def test_get_all_skills(self):
        response = test_client.get("/skills/")
        assert response.status_code == 200
        assert response.json() == Skills.ALL_SKILLS

    def test_get_skills_per_category(self):
        response = test_client.get(f"/skills/?category={Skills.example_category}")
        assert response.status_code == 200
        assert response.json() == Skills.DATA_MANAGEMENT_SKILLS

    @pytest.mark.dependency()
    def test_get_single_skill(self):
        response = test_client.get(f"/skills/{Skills.existing_skill}")
        assert response.status_code == 200
        assert response.json()["name"] == Skills.existing_skill and response.json()["type"] == "Skill"

    def test_get_single_skill_not_found(self):
        response = test_client.get(f"/skills/{Skills.unknown_skill}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Skill not found"

    def test_create_duplicate_skill(self):
        response = test_client.post(
            "/skills/",
            json={"name": Skills.existing_skill, "category": Skills.example_category},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Skill already exists"

    def test_delete_skill_not_found(self):
        response = test_client.delete(f"/skills/{Skills.unknown_skill}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Skill not found"

    @pytest.mark.dependency()
    def test_create_skill(self):
        response = test_client.post(
            "/skills/",
            json={"name": Skills.unknown_skill, "category": Skills.example_category},
        )
        assert response.status_code == 200
        assert response.json() == Skills.expected_new_skill_json

    @pytest.mark.dependency(depends=["TestCategories::test_get_single_skill", "TestCategories::test_create_skill"])
    def test_create_skill_check_result(self):
        double_check = test_client.get(f"/skills/{Skills.unknown_skill}")
        assert double_check.status_code == 200
        assert double_check.json() == Skills.expected_new_skill_json

    @pytest.mark.dependency()
    def test_delete_skill(self):
        response = test_client.delete(f"/skills/{delete_skill}")
        assert response.status_code == 200
        assert response.json()["message"] == f"Deleted skill {delete_skill}"

    @pytest.mark.dependency(depends=["TestCategories::test_get_single_skill", "TestCategories::test_delete_skill"])
    def test_delete_skill_check_result(self):
        double_check = test_client.get(f"/skills/{delete_skill}")
        assert double_check.status_code == 404
        assert double_check.json()["detail"] == "Skill not found"

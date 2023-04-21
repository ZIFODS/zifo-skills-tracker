import pytest
from fastapi.testclient import TestClient

from app import main
from tests.expected_results import skills_testdata

test_client = TestClient(main.app)


@pytest.mark.order(6)
class TestCategories:
    def test_get_all_skills(self):
        response = test_client.get(skills_testdata.GetAllSkills.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == skills_testdata.GetAllSkills.EXPECTED_RESULT

    def test_get_skills_per_category(self):
        response = test_client.get(skills_testdata.GetSkillPerCategory.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == skills_testdata.GetSkillPerCategory.EXPECTED_RESULT

    @pytest.mark.dependency()
    def test_get_single_skill(self):
        response = test_client.get(skills_testdata.GetSingleSkill.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == skills_testdata.GetSingleSkill.EXPECTED_RESULT

    def test_get_single_skill_not_found(self):
        response = test_client.get(skills_testdata.GetSingleSkillNotFound.QUERY_PATH)
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == skills_testdata.GetSingleSkillNotFound.EXPECTED_DETAIL
        )

    def test_create_duplicate_skill(self):
        response = test_client.post(
            skills_testdata.CreatDuplicateSkill.QUERY_PATH,
            json=skills_testdata.CreatDuplicateSkill.INPUT,
        )
        assert response.status_code == 409
        assert (
            response.json()["detail"]
            == skills_testdata.CreatDuplicateSkill.EXPECTED_DETAIL
        )

    def test_delete_skill_not_found(self):
        response = test_client.delete(skills_testdata.DeleteSkillNotFound.QUERY_PATH)
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == skills_testdata.DeleteSkillNotFound.EXPECTED_DETAIL
        )

    @pytest.mark.dependency()
    def test_create_skill(self):
        response = test_client.post(
            skills_testdata.CreateSkill.QUERY_PATH,
            json=skills_testdata.CreateSkill.INPUT,
        )
        assert response.status_code == 200
        assert response.json() == skills_testdata.CreateSkill.EXPECTED_RESULT

    @pytest.mark.dependency(
        depends=[
            "TestCategories::test_get_single_skill",
            "TestCategories::test_create_skill",
        ]
    )
    def test_create_skill_check_result(self):
        double_check = test_client.get(
            skills_testdata.CreateSkillCheckResult.QUERY_PATH
        )
        assert double_check.status_code == 200
        assert (
            double_check.json()
            == skills_testdata.CreateSkillCheckResult.EXPECTED_RESULT
        )

    @pytest.mark.dependency()
    def test_delete_skill(self):
        response = test_client.delete(skills_testdata.DeleteSkill.QUERY_PATH)
        assert response.status_code == 200
        assert (
            response.json()["message"] == skills_testdata.DeleteSkill.EXPECTED_MESSAGE
        )

    @pytest.mark.dependency(
        depends=[
            "TestCategories::test_get_single_skill",
            "TestCategories::test_delete_skill",
        ]
    )
    def test_delete_skill_check_result(self):
        double_check = test_client.get(
            skills_testdata.DeleteSkillCheckResult.QUERY_PATH
        )
        assert double_check.status_code == 404
        assert (
            double_check.json()["detail"]
            == skills_testdata.DeleteSkillCheckResult.EXPECTED_DETAIL
        )

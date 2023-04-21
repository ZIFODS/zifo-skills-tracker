
import pytest

from fastapi.testclient import TestClient

from app import main
import tests.expected_results.userskills_testdata as userskills_testdata

test_client = TestClient(main.app)


@pytest.mark.order(4)
class TestUserSkills:
    def test_userskills_get_all(self):
        response = test_client.get(userskills_testdata.UserSkillsGetAll.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == userskills_testdata.UserSkillsGetAll.EXPECTED_OUTPUT

    def test_userskills_get_category(self):
        response = test_client.get(userskills_testdata.UserSkillsGetCategory.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == userskills_testdata.UserSkillsGetCategory.EXPECTED_OUTPUT

    def test_userskills_get_learned_skill(self):
        response = test_client.get(userskills_testdata.UserSkillsGetLearnedSkill.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == userskills_testdata.UserSkillsGetLearnedSkill.EXPECTED_OUTPUT

    def test_userskills_get_unlearned_skill(self):
        response = test_client.get(userskills_testdata.UserSkillsGetUnlearnedSkill.QUERY_PATH)
        assert response.status_code == 404
        assert response.json()["detail"] == userskills_testdata.UserSkillsGetUnlearnedSkill.EXPECTED_DETAIL

    def test_userskills_train_trained_skill(self):
        response = test_client.post(
            userskills_testdata.UserSkillsTrainTrainedSkill.QUERY_PATH,
            json=userskills_testdata.UserSkillsTrainTrainedSkill.INPUT
        )
        assert response.status_code == 409
        assert response.json()["detail"] == userskills_testdata.UserSkillsTrainTrainedSkill.EXPECTED_DETAIL

    def test_userskills_forget_untrained_skill(self):
        response = test_client.delete(userskills_testdata.UserSkillsForgetUntrainedSkill.QUERY_PATH)
        assert response.status_code == 409
        assert response.json()["detail"] == userskills_testdata.UserSkillsForgetUntrainedSkill.EXPECTED_DETAIL

    def test_userskills_train_unknown_skill(self):
        response = test_client.post(
            userskills_testdata.UserSkillsTrainUnknownSkill.QUERY_PATH,
            json=userskills_testdata.UserSkillsTrainUnknownSkill.INPUT
        )
        assert response.status_code == 404
        assert response.json()["detail"] == userskills_testdata.UserSkillsTrainUnknownSkill.EXPECTED_DETAIL

    def test_userskills_train_skills(self):
        response = test_client.post(
            userskills_testdata.UserSkillsTrainSkills.QUERY_PATH,
            json=userskills_testdata.UserSkillsTrainSkills.INPUT
        )
        assert response.status_code == 200
        assert response.json() == userskills_testdata.UserSkillsTrainSkills.EXPECTED_OUTPUT

    def test_userskills_forget_skills(self):
        response = test_client.delete(userskills_testdata.UserSkillsForgetSkills.QUERY_PATH)
        assert response.status_code == 200
        assert response.json()["message"] == userskills_testdata.UserSkillsForgetSkills.EXPECTED_MESSAGE


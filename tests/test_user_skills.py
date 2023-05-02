from fastapi.testclient import TestClient

import tests.expected_results.user_skills_test_data as user_skills_test_data
from app import main
from pipeline.load_mock_data import load_neo4j

test_client = TestClient(main.app)


class TestUserSkills:
    def test_userskills_get_all(self):
        response = test_client.get(user_skills_test_data.UserSkillsGetAll.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == user_skills_test_data.UserSkillsGetAll.EXPECTED_OUTPUT

    def test_userskills_get_category(self):
        response = test_client.get(
            user_skills_test_data.UserSkillsGetCategory.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == user_skills_test_data.UserSkillsGetCategory.EXPECTED_OUTPUT
        )

    def test_userskills_get_learned_skill(self):
        response = test_client.get(
            user_skills_test_data.UserSkillsGetLearnedSkill.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == user_skills_test_data.UserSkillsGetLearnedSkill.EXPECTED_OUTPUT
        )

    def test_userskills_get_unlearned_skill(self):
        response = test_client.get(
            user_skills_test_data.UserSkillsGetUnlearnedSkill.QUERY_PATH
        )
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == user_skills_test_data.UserSkillsGetUnlearnedSkill.EXPECTED_DETAIL
        )

    def test_userskills_train_trained_skill(self):
        response = test_client.post(
            user_skills_test_data.UserSkillsTrainTrainedSkill.QUERY_PATH,
            json=user_skills_test_data.UserSkillsTrainTrainedSkill.INPUT,
        )
        assert response.status_code == 409
        assert (
            response.json()["detail"]
            == user_skills_test_data.UserSkillsTrainTrainedSkill.EXPECTED_DETAIL
        )

    def test_userskills_forget_untrained_skill(self):
        response = test_client.delete(
            user_skills_test_data.UserSkillsForgetUntrainedSkill.QUERY_PATH
        )
        assert response.status_code == 409
        assert (
            response.json()["detail"]
            == user_skills_test_data.UserSkillsForgetUntrainedSkill.EXPECTED_DETAIL
        )

    def test_userskills_train_unknown_skill(self):
        response = test_client.post(
            user_skills_test_data.UserSkillsTrainUnknownSkill.QUERY_PATH,
            json=user_skills_test_data.UserSkillsTrainUnknownSkill.INPUT,
        )
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == user_skills_test_data.UserSkillsTrainUnknownSkill.EXPECTED_DETAIL
        )

    def test_userskills_train_skills(self):
        response = test_client.post(
            user_skills_test_data.UserSkillsTrainSkills.QUERY_PATH,
            json=user_skills_test_data.UserSkillsTrainSkills.INPUT,
        )
        assert response.status_code == 200
        assert (
            response.json()
            == user_skills_test_data.UserSkillsTrainSkills.EXPECTED_OUTPUT
        )

        double_check = test_client.get(
            user_skills_test_data.UserSkillsGetAll.QUERY_PATH
        )
        load_neo4j(reset=True)
        import json

        print(json.dumps(double_check.json(), indent=4))

        assert double_check.status_code == 200
        assert (
            double_check.json()
            == user_skills_test_data.UserSkillsTrainSkills.EXPECTED_DOUBLE_CHECK
        )

    def test_userskills_forget_skills(self):
        response = test_client.delete(
            user_skills_test_data.UserSkillsForgetSkills.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()["message"]
            == user_skills_test_data.UserSkillsForgetSkills.EXPECTED_MESSAGE
        )

        double_check = test_client.get(
            user_skills_test_data.UserSkillsGetAll.QUERY_PATH
        )

        import json

        print(json.dumps(double_check.json(), indent=4))
        load_neo4j(reset=True)
        assert double_check.status_code == 200
        assert (
            double_check.json()
            == user_skills_test_data.UserSkillsForgetSkills.EXPECTED_DOUBLE_CHECK
        )

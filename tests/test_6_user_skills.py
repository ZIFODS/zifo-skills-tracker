import json

from fastapi.testclient import TestClient

from app import main
from app.models.skills import SkillCreate
from tests.expected_results.expected_userskills import UserSkills

test_client = TestClient(main.app)

unknown_skill = [{"name": "knitting", "category": "Programming_languages"}]
trained_skill = [{"name": "C++", "category": "Programming_languages"}]
untrained_skills = [{"name": "CDISC Study Data Tabulation Model", "category": "Data_Management"},
                    {"name": "Dutch", "category": "Languages"}]



class TestUserSkills:
    def test_userskills_get_all(self):
        response = test_client.get(f"/user/skills/")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json() == UserSkills.ALL_SKILLS

    def test_userskills_get_category(self):
        response = test_client.get(f"/user/skills/?category={trained_skill[0]['category']}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json() == UserSkills.FILTERED_SKILLS

    def test_userskills_get_learned_skill(self):
        response = test_client.get(f"/user/skills/{trained_skill[0]['name']}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json() == UserSkills.LEARNED_SKILL

    def test_userskills_get_unlearned_skill(self):
        response = test_client.get(f"/user/skills/{untrained_skills[0]['name']}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Skill not found for user"

    def test_userskills_train_trained_skill(self):
        response = test_client.post(
            "/user/skills/",
            json=trained_skill
        )
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 409
        assert response.json()["detail"] == \
               f"The following skills are already linked to the user: {trained_skill[0]['name']}"

    def test_userskills_forget_untrained_skill(self):
        response = test_client.delete(f"/user/skills/?skill_names={untrained_skills[0]['name']}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 409
        assert response.json()["detail"] == \
               f"The following skills are not linked to the user: {untrained_skills[0]['name']}"

    def test_userskills_train_unknown_skills(self):
        response = test_client.post(
            "/user/skills/",
            json=unknown_skill
        )
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Skill not found and could not be linked to user"

    def test_userskills_train_skills(self):
        response = test_client.post(
            "/user/skills/",
            json=untrained_skills
        )
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json() == UserSkills.TRAINED_SKILLS

    def test_userskills_forget_skills(self):
        response = test_client.delete(f"/user/skills/?skill_names={untrained_skills[0]['name']}"
                                      f"&skill_names={untrained_skills[1]['name']}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json()["message"] == \
               f"Removed {untrained_skills[0]['name']}, {untrained_skills[1]['name']} " \
               f"for user anthony_hopkins@gmail.com"

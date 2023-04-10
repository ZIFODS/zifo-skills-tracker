import pytest
from fastapi.testclient import TestClient

from app import main
from tests.expected_results.expected_consultants import CONSULTANTS

test_client = TestClient(main.app)

# Set delete_email - Delete consultant based on either unknown_email or existing_email (in CONSULTANTS class)
# unknown_email: is created before the delete test - DB data will be in inital state if create and delete tests pass,
#                but delete test will depend on successful create test
# existing_email: deletion will result in changed DB data after passed tests - mock data will have to be reloaded
#                 before next test, but delete test will be independent of create test
delete_email = CONSULTANTS.existing_email


class TestConsultants:
    def test_get_all_consultants(self):
        response = test_client.get(f"/consultants/")
        assert response.status_code == 200
        assert response.json() == CONSULTANTS.ALL

    @pytest.mark.dependency()
    def test_get_single_consultant(self):
        response = test_client.get(f"/consultants/{CONSULTANTS.existing_email}")
        assert response.status_code == 200
        assert response.json() == CONSULTANTS.expected_consultant_json

    def test_get_single_consultant_not_found(self):
        response = test_client.get(f"/consultants/{CONSULTANTS.unknown_email}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Consultant not found"

    def test_create_duplicate_consultant(self):
        response = test_client.post(
            "/consultants/",
            json={"name": CONSULTANTS.existing_consultant, "email": CONSULTANTS.existing_email},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Consultant already exists"

    def test_delete_consultant_not_found(self):
        response = test_client.delete(f"/consultants/{CONSULTANTS.unknown_consultant}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Consultant not found"

    @pytest.mark.dependency()
    def test_create_consultant(self):
        response = test_client.post(
            "/consultants/",
            json={"name": CONSULTANTS.unknown_consultant, "email": CONSULTANTS.unknown_email},
        )
        assert response.status_code == 200
        assert response.json() == CONSULTANTS.expected_new_consultant_json

    @pytest.mark.dependency(depends=["TestConsultants::test_get_single_consultant", "TestConsultants"
                                                                                    "::test_create_consultant"])
    def test_create_consultant_check_result(self):
        double_check = test_client.get(f"/consultants/{CONSULTANTS.unknown_email}")
        assert double_check.status_code == 200
        assert double_check.json() == CONSULTANTS.expected_new_consultant_json

    @pytest.mark.dependency()
    def test_delete_consultant(self):
        response = test_client.delete(f"/consultants/{delete_email}")
        assert response.status_code == 200
        assert response.json()["message"] == f"Deleted consultant {delete_email}"

    @pytest.mark.dependency(depends=["TestConsultants::test_get_single_consultant", "TestConsultants"
                                                                                    "::test_delete_consultant"])
    def test_delete_consultant_check_result(self):
        double_check = test_client.get(f"/consultants/{delete_email}")
        assert double_check.status_code == 404
        assert double_check.json()["detail"] == "Consultant not found"

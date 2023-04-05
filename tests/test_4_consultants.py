from fastapi.testclient import TestClient
from tests.expected_results.expected_consultants import CONSULTANTS

import pytest
from app import main
from tests.utils import load_mock_data

test_client = TestClient(main.app)

existing_consultant = "Duffy"
existing_email = "duffy@gmail.com"
unknown_consultant = "TEST GUY"
unknown_email = "test-guy@test.com"

expected_consultant_json = {
  "name": existing_consultant,
  "email": existing_email,
  "type": "Consultant"
}
expected_new_consultant_json = {
  "name": unknown_consultant,
  "email": unknown_email,
  "type": "Consultant"
}


class TestConsultants:
    def test_get_all_consultants(self):
        response = test_client.get(f"/consultants/")
        assert response.status_code == 200
        assert response.json() == CONSULTANTS

    def test_get_single_consultant(self):
        response = test_client.get(f"/consultants/{existing_email}")
        assert response.status_code == 200
        assert response.json() == expected_consultant_json

    def test_get_single_consultant_not_found(self):
        response = test_client.get(f"/consultants/{unknown_email}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Consultant not found"

    def test_create_duplicate_consultant(self):
        response = test_client.post(
            "/consultants/",
            json={"name": existing_consultant, "email": existing_email},
        )
        assert response.status_code == 409
        assert response.json()["detail"] == "Consultant already exists"

    def test_delete_consultant_not_found(self):
        response = test_client.delete(f"/consultants/{unknown_consultant}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Consultant not found"

    def test_create_consultant(self):
        response = test_client.post(
            "/consultants/",
            json={"name": unknown_consultant, "email": unknown_email},
        )
        assert response.status_code == 200
        assert response.json() == expected_new_consultant_json

        double_check = test_client.get(f"/consultants/{unknown_email}")
        assert double_check.status_code == 200
        assert double_check.json() == expected_new_consultant_json

    def test_delete_consultant(self):
        response = test_client.delete(f"/consultants/{unknown_email}")
        assert response.status_code == 200
        assert response.json()["message"] == f"Deleted consultant {unknown_email}"

        double_check = test_client.get(f"/consultants/{unknown_email}")
        assert double_check.status_code == 404
        assert double_check.json()["detail"] == "Consultant not found"




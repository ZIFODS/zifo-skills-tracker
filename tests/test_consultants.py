import pytest
from fastapi.testclient import TestClient

from app import main
from tests.expected_results import consultants_testdata

test_client = TestClient(main.app)


@pytest.mark.order(5)
class TestConsultants:
    def test_get_all_consultants(self):
        response = test_client.get(consultants_testdata.GetAllConsultants.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == consultants_testdata.GetAllConsultants.EXPECTED_RESULT

    @pytest.mark.dependency()
    def test_get_single_consultant(self):
        response = test_client.get(consultants_testdata.GetSingleConsultant.QUERY_PATH)
        assert response.status_code == 200
        assert (
            response.json() == consultants_testdata.GetSingleConsultant.EXPECTED_RESULT
        )

    def test_get_single_consultant_not_found(self):
        response = test_client.get(
            consultants_testdata.GetSingleConsultantNotFound.QUERY_PATH
        )
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == consultants_testdata.GetSingleConsultantNotFound.EXPECTED_DETAIL
        )

    def test_create_duplicate_consultant(self):
        response = test_client.post(
            consultants_testdata.CreateDuplicateConsultant.QUERY_PATH,
            json=consultants_testdata.CreateDuplicateConsultant.INPUT,
        )
        assert response.status_code == 409
        assert (
            response.json()["detail"]
            == consultants_testdata.CreateDuplicateConsultant.EXPECTED_DETAIL
        )

    def test_delete_consultant_not_found(self):
        response = test_client.delete(
            consultants_testdata.DeleteConsultantNotFound.QUERY_PATH
        )
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == consultants_testdata.DeleteConsultantNotFound.EXPECTED_DETAIL
        )

    @pytest.mark.dependency()
    def test_create_consultant(self):
        response = test_client.post(
            consultants_testdata.CreateConsultant.QUERY_PATH,
            json=consultants_testdata.CreateConsultant.INPUT,
        )
        assert response.status_code == 200
        assert response.json() == consultants_testdata.CreateConsultant.EXPECTED_RESULT

    @pytest.mark.dependency(
        depends=[
            "TestConsultants::test_get_single_consultant",
            "TestConsultants" "::test_create_consultant",
        ]
    )
    def test_create_consultant_check_result(self):
        double_check = test_client.get(
            consultants_testdata.CreateConsultantCheckResult.QUERY_PATH
        )
        assert double_check.status_code == 200
        assert (
            double_check.json()
            == consultants_testdata.CreateConsultantCheckResult.EXPECTED_RESULT
        )

    @pytest.mark.dependency()
    def test_delete_consultant(self):
        response = test_client.delete(consultants_testdata.DeleteConsultant.QUERY_PATH)
        assert response.status_code == 200
        assert (
            response.json()["message"]
            == consultants_testdata.DeleteConsultant.EXPECTED_MESSAGE
        )

    @pytest.mark.dependency(
        depends=[
            "TestConsultants::test_get_single_consultant",
            "TestConsultants" "::test_delete_consultant",
        ]
    )
    def test_delete_consultant_check_result(self):
        double_check = test_client.get(
            consultants_testdata.DeleteConsultantCheckResult.QUERY_PATH
        )
        assert double_check.status_code == 404
        assert (
            double_check.json()["detail"]
            == consultants_testdata.DeleteConsultantCheckResult.EXPECTED_DETAIL
        )

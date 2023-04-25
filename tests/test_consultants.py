from fastapi.testclient import TestClient

from app import main
from tests.expected_results import consultants_test_data
from tests.utils.load_mock_data import load_neo4j

test_client = TestClient(main.app)


class TestConsultants:
    def test_get_all_consultants(self):
        response = test_client.get(consultants_test_data.GetAllConsultants.QUERY_PATH)
        assert response.status_code == 200
        assert (
            response.json() == consultants_test_data.GetAllConsultants.EXPECTED_RESULT
        )

    def test_get_single_consultant(self):
        response = test_client.get(consultants_test_data.GetSingleConsultant.QUERY_PATH)
        assert response.status_code == 200
        assert (
            response.json() == consultants_test_data.GetSingleConsultant.EXPECTED_RESULT
        )

    def test_get_single_consultant_not_found(self):
        response = test_client.get(
            consultants_test_data.GetSingleConsultantNotFound.QUERY_PATH
        )
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == consultants_test_data.GetSingleConsultantNotFound.EXPECTED_DETAIL
        )

    def test_create_duplicate_consultant(self):
        response = test_client.post(
            consultants_test_data.CreateDuplicateConsultant.QUERY_PATH,
            json=consultants_test_data.CreateDuplicateConsultant.INPUT,
        )
        assert response.status_code == 409
        assert (
            response.json()["detail"]
            == consultants_test_data.CreateDuplicateConsultant.EXPECTED_DETAIL
        )

    def test_delete_consultant_not_found(self):
        response = test_client.delete(
            consultants_test_data.DeleteConsultantNotFound.QUERY_PATH
        )
        assert response.status_code == 404
        assert (
            response.json()["detail"]
            == consultants_test_data.DeleteConsultantNotFound.EXPECTED_DETAIL
        )

    def test_create_consultant(self):
        response = test_client.post(
            consultants_test_data.CreateConsultant.QUERY_PATH,
            json=consultants_test_data.CreateConsultant.INPUT,
        )
        assert response.status_code == 200
        assert response.json() == consultants_test_data.CreateConsultant.EXPECTED_RESULT

        double_check = test_client.get(
            consultants_test_data.CreateConsultant.QUERY_PATH_DOUBLE_CHECK
        )
        load_neo4j(reset=True)
        assert double_check.status_code == 200
        assert (
            double_check.json()
            == consultants_test_data.CreateConsultant.EXPECTED_DOUBLE_CHECK_RESULT
        )

    def test_delete_consultant(self):
        response = test_client.delete(consultants_test_data.DeleteConsultant.QUERY_PATH)
        assert response.status_code == 200
        assert (
            response.json()["message"]
            == consultants_test_data.DeleteConsultant.EXPECTED_MESSAGE
        )

        double_check = test_client.get(
            consultants_test_data.DeleteConsultant.QUERY_PATH
        )
        load_neo4j(reset=True)
        assert double_check.status_code == 404
        assert (
            double_check.json()["detail"]
            == consultants_test_data.DeleteConsultant.EXPECTED_DOUBLE_CHECK_DETAIL
        )

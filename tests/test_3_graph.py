import json

from fastapi.testclient import TestClient

from app import main
from tests.expected_results.expected_graph import Graph
from tests.utils.test_utils import encode_list_json, dictlist_to_dict

test_client = TestClient(main.app)


class TestGraph:

    def test_graph_consultant_unfiltered(self):
        response = test_client.get(f"/graph/?consultant={Graph.existing_consultant}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json() == Graph.DUFFY

    def test_empty_input(self):
        response = test_client.get(f"/graph/")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json() == {"nodes": [], "links": []}

    def test_graph_consultant_unfiltered_unknown(self):
        response = test_client.get(f"/graph/?consultant={Graph.unknown_consultant}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 404
        assert response.json()["detail"] == "A Consultant could not be found with the name provided."

    def test_graph_consultant_hide_categories(self):
        query_base_path = f"/graph/?consultant={Graph.existing_consultant}"
        response = test_client.get(query_base_path + Graph.query_path)
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json() == Graph.DUFFY_HIDDEN_CATEGORIES

    def test_graph_consultant_hide_all_categories(self):
        query_base_path = f"/graph/?consultant={Graph.existing_consultant}"
        response = test_client.get(query_base_path + Graph.query_path_all)
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json() == Graph.DUFFY_ALL_HIDDEN

    def test_graph_skills_scenario1(self):
        json_list = Graph.SCENARIOS_INPUT[0]
        print(f"Input:\n{json_list}")
        json_b64 = encode_list_json(json_list)
        print(f"Encoded JSON input:\n{json_b64}")
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SCENARIO1

    def test_graph_skills_scenario2(self):
        json_list = Graph.SCENARIOS_INPUT[1]
        print(f"Input:\n{json_list}")
        json_b64 = encode_list_json(json_list)
        print(f"Encoded JSON input:\n{json_b64}")
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SCENARIO2

    def test_graph_skills_scenario3(self):
        json_list = Graph.SCENARIOS_INPUT[2]
        print(f"Input:\n{json_list}")
        json_b64 = encode_list_json(json_list)
        print(f"Encoded JSON input:\n{json_b64}")
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SCENARIO3

    def test_graph_skills_scenario4(self):
        json_list = Graph.SCENARIOS_INPUT[3]
        print(f"Input:\n{json_list}")
        json_b64 = encode_list_json(json_list)
        print(f"Encoded JSON input:\n{json_b64}")
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SCENARIO4

    def test_graph_skills_scenario5(self):
        json_list = Graph.SCENARIOS_INPUT[4]
        print(f"Input:\n{json_list}")
        json_b64 = encode_list_json(json_list)
        print(f"Encoded JSON input:\n{json_b64}")
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SCENARIO5

    def test_graph_skills_scenario6(self):
        json_list = Graph.SCENARIOS_INPUT[5]
        print(f"Input:\n{json_list}")
        json_b64 = encode_list_json(json_list)
        print(f"Encoded JSON input:\n{json_b64}")
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SCENARIO6

    def test_graph_skills_scenario7(self):
        json_list = Graph.SCENARIOS_INPUT[6]
        print(f"Input:\n{json_list}")
        json_b64 = encode_list_json(json_list)
        print(f"Encoded JSON input:\n{json_b64}")
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SCENARIO7

    def test_graph_skills_scenario8(self):
        json_list = Graph.SCENARIOS_INPUT[7]
        print(f"Input:\n{json_list}")
        json_b64 = encode_list_json(json_list)
        print(f"Encoded JSON input:\n{json_b64}")
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SCENARIO8

    def test_graph_skills_hide_categories(self):
        json_list = Graph.SCENARIOS_INPUT[0]
        print(f"Input:\n{json_list}")
        json_b64 = encode_list_json(json_list)
        print(f"Encoded JSON input:\n{json_b64}")

        query_base_path = f"/graph/?skills={json_b64}"

        response = test_client.get(query_base_path + Graph.query_path)
        response_json = response.json()
        print(f"Response:\n{json.dumps(response_json, indent=4)}")

        assert response.status_code == 200

        # API sometimes switches ordering within the response "nodes" and "links" lists - to aviod failing the test
        # due to differing indices, the following statements check if each list item from expected results is in
        # actual result
        assert all([dictitem in response_json["nodes"] for dictitem in Graph.SKILL_HIDDEN_CATEGORIES["nodes"]] +
                   [dictitem in response_json["links"] for dictitem in Graph.SKILL_HIDDEN_CATEGORIES["links"]])

    def test_graph_skills_all_hidden(self):
        json_list = Graph.SCENARIOS_INPUT[0]
        print(f"Input:\n{json_list}")
        json_b64 = encode_list_json(json_list)
        print(f"Encoded JSON input:\n{json_b64}")

        query_base_path = f"/graph/?skills={json_b64}"

        response = test_client.get(query_base_path + Graph.query_path_all)
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SKILL_ALL_HIDDEN

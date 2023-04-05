from fastapi.testclient import TestClient
from tests.expected_results.expected_graph import Graph
import json
import base64

import pytest
import os

from app import main

test_client = TestClient(main.app)

existing_consultant = "Duffy"
existing_email = "duffy@gmail.com"

hidden_categories = ["Data Pipelines", "Products_And_Applications"]

existing_skill_1 = "CDISC Study Data Tabulation Model"
existing_skill_2 = "FAIR Data Principles"
existing_skill_3 = "Taxonomy Development & Management"

unknown_consultant = "TEST GUY"
unknown_email = "test-guy@test.com"
expected_consultant_json = {
  "name": "Duffy",
  "email": "duffy@gmail.com",
  "type": "Consultant"
}
expected_new_consultant_json = {
  "name": unknown_consultant,
  "email": unknown_email,
  "type": "Consultant"
}


class TestGraph:

    def test_graph_unfiltered(self):
        response = test_client.get(f"/graph/?consultant={existing_consultant}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json() == Graph.DUFFY

    def test_graph_unfiltered_unknown_consultant(self):
        response = test_client.get(f"/graph/?consultant={unknown_consultant}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 404
        assert response.json()["detail"] == "A Consultant could not be found with the name provided."

    def test_graph_hide_categories(self):
        query_path = f"/graph/?consultant={existing_consultant}"
        for category in hidden_categories:
            query_path += f"&hidden_categories={category}"

        response = test_client.get(query_path)
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        assert response.json() == Graph.DUFFY_HIDDEN_CATEGORIES

    def test_filter_single_skill(self):
        json_list = [{"name": existing_skill_1, "operator": "", "parenthesis": ""}]
        json_string = json.dumps(json_list)
        # convert to byte representation, encode with base64, convert to string:
        json_b64 = base64.urlsafe_b64encode(str.encode(json_string)).decode()

        print(json_b64)
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SINGLE_SKILL

    def test_filter_single_skill(self):
        json_list = [{"name": existing_skill_1, "operator": "", "parenthesis": ""}]
        json_string = json.dumps(json_list)
        # convert to byte representation, encode with base64, convert to string:
        json_b64 = base64.urlsafe_b64encode(str.encode(json_string)).decode()

        print(json_b64)
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SINGLE_SKILL

    def atest_filter_skills_and_or(self):
        json_list = [{"name": existing_skill_1, "operator": "", "parenthesis": "["},
                     {"name": existing_skill_2, "operator": "AND", "parenthesis": "]"},
                     {"name": existing_skill_3, "operator": "OR", "parenthesis": ""}]
        json_string = json.dumps(json_list)
        # convert to byte representation, encode with base64, convert to string:
        json_b64 = base64.urlsafe_b64encode(str.encode(json_string)).decode()
        print(json_string)
        print(json_b64)
        response = test_client.get(f"/graph/?skills={json_b64}")
        print(f"Response:\n{json.dumps(response.json(), indent=4)}")

        assert response.status_code == 200
        assert response.json() == Graph.SINGLE_SKILL


import pytest
from fastapi.testclient import TestClient

import tests.expected_results.graph_test_data as graph_test_data
from app import main

test_client = TestClient(main.app)


@pytest.mark.order(3)
class TestGraph:
    def test_graph_consultant_unfiltered(self):
        response = test_client.get(graph_test_data.GraphConsultantUnfiltered.QUERY_PATH)
        assert response.status_code == 200
        assert (
            response.json() == graph_test_data.GraphConsultantUnfiltered.EXPECTED_OUTPUT
        )

    def test_empty_input(self):
        response = test_client.get(graph_test_data.EmptyInput.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_test_data.EmptyInput.EXPECTED_OUTPUT

    def test_graph_consultant_unfiltered_unknown(self):
        response = test_client.get(
            graph_test_data.GraphConsultantUnfilteredUnknown.QUERY_PATH
        )
        assert response.status_code == 404
        assert (
            response.json()
            == graph_test_data.GraphConsultantUnfilteredUnknown.EXPECTED_OUTPUT
        )

    def test_graph_consultant_hide_categories(self):
        response = test_client.get(
            graph_test_data.GraphConsultantHideCategories.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphConsultantHideCategories.EXPECTED_OUTPUT
        )

    def test_graph_consultant_hide_all_categories(self):
        response = test_client.get(
            graph_test_data.GraphConsultantHideAllCategories.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphConsultantHideAllCategories.EXPECTED_OUTPUT
        )

    def test_graph_skillrules_one_skill(self):
        response = test_client.get(graph_test_data.GraphSkillRulesOneSkill.QUERY_PATH)
        assert response.status_code == 200
        assert (
            response.json() == graph_test_data.GraphSkillRulesOneSkill.EXPECTED_OUTPUT
        )

    def test_graph_skillrules_two_skills_and(self):
        response = test_client.get(
            graph_test_data.GraphSkillRulesTwoSkillsAnd.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphSkillRulesTwoSkillsAnd.EXPECTED_OUTPUT
        )

    def test_graph_skillrules_three_skills_or(self):
        response = test_client.get(
            graph_test_data.GraphSkillRulesThreeSkillsOr.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphSkillRulesThreeSkillsOr.EXPECTED_OUTPUT
        )

    def test_graph_skillrules_three_skills_and_or(self):
        response = test_client.get(
            graph_test_data.GraphSkillRulesThreeSkillsAndOr.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphSkillRulesThreeSkillsAndOr.EXPECTED_OUTPUT
        )

    def test_graph_skillrules_three_skills_parenthesis(self):
        response = test_client.get(
            graph_test_data.GraphSkillRulesThreeSkillsParenthesis.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphSkillRulesThreeSkillsParenthesis.EXPECTED_OUTPUT
        )

    def test_graph_skillrules_three_skills_parenthesis_missing(self):
        response = test_client.get(
            graph_test_data.GraphSkillRulesThreeSkillsParenthesisMissing.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphSkillRulesThreeSkillsParenthesisMissing.EXPECTED_OUTPUT
        )

    def test_graph_skillrules_four_skills_parenthesis(self):
        response = test_client.get(
            graph_test_data.GraphSkillRulesFourSkillsParenthesis.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphSkillRulesFourSkillsParenthesis.EXPECTED_OUTPUT
        )

    def test_graph_skillrules_five_skills_two_parenthesis(self):
        response = test_client.get(
            graph_test_data.GraphSkillRulesFiveSkillsTwoParenthesis.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphSkillRulesFiveSkillsTwoParenthesis.EXPECTED_OUTPUT
        )

    def test_graph_skillrules_hide_categories(self):
        response = test_client.get(
            graph_test_data.GraphSkillRulesHideCategories.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphSkillRulesHideCategories.EXPECTED_OUTPUT
        )

    def test_graph_skills_all_hidden(self):
        response = test_client.get(
            graph_test_data.GraphSkillRulesHideAllCategories.QUERY_PATH
        )
        assert response.status_code == 200
        assert (
            response.json()
            == graph_test_data.GraphSkillRulesHideAllCategories.EXPECTED_OUTPUT
        )

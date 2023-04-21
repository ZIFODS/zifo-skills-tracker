import pytest

from fastapi.testclient import TestClient

from app import main
import tests.expected_results.graph_testdata as graph_testdata

test_client = TestClient(main.app)


@pytest.mark.order(3)
class TestGraph:
    def test_graph_consultant_unfiltered(self):
        response = test_client.get(graph_testdata.GraphConsultantUnfiltered.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphConsultantUnfiltered.EXPECTED_OUTPUT

    def test_empty_input(self):
        response = test_client.get(graph_testdata.EmptyInput.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.EmptyInput.EXPECTED_OUTPUT

    def test_graph_consultant_unfiltered_unknown(self):
        response = test_client.get(graph_testdata.GraphConsultantUnfilteredUnknown.QUERY_PATH)
        assert response.status_code == 404
        assert response.json() == graph_testdata.GraphConsultantUnfilteredUnknown.EXPECTED_OUTPUT

    def test_graph_consultant_hide_categories(self):
        response = test_client.get(graph_testdata.GraphConsultantHideCategories.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphConsultantHideCategories.EXPECTED_OUTPUT

    def test_graph_consultant_hide_all_categories(self):
        response = test_client.get(graph_testdata.GraphConsultantHideAllCategories.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphConsultantHideAllCategories.EXPECTED_OUTPUT

    def test_graph_skillrules_one_skill(self):
        response = test_client.get(graph_testdata.GraphSkillRulesOneSkill.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphSkillRulesOneSkill.EXPECTED_OUTPUT

    def test_graph_skillrules_two_skills_and(self):
        response = test_client.get(graph_testdata.GraphSkillRulesTwoSkillsAnd.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphSkillRulesTwoSkillsAnd.EXPECTED_OUTPUT

    def test_graph_skillrules_three_skills_or(self):
        response = test_client.get(graph_testdata.GraphSkillRulesThreeSkillsOr.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphSkillRulesThreeSkillsOr.EXPECTED_OUTPUT

    def test_graph_skillrules_three_skills_and_or(self):
        response = test_client.get(graph_testdata.GraphSkillRulesThreeSkillsAndOr.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphSkillRulesThreeSkillsAndOr.EXPECTED_OUTPUT

    def test_graph_skillrules_three_skills_parenthesis(self):
        response = test_client.get(graph_testdata.GraphSkillRulesThreeSkillsParenthesis.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphSkillRulesThreeSkillsParenthesis.EXPECTED_OUTPUT

    def test_graph_skillrules_three_skills_parenthesis_missing(self):
        response = test_client.get(graph_testdata.GraphSkillRulesThreeSkillsParenthesisMissing.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphSkillRulesThreeSkillsParenthesisMissing.EXPECTED_OUTPUT

    def test_graph_skillrules_four_skills_parenthesis(self):
        response = test_client.get(graph_testdata.GraphSkillRulesFourSkillsParenthesis.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphSkillRulesFourSkillsParenthesis.EXPECTED_OUTPUT

    def test_graph_skillrules_five_skills_two_parenthesis(self):
        response = test_client.get(graph_testdata.GraphSkillRulesFiveSkillsTwoParenthesis.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphSkillRulesFiveSkillsTwoParenthesis.EXPECTED_OUTPUT

    def test_graph_skillrules_hide_categories(self):
        response = test_client.get(graph_testdata.GraphSkillRulesHideCategories.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphSkillRulesHideCategories.EXPECTED_OUTPUT

    def test_graph_skills_all_hidden(self):
        response = test_client.get(graph_testdata.GraphSkillRulesHideAllCategories.QUERY_PATH)
        assert response.status_code == 200
        assert response.json() == graph_testdata.GraphSkillRulesHideAllCategories.EXPECTED_OUTPUT

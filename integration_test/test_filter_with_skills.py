import base64
import json
import sys
from pathlib import Path

import requests

root_dir = (Path(__file__).parent / "../").resolve()
sys.path.append(str(root_dir))

from app.models.graph import Rule  # noqa: E402
from integration_test.expected_results import ExpectedResults  # noqa: E402
from pipeline.src.utils import Categories  # noqa: E402


def base64_encode(query: list[Rule]) -> str:
    """
    Encode JSON as base64 string for filtering endpoint.

    Arguments
    ---------
    query : list[Rule]
        JSON search list query

    Returns
    -------
    str
        base64 encoded string representing JSON
    """
    json_str = json.dumps(query)
    json_encode = json_str.encode("utf-8")
    return base64.urlsafe_b64encode(json_encode).decode("utf-8")


def generate_all_hidden_query() -> str:
    """
    Generate hidden categories query for filtering endpoint to hide all categories.

    Returns
    -------
    query : str
        query to hide all categories
    """
    query = ""
    for category in Categories:
        query += "&hidden_categories=" + category.value
    return query


def test_single_redux_skill():
    query = base64_encode(
        [
            {
                "group": "Miscellaneous",
                "name": "REDUX",
                "operator": "",
                "parenthesis": "",
            }
        ]
    )
    url = f"http://localhost:8080/skills/?skills={query}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == ExpectedResults.LUKE_EVANS


def test_dotnet_and_csharp():
    query = base64_encode(
        [
            {
                "group": "Programming_languages",
                "name": ".Net",
                "operator": "",
                "parenthesis": "",
            },
            {
                "group": "Programming_languages",
                "name": "C#",
                "operator": "AND",
                "parenthesis": "",
            },
        ]
    )
    url = f"http://localhost:8080/skills/?skills={query}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == ExpectedResults.GARETH_BALE


def test_redux_or_pipeline_pilot():
    query = base64_encode(
        [
            {
                "group": "Miscellaneous",
                "name": "REDUX",
                "operator": "",
                "parenthesis": "",
            },
            {
                "group": "Science",
                "name": "BIOVIA Pipeline Pilot",
                "operator": "OR",
                "parenthesis": "",
            },
        ]
    )
    url = f"http://localhost:8080/skills/?skills={query}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == ExpectedResults.LUKE_EVANS


def test_python_or_r_studio_and_chinese_or_hindi_no_brackets():
    query = base64_encode(
        [
            {
                "group": "Programming_languages",
                "name": "Python",
                "operator": "",
                "parenthesis": "",
            },
            {
                "group": "Programming_languages",
                "name": "R Studio",
                "operator": "AND",
                "parenthesis": "",
            },
            {
                "group": "Languages",
                "name": "Chinese",
                "operator": "OR",
                "parenthesis": "",
            },
            {
                "group": "Languages",
                "name": "Hindi",
                "operator": "AND",
                "parenthesis": "",
            },
        ]
    )
    url = f"http://localhost:8080/skills/?skills={query}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == ExpectedResults.TARON_EDGERTON


def test_python_or_r_studio_and_chinese_or_hindi_with_brackets():
    query = base64_encode(
        [
            {
                "group": "Programming_languages",
                "name": "Python",
                "operator": "",
                "parenthesis": "[",
            },
            {
                "group": "Programming_languages",
                "name": "R Studio",
                "operator": "AND",
                "parenthesis": "]",
            },
            {
                "group": "Languages",
                "name": "Chinese",
                "operator": "OR",
                "parenthesis": "[",
            },
            {
                "group": "Languages",
                "name": "Hindi",
                "operator": "AND",
                "parenthesis": "]",
            },
        ]
    )
    url = f"http://localhost:8080/skills/?skills={query}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == ExpectedResults.EMPTY


def test_single_redux_skill_with_miscellaneous_and_programming_languages_hidden():
    skills_query = base64_encode(
        [
            {
                "group": "Miscellaneous",
                "name": "REDUX",
                "operator": "",
                "parenthesis": "",
            }
        ]
    )
    hidden_categories_query = "Miscellaneous&hidden_categories=Programming_languages"
    url = f"http://localhost:8080/skills/?skills={skills_query}&hidden_categories={hidden_categories_query}"
    response = requests.get(url)
    assert response.status_code == 200
    assert (
        response.json()
        == ExpectedResults.LUKE_EVANS_NO_MISCELLANEOUS_NO_PROGRAMMING_LANGUAGES
    )


def test_single_redux_skill_with_all_skill_categories_hidden():
    skills_b64_query = base64_encode(
        [
            {
                "group": "Miscellaneous",
                "name": "REDUX",
                "operator": "",
                "parenthesis": "",
            }
        ]
    )
    hidden_categories_query = generate_all_hidden_query()
    url = f"http://localhost:8080/skills/?skills={skills_b64_query}{hidden_categories_query}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == ExpectedResults.LUKE_EVANS_ALL_HIDDEN

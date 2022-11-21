import requests

from expected_results import ExpectedResults

def test_consultant_luke_evans():
    query = "Luke Evans"
    url = f"http://localhost:8080/consultant/?consultant_name={query}"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == ExpectedResults.LUKE_EVANS
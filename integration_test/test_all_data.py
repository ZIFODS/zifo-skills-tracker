import pytest
import requests

from pathlib import Path
import sys


@pytest.fixture()
def all_data_response():
    return requests.get("http://localhost:8080/all")


class TestAllData:
    def test_successful_response(self, all_data_response):
        assert all_data_response.status_code == 200

    def test_node_length_correct(self, all_data_response):
        result = all_data_response.json()
        assert len(result["nodes"]) == 109

    def test_link_length_correct(self, all_data_response):
        result = all_data_response.json()
        assert len(result["links"]) == 173

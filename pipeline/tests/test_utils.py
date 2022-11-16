import os

import pandas as pd
import pytest
from dotenv import load_dotenv
from ..src.utils import pull_survey_data_from_d3, filter_survey_data
from .. import tests


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv(dotenv_path=os.path.join(str(tests.__path__), ".env.test.local"))


def test_pull_survey_data_from_d3():
    data = pull_survey_data_from_d3()
    assert isinstance(data, pd.DataFrame)


def test_filter_survey_data():
    data = pd.DataFrame(
        {
            "ID": [0, 1, 2, 3, 4, 5, 6],
            "Completion time": [
                "1/5/22 19:12:15",
                "1/5/22 17:12:15",
                "7/21/22 10:50:11",
                "7/25/22 09:52:11",
                "7/25/22 09:52:11",
                "7/25/22 12:25:18",
                "8/25/22 10:26:01"
            ],
            "Email": [
                "test1@test.com",
                "test1@test.com",
                "test2@test.com",
                "test2@test.com",
                "test2@test.com",
                "test3@test.com",
                "test3@test.com"

            ],
            "Name": [
                "test1",
                "test1",
                "test2",
                "test2",
                "test2",
                "test3",
                "test3"
            ],
        }
    )
    data = filter_survey_data(data=data)
    assert isinstance(data, pd.DataFrame)
    assert {0, 4, 6} == set(data["ID"].values.tolist())




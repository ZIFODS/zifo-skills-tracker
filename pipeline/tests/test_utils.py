import os

import pandas as pd
from ..src.utils import pull_survey_data_from_s3, filter_survey_data


def test_pull_survey_data_from_s3():
    """
    Function should pull a Pandas DataFrame from S3 using Env variables
    """
    data = pull_survey_data_from_s3()
    assert isinstance(data, pd.DataFrame)


def test_filter_survey_data():
    """
    Function should take a Pandas DataFrame with duplicate entries and filter to retain
    row for each individual (identified by Name and Email) from the most recent entry.
    """
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




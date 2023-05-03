import base64
import json


def encode_list_json(list_in: list) -> str:
    """
    convert list to JSON string and encode with base64

    Parameters
    ----------
    list_in : list to convert to base64 JSON string

    Returns
    -------
    String : base64 encoded string object containing list_in in JSON format
    """
    json_string = json.dumps(list_in)
    # convert to byte representation, encode with base64, convert to string:
    return base64.urlsafe_b64encode(str.encode(json_string)).decode()


def query_add_hidden_categories(base_query: str, hidden_categories: list[str]) -> str:
    """
    Appends hidden categories from a list to the base query path.

    Parameters
    ----------
    base_query : graph query without hiddencategories, e.g. "/graph/?consultant=Duffy"
    hidden_categories: list of strings containing category names to hide, e.g. ["Methodology", "R_And_D_Processes"]

    Returns
    -------
    query : full query path with hidden categories.
            base_query + [&hidden_categories={category} for category in hidden_categories]
    """

    return base_query + "".join(
        [f"&hidden_categories={category}" for category in hidden_categories]
    )

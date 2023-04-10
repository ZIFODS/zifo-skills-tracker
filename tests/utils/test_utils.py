import json
import base64


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


def dictlist_to_dict(list_in: list[dict]) -> dict:
    """
    Convert list of dicts to dict of dicts - list items must be dicts containing an "id" key, each. "id" values are
    used as keys in new dict. Used to convert the lists of "nodes" and "links" recieved in API responses. This makes
    test independent of list sorting, which occasionally changed in the responses for some reason.

    Parameters
    ----------
    list_in : List of dicts to convert to dicts of dicts

    Returns
    -------

    """
    tempdict = {}
    for dictionary in list_in:
        tempdict[dictionary["id"]] = dictionary

    return tempdict

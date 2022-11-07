"""
Convert existing skills.json to d3.js graph compatible form
"""

def neo4j_to_d3_json(neo4j_json):

    d3_json = {"nodes": [], "links": []}

    for object in neo4j_json:
        if object["type"] == "node":
            d3_json["nodes"].append(
                {
                    "id": int(object["id"]),
                    "name": object["properties"]["Name"],
                    "group": object["labels"][0]
                }
            )

        elif object["type"] == "relationship":
            d3_json["links"].append(
                {
                    "id": int(object["id"]),
                    "source": int(object["start"]["id"]),
                    "target": int(object["end"]["id"]),
                }
            )

    return d3_json

        
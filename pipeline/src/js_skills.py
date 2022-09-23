"""
Convert existing skills.json to d3.js graph compatible form
"""

def neo4j_to_d3_json(neo4j_json):

    d3_json = {"nodes": [], "links": []}

    for object in neo4j_json:
        if object["type"] == "node":
            d3_json["nodes"].append(
                {
                    "id": object["id"],
                    "name": object["properties"]["Name"],
                    "group": object["labels"][0]
                }
            )

        elif object["type"] == "relationship":
            d3_json["links"].append(
                {
                    "source": object["start"]["id"],
                    "target": object["end"]["id"],
                    "value": 1
                }
            )

    return d3_json
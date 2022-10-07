"""
Convert existing skills.json to d3.js graph compatible form
"""

import json


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

if __name__ == "__main__":
    with open("pipeline/src/neo4j_skills.json", "r") as neo4j_file:
        neo4j_json = json.load(neo4j_file)

        d3_json = neo4j_to_d3_json(neo4j_json)

        with open("frontend/src/data/d3_skills.json", "w+") as d3_file:
            json.dump(d3_json, d3_file, indent=4)

        
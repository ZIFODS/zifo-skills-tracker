# Graph endpoint

This document describes the process by which a skill search query is processed and used to generate Cypher queries for Neo4j.

A skill search query is trying to find the consultants that know a particular set of skills and retrieve them along with the skills that they know.

There is also the option to hide certain skill categories from the final results.

## Skill search query

The skill search query is a base64 encoded JSON list of objects which each object containing the following fields:

- `name`: the name of the skill
- `operator`: the operator that applies to the previous skill or bracket: either `AND`, `OR` or no value.
- `parenthesis`: whether the skill is at the start or end of a bracket: either `[` or `]` or no value.

Each of these JSON objects in the list has been represented in the endpoint as a `Rule` object.

For example, a skill search query that looks for consultants that know both [`Java` and `Python`] or know `C++` would be:

```
[
    {
        name: "Java",
        operator: "",
        parenthesis: "["
    },
    {
        name: "Python",
        operator: "AND",
        parenthesis: "]"
    },
    {
        name: "C++",
        operator: "OR",
        parenthesis: ""
    }
]
```

The JSON list is encoded using base64 by the frontend and then passed as a query parameter to the `/graph` endpoint, where it is decoded and processed to generate a Cypher query. The encoding and subsequent decoding has been done to minimise the size of the URL.

## Cypher

The Cypher query is generated using information from the components described previously.

The general premise is that we are matching Consultants who have `KNOWS` relationships to skills that fit certain criteria.

Generally, we are creating an initial `MATCH` statement that gets all of the consultants that know at least one skill. We then use a WHERE clause and define successive MATCH statements related by AND and OR operators to filter the consultants that know the skills that we are looking for.

The brackets defined in the rule list are also transferred to the Cypher query.

Let's take an example rule list and see how we generate the Cypher step-by-step.

```
[
    {
        name: "Java",
        operator: "",
        parenthesis: "["
    },
    {
        name: "Python",
        operator: "AND",
        parenthesis: "]"
    },
    {
        name: "C++",
        operator: "OR",
        parenthesis: ""
    }
]
```

First, we get all Consultants that know `Java`:

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE (c)-[:KNOWS]->(:Skill {name: "Java"})
```

For the second rule, we need to get all Consultants that also know `Python`. Given the bracket definitions, we need to get all Consultants that know `Java` and `Python` before we combine that result with the Consultants that know `C++` for the third rule. To do this, we simply add the bracket to the Cypher query:

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE ( (c)-[:KNOWS]->(:Skill {name: "Java"}) AND (c)-[:KNOWS]->(:Skill {name: "Python"}) )
```

We then simply add the third rule using an `OR` statement:

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE ( (c)-[:KNOWS]->(:Skill {name: "Java"}) AND (c)-[:KNOWS]->(:Skill {name: "Python"}) )
OR (c)-[:KNOWS]->(:Skill {name: "C++"})
```

## Compiling results

After the query above is performed, the consultants stored in the `c` variable will match those defined by our query. We then need to get the skills that they know and return them as part of the result.

The way we do this is dependent on whether skill categories have been defined to be hidden from the result (more in this in next section) but ultimately we are first using a `MATCH` to get the consultants and their known skills, then separating out the nodes and relationships for the resulting data and returning them as a JSON object.

The final query for our example would look like this:

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE ( (c)-[:KNOWS]->(:Skill {name: "Java"}) AND (c)-[:KNOWS]->(:Skill {name: "Python"}) )
OR (c)-[:KNOWS]->(:Skill {name: "C++"})
MATCH p=(c)-[:KNOWS]->(:Skill)
UNWIND nodes(p) as n UNWIND relationships(p) as r
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz,
collect( distinct {id: ID(r), source: ID(startnode(r)), taret: ID(endnode(r))}) as rz
RETURN {nodes: nz, links: rz}
```

The return value will look something like this:

```
{
    "nodes": [
        {
            "id": 1,
            "name": "John Smith",
            "type": "Consultant",
            "email": "john.smith@zifornd.com"
        },
        {
            "id": 2,
            "name": "Python",
            "type": "Skill",
            "category": "Programming_Languages"
        },
    ],
    "links": [
        {
            "id": 1,
            "source": 1
            "target": 2,
        }
    ]
}
```

## Hiding skill categories

If specific skill categories, but not all, have been selected to be hidden, we use the `WHERE NOT` statement to filter. Here's how it looks with our example, ignoring the query up to the final `MATCH` statement:

```
...
...
MATCH p=(c)-[:KNOWS]->(s:Skill)
WHERE NOT s.category IN ["Programming_Languages", "Data_Management"]
UNWIND nodes(p) as n UNWIND relationships(p) as r
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz,
collect( distinct {id: ID(r), source: ID(startnode(r)), taret: ID(endnode(r))}) as rz
RETURN {nodes: nz, links: rz}
```

If all skill categories have been selected to be hidden from the final results, we simply take the filtered Consultant nodes and return them, without defining that they should have any relationships:

```
...
MATCH p=(c)
UNWIND nodes(p) as n
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz
RETURN {nodes: nz, links: []}
```

## Query scenarios

Some other rule list scenarios and their associated Cypher queries are shown below:

### Scenario 1

```
[
    {
        name: "Java",
        operator: "",
        parenthesis: ""
    }
]
```

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE (c)-[:KNOWS]->(:Skill {name: "Java"})
MATCH p=(c)-[:KNOWS]->(:Skill)
UNWIND nodes(p) as n UNWIND relationships(p) as r
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz,
collect( distinct {id: ID(r), source: ID(startnode(r)), taret: ID(endnode(r))}) as rz
RETURN {nodes: nz, links: rz}
```

### Scenario 2

```
[
    {
        name: "Java",
        operator: "",
        parenthesis: ""
    },
    {
        name: "ELOG",
        operator: "AND",
        parenthesis: ""
    }
]
```

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE (c)-[:KNOWS]->(:Skill {name: "Java"}) AND (c)-[:KNOWS]->(:Skill {name: "ELOG"})
MATCH p=(c)-[:KNOWS]->(:Skill)
UNWIND nodes(p) as n UNWIND relationships(p) as r
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz,
collect( distinct {id: ID(r), source: ID(startnode(r)), taret: ID(endnode(r))}) as rz
RETURN {nodes: nz, links: rz}
```

### Scenario 3

```
[
    {
        name: "Java",
        operator: "",
        parenthesis: ""
    },
    {
        name: "Python",
        operator: "OR",
        parenthesis: ""
    },
    {
        name: "C++",
        operator: "OR",
        parenthesis: ""
    }
]
```

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE (c)-[:KNOWS]->(:Skill {name: "Java"}) OR (c)-[:KNOWS]->(:Skill {name: "Python"}) OR (c)-[:KNOWS]->(:Skill {name: "C++"})
MATCH p=(c)-[:KNOWS]->(:Skill)
UNWIND nodes(p) as n UNWIND relationships(p) as r
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz,
collect( distinct {id: ID(r), source: ID(startnode(r)), taret: ID(endnode(r))}) as rz
RETURN {nodes: nz, links: rz}
```

### Scenario 4

```
[
    {
        name: "Java",
        operator: "",
        parenthesis: ""
    },
    {
        name: "Python",
        operator: "AND",
        parenthesis: ""
    },
    {
        name: "C++",
        operator: "OR",
        parenthesis: ""
    }
]
```

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE (c)-[:KNOWS]->(:Skill {name: "Java"}) AND (c)-[:KNOWS]->(:Skill {name: "Python"}) OR (c)-[:KNOWS]->(:Skill {name: "C++"})
MATCH p=(c)-[:KNOWS]->(:Skill)
UNWIND nodes(p) as n UNWIND relationships(p) as r
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz,
collect( distinct {id: ID(r), source: ID(startnode(r)), taret: ID(endnode(r))}) as rz
RETURN {nodes: nz, links: rz}
```

### Scenario 5

```
[
    {
        name: "Java",
        operator: "",
        parenthesis: "["
    },
    {
        name: "Python",
        operator: "AND",
        parenthesis: "]"
    },
    {
        name: "C++",
        operator: "OR",
        parenthesis: ""
    }
]
```

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE ( (c)-[:KNOWS]->(:Skill {name: "Java"}) AND (c)-[:KNOWS]->(:Skill {name: "Python"}) )
OR (c)-[:KNOWS]->(:Skill {name: "C++"})
MATCH p=(c)-[:KNOWS]->(:Skill)
UNWIND nodes(p) as n UNWIND relationships(p) as r
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz,
collect( distinct {id: ID(r), source: ID(startnode(r)), taret: ID(endnode(r))}) as rz
RETURN {nodes: nz, links: rz}
```

### Scenario 6

Note: Closing parenthesis can be omitted in the UI and JSON, it is automatically added after the last item in the cypher query.

```
[
    {
        name: "Java",
        operator: "",
        parenthesis: ""
    },
    {
        name: "XML",
        operator: "AND",
        parenthesis: "["
    },
    {
        name: "ELOG",
        operator: "OR",
        parenthesis: ""
    }
]
```

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE (c)-[:KNOWS]->(:Skill {name: "Java"})
AND ( (c)-[:KNOWS]->(:Skill {name: "XML"}) OR (c)-[:KNOWS]->(:Skill {name: "ELOG"}) )
MATCH p=(c)-[:KNOWS]->(:Skill)
UNWIND nodes(p) as n UNWIND relationships(p) as r
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz,
collect( distinct {id: ID(r), source: ID(startnode(r)), taret: ID(endnode(r))}) as rz
RETURN {nodes: nz, links: rz}
```

### Scenario 7

```
[
    {
        name: "Java",
        operator: "",
        parenthesis: ""
    },
    {
        name: "XML",
        operator: "AND",
        parenthesis: "["
    },
    {
        name: "ELOG",
        operator: "OR",
        parenthesis: ""
    },
    {
        name: "SQL",
        operator: "AND",
        parenthesis: "]"
    }
]
```

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE (c)-[:KNOWS]->(:Skill {name: "Java"})
AND ( (c)-[:KNOWS]->(:Skill {name: "XML"}) OR (c)-[:KNOWS]->(:Skill {name: "ELOG"}) AND (c)-[:KNOWS]->(:Skill {name: "SQL"}) )
MATCH p=(c)-[:KNOWS]->(:Skill)
UNWIND nodes(p) as n UNWIND relationships(p) as r
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz,
collect( distinct {id: ID(r), source: ID(startnode(r)), taret: ID(endnode(r))}) as rz
RETURN {nodes: nz, links: rz}
```

### Scenario 8

```
[
    {
        name: "Java",
        operator: "",
        parenthesis: ""
    },
    {
        name: "SQL",
        operator: "OR",
        parenthesis: "["
    },
    {
        name: "Perl",
        operator: "AND",
        parenthesis: "]"
    },
    {
        name: "SQL",
        operator: "OR",
        parenthesis: "["
    },
    {
        name: "Assembler",
        operator: "AND",
        parenthesis: "]"
    }
]
```

```
MATCH (c:Consultant)-[:KNOWS]->(:Skill)
WHERE (c)-[:KNOWS]->(:Skill {name: "Java"})
OR ( (c)-[:KNOWS]->(:Skill {name: "SQL"}) AND (c)-[:KNOWS]->(:Skill {name: "Perl"}) )
OR ( (c)-[:KNOWS]->(:Skill {name: "SQL"}) AND (c)-[:KNOWS]->(:Skill {name: "Assembler"}) )
MATCH p=(c)-[:KNOWS]->(:Skill)
UNWIND nodes(p) as n UNWIND relationships(p) as r
with collect( distinct {id: ID(n), name: n.name, type: labels(n)[0], email: n.email, category: n.category}) as nz,
collect( distinct {id: ID(r), source: ID(startnode(r)), taret: ID(endnode(r))}) as rz
RETURN {nodes: nz, links: rz}
```

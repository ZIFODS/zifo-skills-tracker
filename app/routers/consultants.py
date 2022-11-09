import base64
from typing import List, TypedDict, NamedTuple
from fastapi import APIRouter, Query
from app.utils import neo4j_to_d3_cypher
import json

from pipeline.src.neo4j_connect import Neo4jConnection

consultants_router = APIRouter()

"""
Get consultants who know BIOVIA ONELab along with their known skills but don't return skills in ScienceApps or Process categories:

MATCH pa=(c:Consultant)-[:KNOWS]->(sa) where sa.Name = 'BIOVIA ONELab'
unwind nodes(pa) as na
MATCH pb=(na)-[:KNOWS]->() 
WHERE NONE(n IN nodes(pb) WHERE n:ScienceApps OR n:Process) 
unwind nodes(pb) as nb unwind relationships(pb) as rb 
with collect( distinct {id: ID(nb), name: nb.Name, group: labels(nb)[0]}) as nzz, 
collect( distinct {id: ID(rb), source: ID(startnode(rb)), target: ID(endnode(rb))}) as rzz 
RETURN {nodes: nzz, links: rzz}
"""

def char(num: int):
    return chr(num + 97)

def determine_all_categories_hidden(conn: Neo4jConnection, hidden_categories: list[str]):
    """
    Determine if all categories in current data have been selected to be hidden.
    Retrieve all labels in data, sort and then compare to sorted user category selection.

    Arguments
    ---------
    conn : Neo4jConnection
        custom neo4j database driver
    hidden_categories: list[str]
        list of categories hidden by user

    Returns
    -------
    all_hidden : bool
        if all categories in data have been hidden by user 
    """
    if hidden_categories:
        # retrieve all labels and therefore categories in data
        all_labels_result = conn.query("MATCH (n) RETURN COLLECT(DISTINCT n.Group) ")
        all_categories = all_labels_result[0].values("COLLECT(DISTINCT n.Group)")[0]
        if "Consultant" in all_categories:
            all_categories.remove("Consultant")

        all_categories.sort()
        hidden_categories.sort()
        if all_categories == hidden_categories:
            return True

    return False

class Rule(TypedDict):
    name: str
    operator: str
    parenthesis: str

class BracketIndexes(NamedTuple):
    start: int
    end: int

def determine_effective_bracket_indexes(rules: list[Rule]) -> list[BracketIndexes]:
    """
    Determine index ranges of effective brackets in search list.
    If bracket not closed, end of search list is classed as closing bracket.
    Returns empty list if no parenthesis present.
    
    Arguments
    ---------
    rules : list[Rule]
        list of rules in search list

    Returns
    -------
    bracket_idx_list : list[BracketIndexes]
    """
    bracket_idx_list = []
    final_i = len(rules) - 1

    for i, rule in enumerate(rules):
        
        current_parenthesis = rule["parenthesis"]

        # If index at start of bracket, add index pair with start and end equal to index
        if i == 0:
            bracket_idx_list.append(BracketIndexes(i, i))

        elif current_parenthesis == "[":
            bracket_idx_list.append(BracketIndexes(i, i))

        else:
            previous_parenthesis = rules[i-1]["parenthesis"]

            if previous_parenthesis == "]":
                bracket_idx_list.append(BracketIndexes(i, i))

        # If index at end of bracket, extend most recent index pair to current index
        if bracket_idx_list:
            last_bracket_idx = bracket_idx_list[-1]
            if i == final_i:
                bracket_idx_list[-1] = BracketIndexes(last_bracket_idx.start, i)

            elif current_parenthesis == "]":
                bracket_idx_list[-1] = BracketIndexes(last_bracket_idx.start, i)

            else:
                next_parenthesis = rules[i + 1]["parenthesis"]

                if next_parenthesis == "[":
                    bracket_idx_list[-1] = BracketIndexes(last_bracket_idx.start, i)
   
    return bracket_idx_list

class OrStatus(NamedTuple):
    is_or: bool
    start_or: bool
    end_or: bool

class OrStatusProcesser:
    def _not(self):
        return OrStatus(False, False, False)

    def _start(self):
        return OrStatus(True, True, False)

    def _middle(self):
        return OrStatus(True, False, False)

    def _end(self):
        return OrStatus(True, False, True)

    def process(self, i: int, rules: list[Rule]) -> OrStatus:
        """
        Determine if current index is within, first element of, or last element of OR sequence.

        Arguments
        ---------
        i : int
            current index of rule in search list
        rules: list[Rule]
            all rules in search list
        
        Returns
        -------
        or_status : OrStatus
            OR sequence information for current rule
        """
        rule = rules[i]

        final_i = len(rules) - 1

        current_operator = rule["operator"]
        current_parenthesis = rule["parenthesis"]

        if i != final_i:
            next_operator = rules[i + 1]["operator"]
            next_parenthesis = rules[i + 1]["parenthesis"]

            # For first rule, if next operator is OR then it's start of OR sequence, otherwise not.
            if i == 0:
                if next_operator == "OR":
                    return self._start()
                else:
                    return self._not()

            else:
                previous_parenthesis = rules[i - 1]["parenthesis"]

                # If neither the current nor next operators are OR then not part of OR sequence
                if current_operator != "OR" and next_operator != "OR":
                    return self._not()

                # If next operator is OR and it's either start of bracket or first OR then it's start of OR sequence
                # Otherwise if next operator is still OR then it's in middle of OR sequence
                if next_operator == "OR":
                    if current_operator != "OR" or previous_parenthesis == "]" or current_parenthesis == "[":
                        return self._start() 

                    return self._middle()

                # If current operator is OR and isn't start of bracket then it's within OR sequence but can't be start
                elif current_operator == "OR" and current_parenthesis != "[":
                    # If next operator is not OR or end of bracket then it's end of OR sequence
                    # Otherwise it's in middle of OR sequence
                    if next_operator != "OR" or current_parenthesis == "]" or next_parenthesis == "[":
                        return self._end()

                    return self._middle()

        else:
            # If one skill in list then can't be part of OR sequence
            if i == 0:
                return self._not()

            # If it's the final skill, current operator is OR and not start of bracket then it's end of OR sequence
            elif current_operator == "OR":
                if current_parenthesis != "[":
                    return self._end()

            # If last operator not OR then not part of OR sequence
            else:
                return self._not()

        print("Or sequence not processed correctly")

@consultants_router.get("/", name="Filter by skills")
async def filter_consultants_by_skills(
    skills: str = Query(default=...),
    hidden_categories: List[str] = Query(default=[])
    ):
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    rules_str = base64.urlsafe_b64decode(skills)
    rules = json.loads(rules_str)

    all_hidden = determine_all_categories_hidden(conn, hidden_categories)

    effective_bracket_idxs = determine_effective_bracket_indexes(rules)

    apoc_idxs = [i[1] for i in effective_bracket_idxs]

    path_count = 0
    idx_path_num = {}
    or_status = OrStatusProcesser()
    query = "MATCH pa=(c:Consultant)-[:KNOWS]->(sa)"

    for i, rule in enumerate(rules):

        idx_path_num[i] = path_count

        intersect = ""
        union = ""
        match_start = ""
        where_q = ""
        or_q = ""
        unwind_q = ""

        name = rule["name"]

        is_or, start_or, end_or = or_status.process(i, rules)

        ## match
        if i != 0:
            if rule["parenthesis"] == "[" or start_or:
                match_start = f" MATCH p{char(path_count)}=()-[:KNOWS]->(s{char(path_count)})"

            elif not is_or:
                match_start = f" MATCH p{char(path_count)}=(n{char(path_count-1)})-[:KNOWS]->(s{char(path_count)})"

        ## where
        if not is_or or start_or:
            where_q = f" where s{char(path_count)}.Name = '{name}'"

        ## or_q
        if is_or and not start_or:
            or_q = f" OR s{char(path_count)}.Name = '{name}'"

        ## unwind_q
        if not start_or:
            unwind_q = f" unwind nodes(p{char(path_count)}) as n{char(path_count)}"

        ## intersection/union
        if i in apoc_idxs and i != apoc_idxs[0]:
            bracket_i = apoc_idxs.index(i)
            path_1 = idx_path_num[effective_bracket_idxs[bracket_i - 1][1]]
            path_2 = idx_path_num[effective_bracket_idxs[bracket_i][1]]
            if rules[effective_bracket_idxs[bracket_i][0]]["operator"] == "AND":
                path_count += 1
                intersect += f" with apoc.coll.intersection(collect(n{char(path_1)}), collect(n{char(path_2)})) as n{char(path_count)}"
                intersect += f" unwind n{char(path_count)} as n{char(path_count + 1)}"
                path_count += 1

            elif rules[effective_bracket_idxs[bracket_i][0]]["operator"] == "OR":
                path_count += 1
                intersect += f" with apoc.coll.union(collect(n{char(path_1)}), collect(n{char(path_2)})) as n{char(path_count)}"
                intersect += f" unwind n{char(path_count)} as n{char(path_count + 1)}"
                path_count += 1
        

        # Move to next path
        if rule["parenthesis"] == "]":
            path_count += 1
        elif not is_or:
            path_count += 1
        elif end_or:
            path_count += 1

        query += match_start + where_q + or_q + unwind_q + intersect + union

    penult_char = char(path_count - 1)
    final_char = char(path_count)

    if not all_hidden:
        query += f" MATCH p{final_char}=(n{penult_char})-[:KNOWS]->()"
    else:
        query += f" MATCH p{final_char}=(n{penult_char})"
    
    if hidden_categories:
        query += f" WHERE NONE(n IN nodes(p{final_char}) WHERE"
        for i, group in enumerate(hidden_categories):
            query += f' n.Group = "{group}"'
            if i != len(hidden_categories) - 1:
                query += " OR"
            else:
                query += ")"

    if all_hidden:
        query += f" unwind nodes(p{final_char}) as n{final_char}"
        query += " with collect( distinct {id: ID(n" + final_char + f"), name: n{final_char}.Name, group: n{final_char}.Group" + "}) as nzz"
        query += " return {nodes: nzz, links: []}"

    else:
        query += neo4j_to_d3_cypher(final_char)

    print(query)

    result = conn.query(query)
    
    conn.close()

    return result[0][0]
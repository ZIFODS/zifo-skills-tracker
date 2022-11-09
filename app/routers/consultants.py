import base64
from typing import List, TypedDict, NamedTuple
from fastapi import APIRouter, Query
from app.utils import char
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

def generate_intersect_or_union_query(
    i: int, 
    rules: list[Rule], 
    bracket_idx_list: list[BracketIndexes], 
    idx_path_num: dict[int, int], 
    ) -> str:
    """
    Generate apoc intersection or union query to combine results from current and preceding effective brackets.

    Arguments
    ---------
    i : int
        current index of rule in search list
    rules : list[Rule]
        all rules in search list
    bracket_idx_list : list[BracketIndexes]
        list of start and end indexes for effective brackets
    idx_path_num : dict[int, int]
        link between i and path count

    Returns
    -------
    query : str
        apoc intersection or union query
    """
    query = ""

    end_bracket_idxs = [i[1] for i in bracket_idx_list]

    if i in end_bracket_idxs and i != end_bracket_idxs[0]:
        bracket_i = end_bracket_idxs.index(i)

        previous_path = idx_path_num[bracket_idx_list[bracket_i - 1].end]
        current_path = idx_path_num[bracket_idx_list[bracket_i].end]

        current_operator = rules[bracket_idx_list[bracket_i].start]["operator"]

        if current_operator == "AND":
            func_str = "intersection"

        elif current_operator == "OR":
            func_str = "union"

        query += f" with apoc.coll.{func_str}(collect(n{char(previous_path)}), collect(n{char(current_path)})) as n{char(current_path + 1)}"
        query += f" unwind n{char(current_path + 1)} as n{char(current_path + 2)}"

    return query

def collect_final_nodes(path_count: int, all_hidden: bool) -> str:
    """
    Generate match statement to collect final nodes.
    If all categories to be hidden, don't include any relationships.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    all_hidden : bool
        if all categories are to be hidden

    Returns
    -------
    query : str
        final match query to collect nodes
    """
    penult_char = char(path_count - 1)
    final_char = char(path_count)

    if not all_hidden:
        return f" MATCH p{final_char}=(n{penult_char})-[:KNOWS]->()"
    else:
        return f" MATCH p{final_char}=(n{penult_char})"

def remove_nodes_with_hidden_categories(path_count: int, hidden_categories: list[str]) -> str:
    """
    Use Cypher WHERE clause to remove nodes where group property is a category to be hidden.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    hidden_categories : list[str]
        list of categories hidden by user

    Returns
    -------
    query : str
        WHERE query to remove nodes in certain categories
    """
    query = ""

    final_char = char(path_count)

    if hidden_categories:
        query += f" WHERE NONE(n IN nodes(p{final_char}) WHERE"
        for i, group in enumerate(hidden_categories):
            query += f' n.Group = "{group}"'
            if i != len(hidden_categories) - 1:
                query += " OR"
            else:
                query += ")"

    return query

def compile_results_with_nodes_and_links(final_char):
    query = f" unwind nodes(p{final_char}) as n{final_char} unwind relationships(p{final_char}) as r{final_char}"

    query += " with collect( distinct {"
    query += f"id: ID(n{final_char}), name: n{final_char}.Name, group: n{final_char}.Group"
    query += "}) as nzz,"

    query += " collect( distinct {"
    query += f"id: ID(r{final_char}), source: ID(startnode(r{final_char})), target: ID(endnode(r{final_char}))"
    query += "}) as rzz"
    
    query += " RETURN {nodes: nzz, links: rzz}"
    return query

def compile_results_with_nodes(path_count: int) -> str:
    """
    Compile results if all categories have been hidden.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated

    Returns
    -------
    query : str
        final Cypher query to compile all results
    """
    final_char = char(path_count)

    query = f" unwind nodes(p{final_char}) as n{final_char}"
    query += " with collect( distinct {id: ID(n" + final_char + f"), name: n{final_char}.Name, group: n{final_char}.Group" + "}) as nzz"
    query += " return {nodes: nzz, links: []}"

    return query

@consultants_router.get("/", name="Filter by skills")
async def filter_consultants_by_skills(
    skills: str = Query(default=...),
    hidden_categories: List[str] = Query(default=[])
    ):
    conn = Neo4jConnection(uri="neo4j://neo4j-db:7687", user="neo4j", password="test")

    rules_str = base64.urlsafe_b64decode(skills)
    rules = json.loads(rules_str)

    all_hidden = determine_all_categories_hidden(conn, hidden_categories)

    bracket_idx_list = determine_effective_bracket_indexes(rules)

    path_count = 0
    idx_path_num = {}
    or_status = OrStatusProcesser()
    query = "MATCH pa=(c:Consultant)-[:KNOWS]->(sa)"

    for i, rule in enumerate(rules):

        idx_path_num[i] = path_count

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
        intersect_or_union = generate_intersect_or_union_query(i, rules, bracket_idx_list, idx_path_num)

        # Move to next path
        if intersect_or_union:
            path_count += 2
        if rule["parenthesis"] == "]":
            path_count += 1
        elif not is_or:
            path_count += 1
        elif end_or:
            path_count += 1

        query += match_start + where_q + or_q + unwind_q + intersect_or_union

    query += collect_final_nodes(path_count, all_hidden)

    query += remove_nodes_with_hidden_categories(path_count, hidden_categories)

    if all_hidden:
        query += compile_results_with_nodes(path_count)

    else:
        final_char = char(path_count)
        query += compile_results_with_nodes_and_links(final_char)

    print(query)

    result = conn.query(query)
    
    conn.close()

    return result[0][0]
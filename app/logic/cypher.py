from app.utils import char
from app.logic.brackets import BracketIndexes, get_all_end_brackets
from app.models.rule import Rule
from pipeline.src.neo4j_connect import Neo4jConnection

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
    final_char = char(path_count)

    query = f" WHERE NONE(n IN nodes(p{final_char}) WHERE"
    for i, group in enumerate(hidden_categories):
        query += f' n.Group = "{group}"'
        if i != len(hidden_categories) - 1:
            query += " OR"
        else:
            query += ")"

    return query

def compile_results_with_nodes(path_count: int) -> str:
    """
    Compile results with Cypher returning only nodes.

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

def compile_results_with_nodes_and_links(path_count: int) -> str:
    """
    Compile results with Cypher returning nodes and links.

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

    query = f" unwind nodes(p{final_char}) as n{final_char} unwind relationships(p{final_char}) as r{final_char}"

    query += " with collect( distinct {"
    query += f"id: ID(n{final_char}), name: n{final_char}.Name, group: n{final_char}.Group"
    query += "}) as nzz,"

    query += " collect( distinct {"
    query += f"id: ID(r{final_char}), source: ID(startnode(r{final_char})), target: ID(endnode(r{final_char}))"
    query += "}) as rzz"
    
    query += " RETURN {nodes: nzz, links: rzz}"

    return query

def match_all_consultants_with_knows_relationship(path_count: int) -> str:
    """
    Cypher: MATCH all nodes to a new path, where nodes have Consultant label and KNOWS relationship.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    
    Returns
    -------
    query : str
    """
    return f" MATCH p{char(path_count)}=(c:Consultant)-[:KNOWS]->(s{char(path_count)})"

def match_consultant_with_name_with_knows_relationship(path_count: int, name: str) -> str:
    """
    Cypher: MATCH all nodes to a new path, where nodes have Consultant label, defined name property and KNOWS relationship.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    name : str
        full name of Consultant
    
    Returns
    -------
    query : str
    """
    return f" MATCH p{char(path_count)}=(c:Consultant " + "{" + f'Name: "{name}"' + "}" + f")-[:KNOWS]->(s{char(path_count)})"

def match_consultant_with_name(path_count: int, name: str) -> str:
    """
    Cypher: MATCH all nodes to a new path, where nodes have Consultant label and defined name property.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    name : str
        full name of Consultant
    
    Returns
    -------
    query : str
    """
    return f" MATCH p{char(path_count)}=(c:Consultant " + "{" + f'Name: "{name}"' + "})"

def match_nodes_from_previous_nodes_with_knows_relationship(path_count: int) -> str:
    """
    Cypher: MATCH existing set of nodes to a new path, where nodes have KNOWS relationship.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    
    Returns
    -------
    query : str
    """
    return f" MATCH p{char(path_count)}=(n{char(path_count - 1)})-[:KNOWS]->(s{char(path_count)})"

def match_nodes_from_previous_nodes(path_count: int) -> str:
    """
    Cypher: MATCH existing set of nodes to a new path.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    
    Returns
    -------
    query : str
    """
    return f" MATCH p{char(path_count)}=(n{char(path_count - 1)})"

def where_skill_has_name(path_count: int, name: str) -> str:
    """
    Cypher: WHERE a matched skill has property Name equal to supplied value.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    name : str
        name of skill
    
    Returns
    -------
    query : str
    """
    return f" where s{char(path_count)}.Name = '{name}'"

def or_skill_with_name(path_count: int, name: str) -> str:
    """
    Cypher: OR a matched skill has another property Name equal to supplied value

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    name : str
        name of skill
    
    Returns
    -------
    query : str
    """
    return f" OR s{char(path_count)}.Name = '{name}'"

def unwind_nodes(path_count: int) -> str:
    """
    Cypher: UNWIND nodes from existing path into node set.

    Arguments
    ---------
    path_count : int
        current number of Cypher paths that have generated
    
    Returns
    -------
    query : str
    """
    return f" unwind nodes(p{char(path_count)}) as n{char(path_count)}"

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
    end_bracket_idxs = get_all_end_brackets(bracket_idx_list)

    bracket_i = end_bracket_idxs.index(i)

    previous_path = idx_path_num[bracket_idx_list[bracket_i - 1].end]
    current_path = idx_path_num[bracket_idx_list[bracket_i].end]

    current_operator = rules[bracket_idx_list[bracket_i].start]["operator"]

    if current_operator == "AND":
        func_str = "intersection"

    elif current_operator == "OR":
        func_str = "union"

    query = f" with apoc.coll.{func_str}(collect(n{char(previous_path)}), collect(n{char(current_path)})) as n{char(current_path + 1)}"
    query += f" unwind n{char(current_path + 1)} as n{char(current_path + 2)}"

    return query
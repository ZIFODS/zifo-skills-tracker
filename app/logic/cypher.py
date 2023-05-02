from app.utils.neo4j_connect import Neo4jConnection


def determine_all_categories_hidden(
    conn: Neo4jConnection, hidden_categories: list[str]
):
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
        all_labels_result = conn.query("MATCH (n) RETURN COLLECT(DISTINCT n.category) ")
        all_categories = all_labels_result[0].values("COLLECT(DISTINCT n.category)")[0]

        all_categories.sort()
        hidden_categories.sort()
        if all_categories == hidden_categories:
            return True

    return False


def remove_skill_nodes_with_hidden_categories(hidden_categories: list[str]) -> str:
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
    query = f" WHERE NOT s.category IN {hidden_categories}"

    return query


def compile_results_with_nodes() -> str:
    """
    Compile results with Cypher returning only nodes.

    Returns
    -------
    query : str
        final Cypher query to compile all results
    """
    query = " UNWIND nodes(p) as n"

    query += (
        " WITH collect( distinct {id: n.uid, name: n.name, type: labels(n)[0], email: n.email, category: "
        "n.category}) as nz"
    )

    query += " RETURN {nodes: nz, links: []}"

    return query


def compile_results_with_nodes_and_links() -> str:
    """
    Compile results with Cypher returning nodes and links.

    Returns
    -------
    query : str
        final Cypher query to compile all results
    """
    query = " UNWIND nodes(p) as n UNWIND relationships(p) as r"

    query += (
        " WITH collect( distinct {id: n.uid, name: n.name, type: labels(n)[0], email: n.email, category: "
        "n.category}) as nz, collect( distinct {id: r.uid, source: startnode(r).uid, target: endnode(r).uid}) "
        "as rz"
    )

    query += " RETURN {nodes: nz, links: rz}"

    return query

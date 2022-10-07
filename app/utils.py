NEO4J_TO_D3_CYPHER = '''unwind nodes(p) as n unwind relationships(p) as r
                        with collect( distinct {id: ID(n), name: n.Name, group: labels(n)[0]}) as nl, 
                        collect( distinct {id: ID(r), source: ID(startnode(r)), target: ID(endnode(r))}) as rl
                        RETURN {nodes: nl, links: rl}
                    '''
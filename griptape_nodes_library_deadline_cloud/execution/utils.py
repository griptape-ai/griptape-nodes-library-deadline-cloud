def _outgoing_connection_exists(source_node: str, source_param: str) -> bool:
    """Check if a source node/parameter has any outgoing connections.

    Args:
        source_node: Name of the node that would be sending the connection
        source_param: Name of the parameter on that node

    Returns:
        True if the parameter has at least one outgoing connection, False otherwise

    Logic: Look in connections.outgoing_index[source_node][source_param]
    """
    from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

    connections = GriptapeNodes.FlowManager().get_connections()

    # Check if source_node has any outgoing connections at all
    source_connections = connections.outgoing_index.get(source_node)
    if source_connections is None:
        return False

    # Check if source_param has any outgoing connections
    param_connections = source_connections.get(source_param)
    if param_connections is None:
        return False

    # Return True if connections list is populated
    return bool(param_connections)


def _incoming_connection_exists(target_node: str, target_param: str) -> bool:
    """Check if a target node/parameter has any incoming connections.

    Args:
        target_node: Name of the node that would be receiving the connection
        target_param: Name of the parameter on that node

    Returns:
        True if the parameter has at least one incoming connection, False otherwise

    Logic: Look in connections.incoming_index[target_node][target_param]
    """
    from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

    connections = GriptapeNodes.FlowManager().get_connections()

    # Check if target_node has any incoming connections at all
    target_connections = connections.incoming_index.get(target_node)
    if target_connections is None:
        return False

    # Check if target_param has any incoming connections
    param_connections = target_connections.get(target_param)
    if param_connections is None:
        return False

    # Return True if connections list is populated
    return bool(param_connections)

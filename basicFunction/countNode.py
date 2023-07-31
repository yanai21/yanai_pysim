def countNode(Nodes,status):
    empty_node = []
    for node in Nodes:
        if node.status == status:
            empty_node.append(node)

    return empty_node

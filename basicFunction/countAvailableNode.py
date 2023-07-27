def countAvaiableNode(Nodes):
    empty_node = []
    for node in Nodes:
        if node.status == 0:
            empty_node.append(node)

    return empty_node

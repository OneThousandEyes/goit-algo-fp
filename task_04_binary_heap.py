import uuid
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Рекурсивно додає ребра до графа для візуалізації."""
    if node is None:
        return graph

    graph.add_node(node.id, color=node.color, label=node.val)

    if node.left:
        graph.add_edge(node.id, node.left.id)
        lx = x - 1 / 2 ** layer
        pos[node.left.id] = (lx, y - 1)
        add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)

    if node.right:
        graph.add_edge(node.id, node.right.id)
        rx = x + 1 / 2 ** layer
        pos[node.right.id] = (rx, y - 1)
        add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root, figsize=(9, 5)):
    """Малює дерево з коренем tree_root."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {node_id: data["label"] for node_id, data in tree.nodes(data=True)}

    plt.figure(figsize=figsize)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


def heap_to_tree(heap):
    """Перетворює купу у бінарне дерево."""
    if not heap:
        return None

    nodes = [Node(v) for v in heap]  # створили всі вузли

    for i in range(len(heap)):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < len(heap):
            nodes[i].left = nodes[li]
        if ri < len(heap):
            nodes[i].right = nodes[ri]

    return nodes[0]


def visualize_heap(heap):
    """Візуалізує купу: перетворює heap -> дерево -> малює."""
    root = heap_to_tree(heap)
    if root is None:
        print("Heap is empty")
        return
    draw_tree(root)


def main():
    heap = [1, 3, 6, 5, 9, 8, 15, 74, 52]
    visualize_heap(heap)


if __name__ == "__main__":
    main()
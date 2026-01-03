import uuid
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="#B0CBEF"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Рекурсивно додає ребра для візуалізації"""
    if node is None:
        return

    graph.add_node(node.id, color=node.color, label=node.val)

    if node.left:
        graph.add_edge(node.id, node.left.id)
        lx = x - 1 / 2 ** layer
        pos[node.left.id] = (lx, y - 1)
        add_edges(graph, node.left, pos, lx, y - 1, layer + 1)

    if node.right:
        graph.add_edge(node.id, node.right.id)
        rx = x + 1 / 2 ** layer
        pos[node.right.id] = (rx, y - 1)
        add_edges(graph, node.right, pos, rx, y - 1, layer + 1)


def draw_tree(root, title="", figsize=(10, 6)):
    """Малює дерево з коренем root."""
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(tree, root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {nid: data["label"] for nid, data in tree.nodes(data=True)}

    plt.clf()
    plt.title(title)
    nx.draw(
        tree,
        pos=pos,
        labels=labels,
        arrows=False,
        node_size=2600,
        node_color=colors
    )
    plt.tight_layout()
    plt.pause(1.1)   # невелика пауза, щоб встигнути побачити зміни


def heap_to_tree(heap):
    """Перетворює купу у бінарне дерево."""
    if not heap:
        return None

    nodes = [Node(v) for v in heap]

    for i in range(len(nodes)):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < len(nodes):
            nodes[i].left = nodes[li]
        if ri < len(nodes):
            nodes[i].right = nodes[ri]

    return nodes[0]


def make_gradient_colors(
    n,
    start=(30, 90, 170),      # темний/насичений синій
    end=(220, 240, 255),     # майже білий блакитний
    gamma=0.7                # <1 => візуально помітніші кроки
):
    """Створює n кольорів у вигляді градієнта від start до end."""
    colors = []
    for i in range(n):
        t = 1 if n == 1 else (i / (n - 1)) ** gamma
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        colors.append(f"#{r:02X}{g:02X}{b:02X}")
    return colors


def reset_colors(root, default="#B0CBEF"):
    """Скидає кольори всіх вузлів дерева до default."""
    q = deque([root])
    while q:
        n = q.popleft()
        n.color = default
        if n.left:
            q.append(n.left)
        if n.right:
            q.append(n.right)


def count_nodes_bfs(root):
    """Підраховує кількість вузлів у дереві за допомогою BFS."""
    q = deque([root])
    count = 0
    while q:
        n = q.popleft()
        count += 1
        if n.left:
            q.append(n.left)
        if n.right:
            q.append(n.right)
    return count


def visualize_dfs(root):
    """Візуалізує обхід дерева в глибину (DFS) за допомогою стеку."""
    total = count_nodes_bfs(root)
    colors = make_gradient_colors(total)

    stack = [root]
    step = 0

    while stack:
        node = stack.pop()

        node.color = colors[step]
        step += 1

        draw_tree(root, f"DFS (stack) | step {step} | visit {node.val}")

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)


def visualize_bfs(root):
    """Візуалізує обхід дерева в ширину (BFS) за допомогою черги."""
    total = count_nodes_bfs(root)
    colors = make_gradient_colors(total)

    q = deque([root])
    step = 0

    while q:
        node = q.popleft()

        node.color = colors[step]
        step += 1

        draw_tree(root, f"BFS (queue) | step {step} | visit {node.val}")

        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)


def main():
    heap = [1, 3, 6, 5, 9, 8, 15, 74, 52]
    root = heap_to_tree(heap)

    if root is None:
        print("Heap is empty")
        return

    plt.figure(figsize=(10, 6))
    plt.ion()

    draw_tree(root, "Initial tree")

    reset_colors(root)
    visualize_dfs(root)

    reset_colors(root)
    draw_tree(root, "Reset before BFS")

    visualize_bfs(root)

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()

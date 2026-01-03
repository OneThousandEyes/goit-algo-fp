import heapq
from math import inf
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


console = Console()


def show_step(step, current, dist, visited):
    """Відображає поточний крок алгоритму Дейкстри."""
    t = Table(title=f"Крок {step}: обрана вершина [cyan]{current}[/cyan]", show_lines=True)
    t.add_column("Вершина", style="bold")
    t.add_column("Відстань", justify="right")
    t.add_column("Перевірено", justify="center")

    for v in sorted(dist):
        d = "∞" if dist[v] == inf else str(dist[v])
        ok = "[green]Так[/green]" if v in visited else "[yellow]Ні[/yellow]"
        t.add_row(v, d, ok)

    console.print(t)


def dijkstra_heap(graph, start, show=True):
    """Реалізація алгоритму Дейкстри з використанням бінарної купи (heapq)."""
    dist = {v: inf for v in graph}
    prev = {v: None for v in graph}
    dist[start] = 0

    heap = [(0, start)]
    visited = set()
    step = 0

    console.print(Panel.fit(f"Дейкстра з [bold]бінарною купою[/bold] (heapq)\nСтарт: [cyan]{start}[/cyan]",
                            border_style="cyan"))

    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u] or u in visited:
            continue

        visited.add(u)
        step += 1

        for v, w in graph[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

        if show:
            show_step(step, u, dist, visited)

    return dist, prev


def path(prev, start, target):
    """Відновлює найкоротший шлях від start до target."""
    cur = target
    p = []
    while cur is not None:
        p.append(cur)
        if cur == start:
            break
        cur = prev[cur]
    p.reverse()
    return p if p and p[0] == start else None


def show_final(start, dist, prev):
    """Відображає підсумкові найкоротші шляхи від стартової вершини."""
    t = Table(title=f"Найкоротші шляхи від [cyan]{start}[/cyan]", show_lines=True)
    t.add_column("Вершина", style="bold")
    t.add_column("Відстань", justify="right")
    t.add_column("Шлях")

    for v in sorted(dist):
        d = "∞" if dist[v] == inf else str(dist[v])
        p = path(prev, start, v)
        p = "—" if p is None else " → ".join(p)
        t.add_row(v, d, p)

    console.print(t)


def main():
    graph = {
        "A": {"B": 5, "C": 10},
        "B": {"A": 5, "D": 3},
        "C": {"A": 10, "D": 2},
        "D": {"B": 3, "C": 2, "E": 4},
        "E": {"D": 4},
    }

    dist, prev = dijkstra_heap(graph, "A", show=True)
    show_final("A", dist, prev)


if __name__ == "__main__":
    main()
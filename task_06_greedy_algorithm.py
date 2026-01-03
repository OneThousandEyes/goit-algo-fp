from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: dict, budget: int):
    """Жадібний алгоритм вибору страв за максимальним співвідношенням калорій до вартості."""
    ranked = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True,
    )
    picked, cost, cal = [], 0, 0
    for name, v in ranked:
        if cost + v["cost"] <= budget:
            picked.append(name)
            cost += v["cost"]
            cal += v["calories"]
    return picked, cost, cal


def dynamic_programming(items: dict, budget: int):
    """Динамічне програмування для оптимального вибору страв за калоріями."""
    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    cals = [items[n]["calories"] for n in names]
    n = len(names)

    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w, val = costs[i - 1], cals[i - 1]
        for b in range(budget + 1):
            best = dp[i - 1][b]
            if w <= b:
                best = max(best, dp[i - 1][b - w] + val)
            dp[i][b] = best

    picked = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            picked.append(names[i - 1])
            b -= costs[i - 1]
    picked.reverse()

    total_cost = sum(items[n]["cost"] for n in picked)
    total_cal = dp[n][budget]
    return picked, total_cost, total_cal


def render(items: dict, budget: int):
    """Виводить таблиці з меню та результатами обох алгоритмів."""
    console = Console()

    # items table
    t = Table(title=f"Меню (бюджет: {budget})", show_lines=False)
    t.add_column("Item", style="bold")
    t.add_column("Cost", justify="right")
    t.add_column("Calories", justify="right")
    t.add_column("Cal/Cost", justify="right")

    for name, v in sorted(items.items(), key=lambda kv: kv[0]):
        ratio = v["calories"] / v["cost"]
        t.add_row(name, str(v["cost"]), str(v["calories"]), f"{ratio:.2f}")

    g_items, g_cost, g_cal = greedy_algorithm(items, budget)
    d_items, d_cost, d_cal = dynamic_programming(items, budget)

    r = Table(title="Результати", show_lines=False)
    r.add_column("Алгоритм", style="bold")
    r.add_column("Обрано")
    r.add_column("Вартість", justify="right")
    r.add_column("Калорії", justify="right")

    r.add_row("Greedy", ", ".join(g_items) or "-", str(g_cost), str(g_cal))
    r.add_row("Dynamic", ", ".join(d_items) or "-", str(d_cost), str(d_cal))

    delta = d_cal - g_cal
    note = f"[green]Dynamic краще на {delta} кал[/green]" if delta > 0 else "[yellow]Greedy = DP[/yellow]" if delta == 0 else f"[red]Greedy краще на {-delta} кал[/red]"

    console.print(t)
    console.print(r)
    console.print(Panel.fit(note, title="Порівняння", border_style="cyan"))


if __name__ == "__main__":
    render(items, budget=100)
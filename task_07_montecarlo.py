import random
import time
from collections import defaultdict

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich import box


def simulate_two_dice(rolls: int) -> dict[int, int]:
    """Симуляція кидання двох шестигранних кубиків."""
    counts: dict[int, int] = defaultdict(int)

    # прогрес рухається повільніше 
    chunk = max(1, rolls // 150)

    with Progress(
        TextColumn("[bold]Monte-Carlo[/bold]"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=Console(),
        transient=True,  # після завершення прогрес зникає
    ) as progress:
        task_id = progress.add_task("Rolling...", total=rolls)

        done = 0
        while done < rolls:
            step = min(chunk, rolls - done)
            for _ in range(step):
                d1 = random.randint(1, 6)
                d2 = random.randint(1, 6)
                counts[d1 + d2] += 1

            done += step
            progress.update(task_id, advance=step)

            # маленька пауза
            time.sleep(0.02)

    return counts


def build_theory() -> dict[int, int]:
    """Побудова теоретичних ймовірностей сум при киданні двох кубиків."""
    return {
        2: 1, 3: 2, 4: 3, 5: 4, 6: 5,
        7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1
    }


def print_results(counts: dict[int, int], rolls: int) -> None:
    """Вивід результатів симуляції та теоретичних ймовірностей."""
    console = Console()
    theory = build_theory()

    table = Table(
        title=f"Ймовірності сум при киданні двох кубиків (N = {rolls:,})",
        box=box.ROUNDED,
        header_style="bold",
        show_lines=True,
    )

    table.add_column("Сума", justify="right", style="bold cyan")
    table.add_column("Monte-Carlo", justify="right")
    table.add_column("Аналітична", justify="right")
    table.add_column("Різниця", justify="right")

    for s in range(2, 13):
        mc = counts.get(s, 0) / rolls * 100
        an = theory[s] / 36 * 100
        diff = mc - an

        diff_style = "green" if abs(diff) < 0.05 else ("yellow" if abs(diff) < 0.15 else "red")

        table.add_row(
            str(s),
            f"{mc:6.2f}%",
            f"{an:6.2f}%",
            f"[{diff_style}]{diff:+.2f}%[/{diff_style}]",
        )

    console.print(table)

    console.print(
        "\n[bold]Висновок:[/bold] чим більше N, тим ближче Monte-Carlo до аналітичних значень. "
        "Найбільш імовірна сума — [bold]7[/bold]."
    )


def plot_chart(counts: dict[int, int], rolls: int) -> None:
    """Побудова графіка порівняння Monte-Carlo та аналітичних ймовірностей."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        Console().print("[yellow]matplotlib не встановлено — графік пропущено.[/yellow]")
        return

    theory = build_theory()
    sums = list(range(2, 13))
    mc_probs = [counts.get(s, 0) / rolls for s in sums]
    th_probs = [theory[s] / 36 for s in sums]

    plt.figure()
    plt.bar(sums, mc_probs, alpha=0.75, label="Monte-Carlo")
    plt.plot(sums, th_probs, marker="o", label="Аналітична")
    plt.xticks(sums)
    plt.xlabel("Сума")
    plt.ylabel("Ймовірність")
    plt.title(f"Два кубики: Monte-Carlo vs Аналітична (N={rolls:,})")
    plt.legend()
    plt.show()


def main():
    rolls = 1_000_000

    counts = simulate_two_dice(rolls)
    print_results(counts, rolls)
    plot_chart(counts, rolls)


if __name__ == "__main__":
    main()

import turtle
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def draw_branch(t: turtle.Turtle, length: float, level: int):
    """Рекурсивна функція для малювання гілок дерева Піфагора."""
    if level == 0:
        return

    # Малюємо гілку
    t.forward(length)

    # Ліва гілка
    t.left(30)
    draw_branch(t, length * 0.7, level - 1)

    # Повертаємось до стовбура
    t.right(60)
    draw_branch(t, length * 0.7, level - 1)

    # Повертаємо черепашку в початковий стан
    t.left(30)
    t.backward(length)


def main():
    console.print(
        Panel(
            Text("Фрактал: Дерево Піфагора (рекурсія)", justify="center", style="bold green"),
            expand=False
        )
    )

    level = int(
        input("Введіть рівень рекурсії (наприклад 6–10): ").strip() or "8"
    )

    console.print(f"[cyan]Обраний рівень рекурсії:[/cyan] [bold]{level}[/bold]")
    console.print("[yellow]Малюю фрактал...[/yellow]\n")

    screen = turtle.Screen()
    screen.title("Фрактал: Дерево Піфагора")
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.hideturtle()
    t.color("darkred")
    t.speed(0)
    t.pensize(2)

    # Початкова позиція
    t.penup()
    t.goto(0, -screen.window_height() // 2 + 40)
    t.setheading(90)  
    t.pendown()

    draw_branch(t, length=120, level=level)

    screen.mainloop()


if __name__ == "__main__":
    main()

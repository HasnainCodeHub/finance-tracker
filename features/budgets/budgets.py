import questionary
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from datetime import datetime

BUDGET_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]

console = Console()

def set_budget():
    """Sets a monthly budget for a category."""
    try:
        category = questionary.select(
            "Select category to set budget for:",
            choices=BUDGET_CATEGORIES,
            qmark="🏷️"
        ).ask()
        if not category:
            return

        amount_str = questionary.text(
            "Enter the monthly budget amount for this category:",
            validate=lambda text: text.isdigit() and float(text) > 0,
            qmark="💰"
        ).ask()
        if not amount_str:
            console.print(Panel("[bold red]Amount cannot be empty.[/bold red]", title="Error"))
            return

        amount = int(float(amount_str) * 100)  # Store as paisa/cents

        budget_entry = f"{category},{amount}\n"

        # Check if budget for this category already exists and update it
        budgets = []
        try:
            with open("database/budgets.txt", "r") as f:
                budgets = f.readlines()
        except FileNotFoundError:
            pass # File will be created if it doesn't exist

        updated_budgets = []
        category_found = False
        for budget in budgets:
            if budget.startswith(f"{category},"):
                updated_budgets.append(budget_entry)
                category_found = True
            else:
                updated_budgets.append(budget)
        
        if not category_found:
            updated_budgets.append(budget_entry)

        with open("database/budgets.txt", "w") as f:
            f.writelines(updated_budgets)

        console.print(Panel(f"[bold green]Budget of {amount/100:.2f} for '{category}' set successfully![/bold green]", title="Success"))

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled.[/bold yellow]")
    except Exception as e:
        console.print(Panel(f"[bold red]An error occurred: {e}[/bold red]", title="Error"))

def display_budgets():
    """Displays current month's budget vs. actual spending."""
    try:
        # Read budgets
        budgets_data = {}
        try:
            with open("database/budgets.txt", "r") as f:
                for line in f:
                    category, amount = line.strip().split(',')
                    budgets_data[category] = int(amount)
        except FileNotFoundError:
            console.print(Panel("[bold yellow]No budgets set yet.[/bold yellow]", title="Budgets"))
            return

        if not budgets_data:
            console.print(Panel("[bold yellow]No budgets set yet.[/bold yellow]", title="Budgets"))
            return

        # Read transactions for current month
        current_month = datetime.now().month
        current_year = datetime.now().year
        spent_data = {category: 0 for category in BUDGET_CATEGORIES}

        try:
            with open("database/transactions.txt", "r") as f:
                for line in f:
                    date_str, type, category, _, amount = line.strip().split(',')
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    if date.month == current_month and date.year == current_year and type == "expense":
                        if category in spent_data:
                            spent_data[category] += int(amount)
        except FileNotFoundError:
            pass # No transactions yet

        table = Table(title=f"Monthly Budgets ({datetime.now().strftime('%B %Y')})")
        table.add_column("Category", style="cyan")
        table.add_column("Budget", justify="right", style="magenta")
        table.add_column("Spent", justify="right", style="red")
        table.add_column("Remaining", justify="right", style="green")
        table.add_column("Utilization", justify="left")
        table.add_column("Status", justify="center")

        total_budget = 0
        total_spent = 0
        over_budget_categories = []

        for category in BUDGET_CATEGORIES:
            budget_amount = budgets_data.get(category, 0)
            spent_amount = spent_data.get(category, 0)
            remaining_amount = budget_amount - spent_amount

            total_budget += budget_amount
            total_spent += spent_amount

            if budget_amount > 0:
                utilization_percent = (spent_amount / budget_amount) * 100
            else:
                utilization_percent = 0

            # Status and color coding
            status = ""
            status_color = ""
            if utilization_percent < 70:
                status = "OK"
                status_color = "green"
            elif 70 <= utilization_percent <= 100:
                status = "Warning"
                status_color = "yellow"
            else:
                status = "Over"
                status_color = "red"
                over_budget_categories.append(category)

            # Progress bar
            progress_bar = ""
            with Progress(BarColumn(bar_width=20), TextColumn("[progress.percentage]{task.percentage:>3.0f}%")) as progress:
                task_id = progress.add_task("util", total=budget_amount)
                progress.update(task_id, completed=spent_amount)
                progress_bar = str(progress) # This is a simplification, rich progress bar needs to be rendered

            table.add_row(
                category,
                f"{budget_amount/100:.2f}",
                f"{spent_amount/100:.2f}",
                f"[{'green' if remaining_amount >= 0 else 'red'}]{remaining_amount/100:.2f}[/]",
                f"{utilization_percent:.0f}%", # Simplified progress bar for now
                f"[{status_color}]{status}[/]"
            )
        
        console.print(table)

        # Overall Summary
        overall_remaining = total_budget - total_spent
        overall_utilization = (total_spent / total_budget) * 100 if total_budget > 0 else 0
        overall_balance_style = "green" if overall_remaining >= 0 else "red"

        summary_panel_content = (
            f"[green]Total Monthly Budget: {total_budget/100:.2f}[/green]\n"
            f"[red]Total Spent: {total_spent/100:.2f}[/red]\n"
            f"[{overall_balance_style}]Total Remaining: {overall_remaining/100:.2f}[/{overall_balance_style}]\n"
            f"Overall Utilization: {overall_utilization:.0f}%"
        )

        if over_budget_categories:
            summary_panel_content += "\n[bold red]Categories Over Budget:[/bold red] " + ", ".join(over_budget_categories)
            summary_panel_content += "\n[yellow]Recommendation: Review spending in highlighted categories.[/yellow]"
        else:
            summary_panel_content += "\n[green]Good job! All categories are within budget.[/green]"


        console.print(Panel(summary_panel_content, title="Budget Summary"))


    except FileNotFoundError:
        console.print(Panel("[bold yellow]No budgets set yet.[/bold yellow]", title="Budgets"))
    except Exception as e:
        console.print(Panel(f"[bold red]An error occurred: {e}[/bold red]", title="Error"))

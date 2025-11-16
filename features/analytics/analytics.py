from datetime import datetime
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

console = Console()

def analyze_spending():
    """Analyzes spending patterns for the current month."""
    try:
        # Read transactions
        transactions = []
        try:
            with open("database/transactions.txt", "r") as f:
                transactions = f.readlines()
        except FileNotFoundError:
            console.print(Panel("[bold yellow]No transactions found.[/bold yellow]", title="Spending Analysis"))
            return

        if not transactions:
            console.print(Panel("[bold yellow]No transactions found.[/bold yellow]", title="Spending Analysis"))
            return

        # Filter for current month's expenses
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_expenses = {}

        for transaction in transactions:
            date_str, type, category, _, amount = transaction.strip().split(',')
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date.month == current_month and date.year == current_year and type == "expense":
                amount = int(amount)
                if category in monthly_expenses:
                    monthly_expenses[category] += amount
                else:
                    monthly_expenses[category] = amount
        
        if not monthly_expenses:
            console.print(Panel("[bold yellow]No expenses found for the current month.[/bold yellow]", title="Spending Analysis"))
            return

        # Spending breakdown table
        table = Table(title=f"Spending Breakdown ({datetime.now().strftime('%B %Y')})")
        table.add_column("Category", style="cyan")
        table.add_column("Amount", justify="right", style="red")
        table.add_column("Percentage", justify="right", style="yellow")

        total_spent = sum(monthly_expenses.values())
        
        # Sort categories by amount spent
        sorted_expenses = sorted(monthly_expenses.items(), key=lambda item: item[1], reverse=True)

        for category, amount in sorted_expenses:
            percentage = (amount / total_spent) * 100
            table.add_row(category, f"{amount/100:.2f}", f"{percentage:.2f}%")

        console.print(table)

        # Top 3 spending categories
        top_3 = sorted_expenses[:3]
        top_3_panel_content = "[bold]Top 3 Spending Categories:[/bold]\n"
        for i, (category, amount) in enumerate(top_3):
            top_3_panel_content += f"{i+1}. {category}: {amount/100:.2f}\n"
        
        console.print(Panel(top_3_panel_content, title="Top Spending"))

    except Exception as e:
        console.print(Panel(f"[bold red]An error occurred: {e}[/bold red]", title="Error"))

def analyze_income():
    """Analyzes income for the current month."""
    try:
        # Read transactions
        transactions = []
        try:
            with open("database/transactions.txt", "r") as f:
                transactions = f.readlines()
        except FileNotFoundError:
            console.print(Panel("[bold yellow]No transactions found.[/bold yellow]", title="Income Analysis"))
            return

        if not transactions:
            console.print(Panel("[bold yellow]No transactions found.[/bold yellow]", title="Income Analysis"))
            return

        # Filter for current and previous month's income
        current_month = datetime.now().month
        current_year = datetime.now().year
        prev_month = current_month - 1 if current_month > 1 else 12
        prev_year = current_year if current_month > 1 else current_year - 1
        
        current_month_income = {}
        prev_month_income = {}

        for transaction in transactions:
            date_str, type, category, _, amount = transaction.strip().split(',')
            date = datetime.strptime(date_str, "%Y-%m-%d")
            amount = int(amount)
            if type == "income":
                if date.month == current_month and date.year == current_year:
                    if category in current_month_income:
                        current_month_income[category] += amount
                    else:
                        current_month_income[category] = amount
                elif date.month == prev_month and date.year == prev_year:
                    if category in prev_month_income:
                        prev_month_income[category] += amount
                    else:
                        prev_month_income[category] = amount

        if not current_month_income:
            console.print(Panel("[bold yellow]No income found for the current month.[/bold yellow]", title="Income Analysis"))
            return

        # Income breakdown table
        table = Table(title=f"Income Sources ({datetime.now().strftime('%B %Y')})")
        table.add_column("Source", style="cyan")
        table.add_column("Amount", justify="right", style="green")

        total_current_income = sum(current_month_income.values())
        
        for source, amount in current_month_income.items():
            table.add_row(source, f"{amount/100:.2f}")

        console.print(table)

        # Comparison with last month
        total_prev_income = sum(prev_month_income.values())
        comparison_str = ""
        if total_prev_income > 0:
            percentage_change = ((total_current_income - total_prev_income) / total_prev_income) * 100
            if percentage_change > 0:
                comparison_str = f"[green]Up by {percentage_change:.2f}% from last month.[/green]"
            else:
                comparison_str = f"[red]Down by {abs(percentage_change):.2f}% from last month.[/red]"
        else:
            comparison_str = "No income data for last month to compare."

        summary_panel_content = (
            f"Total Income this month: [bold green]{total_current_income/100:.2f}[/bold green]\n"
            f"{comparison_str}"
        )
        console.print(Panel(summary_panel_content, title="Income Summary"))

    except Exception as e:
        console.print(Panel(f"[bold red]An error occurred: {e}[/bold red]", title="Error"))

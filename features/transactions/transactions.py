import questionary
from datetime import datetime, timedelta
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]

console = Console()

def add_expense():
    """Adds an expense transaction."""
    try:
        amount_str = questionary.text(
            "Enter the expense amount:",
            validate=lambda text: text.isdigit() and float(text) > 0,
            qmark="💰"
        ).ask()
        if not amount_str:
            console.print(Panel("[bold red]Amount cannot be empty.[/bold red]", title="Error"))
            return

        amount = int(float(amount_str) * 100)  # Store as paisa/cents

        category = questionary.select(
            "Select expense category:",
            choices=EXPENSE_CATEGORIES,
            qmark="🏷️"
        ).ask()
        if not category:
            return

        description = questionary.text("Enter a short description:", qmark="📝").ask()
        if not description:
            return

        date_str = questionary.text(
            f"Enter the date (YYYY-MM-DD), leave empty for today ({datetime.now().strftime('%Y-%m-%d')}):",
            qmark="📅"
        ).ask()

        if not date_str:
            date = datetime.now()
        else:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                console.print(Panel("[bold red]Invalid date format. Please use YYYY-MM-DD.[/bold red]", title="Error"))
                return

        transaction = f"{date.strftime('%Y-%m-%d')}|expense|{category}|{description}|{amount}\n"

        with open("database/transactions.txt", "a") as f:
            f.write(transaction)

        console.print(Panel(f"[bold green]Expense of {amount/100:.2f} in '{category}' added successfully![/bold green]", title="Success"))

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled.[/bold yellow]")
    except Exception as e:
        console.print(Panel(f"[bold red]An error occurred: {e}[/bold red]", title="Error"))

def add_income():
    """Adds an income transaction."""
    try:
        amount_str = questionary.text(
            "Enter the income amount:",
            validate=lambda text: text.isdigit() and float(text) > 0,
            qmark="💰"
        ).ask()
        if not amount_str:
            console.print(Panel("[bold red]Amount cannot be empty.[/bold red]", title="Error"))
            return

        amount = int(float(amount_str) * 100)  # Store as paisa/cents

        category = questionary.select(
            "Select income source:",
            choices=INCOME_CATEGORIES,
            qmark="🏷️"
        ).ask()
        if not category:
            return

        description = questionary.text("Enter a short description:", qmark="📝").ask()
        if not description:
            return

        date_str = questionary.text(
            f"Enter the date (YYYY-MM-DD), leave empty for today ({datetime.now().strftime('%Y-%m-%d')}):",
            qmark="📅"
        ).ask()

        if not date_str:
            date = datetime.now()
        else:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                console.print(Panel("[bold red]Invalid date format. Please use YYYY-MM-DD.[/bold red]", title="Error"))
                return

        transaction = f"{date.strftime('%Y-%m-%d')}|income|{category}|{description}|{amount}\n"

        with open("database/transactions.txt", "a") as f:
            f.write(transaction)

        console.print(Panel(f"[bold green]Income of {amount/100:.2f} from '{category}' added successfully![/bold green]", title="Success"))

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Operation cancelled.[/bold yellow]")
    except Exception as e:
        console.print(Panel(f"[bold red]An error occurred: {e}[/bold red]", title="Error"))

def list_transactions():
    """Lists all transactions."""
    try:
        with open("database/transactions.txt", "r") as f:
            transactions = f.readlines()

        if not transactions:
            console.print(Panel("[bold yellow]No transactions found.[/bold yellow]", title="Transactions"))
            return

        table = Table(title="Transactions")
        table.add_column("Date", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Category", style="yellow")
        table.add_column("Description", style="blue")
        table.add_column("Amount", justify="right", style="green")

        # Sort transactions by date (newest first)
        transactions.sort(key=lambda t: datetime.strptime(t.split('|')[0], "%Y-%m-%d"), reverse=True)

        for transaction in transactions:
            date, type, category, description, amount = transaction.strip().split('|')
            amount = int(amount)
            amount_str = f"{amount/100:.2f}"
            style = "red" if type == "expense" else "green"
            table.add_row(date, type, category, description, f"[{style}]{amount_str}[/{style}]")

        console.print(table)

    except FileNotFoundError:
        console.print(Panel("[bold yellow]No transactions found.[/bold yellow]", title="Transactions"))
    except Exception as e:
        console.print(Panel(f"[bold red]An error occurred: {e}[/bold red]", title="Error"))

def show_balance():
    """Shows the balance for the current month."""
    try:
        with open("database/transactions.txt", "r") as f:
            transactions = f.readlines()

        if not transactions:
            console.print(Panel("[bold yellow]No transactions found.[/bold yellow]", title="Balance"))
            return

        current_month = datetime.now().month
        current_year = datetime.now().year
        total_income = 0
        total_expense = 0

        for transaction in transactions:
            date_str, type, _, _, amount = transaction.strip().split('|')
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if date.month == current_month and date.year == current_year:
                amount = int(amount)
                if type == "income":
                    total_income += amount
                else:
                    total_expense += amount

        balance = total_income - total_expense
        balance_style = "green" if balance >= 0 else "red"

        balance_panel = Panel(
            f"[green]Total Income: {total_income/100:.2f}[/green]\n"
            f"[red]Total Expense: {total_expense/100:.2f}[/red]\n"
            f"[{balance_style}]Current Balance: {balance/100:.2f}[/{balance_style}]",
            title="Current Month Balance"
        )
        console.print(balance_panel)

    except FileNotFoundError:
        console.print(Panel("[bold yellow]No transactions found.[/bold yellow]", title="Balance"))
    except Exception as e:
        console.print(Panel(f"[bold red]An error occurred: {e}[/bold red]", title="Error"))

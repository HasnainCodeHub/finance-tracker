import questionary
import subprocess
from features.transactions.transactions import add_expense, add_income, list_transactions, show_balance
from features.budgets.budgets import set_budget, display_budgets
from features.analytics.analytics import analyze_spending

def main_menu():
    """Displays the main menu and returns the user's choice."""
    choice = questionary.select(
        "What would you like to do?",
        choices=[
            "Add Expense",
            "Add Income",
            "List Transactions",
            "Show Balance",
            "Set Budget",
            "Display Budgets",
            "Spending Analysis",
            "Launch Dashboard",
            "Exit"
        ],
        qmark=">"
    ).ask()
    return choice

def main():
    """Main function to run the finance tracker CLI."""
    while True:
        choice = main_menu()
        if choice == "Add Expense":
            add_expense()
        elif choice == "Add Income":
            add_income()
        elif choice == "List Transactions":
            list_transactions()
        elif choice == "Show Balance":
            show_balance()
        elif choice == "Set Budget":
            set_budget()
        elif choice == "Display Budgets":
            display_budgets()
        elif choice == "Spending Analysis":
            analyze_spending()
        elif choice == "Launch Dashboard":
            subprocess.run(["streamlit", "run", "dashboard.py"])
        elif choice == "Exit" or choice is None:
            break

if __name__ == "__main__":
    main()

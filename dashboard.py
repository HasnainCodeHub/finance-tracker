import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    layout="wide",
    page_title="Finance Tracker Pro",
    page_icon="💰",
    initial_sidebar_state="expanded"
)

# --- Color Scheme ---
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
SUCCESS_COLOR = "#2ca02c"
WARNING_COLOR = "#d62728"

# --- Data Loading ---
@st.cache_data
def load_transactions():
    """Loads transactions from the text file and returns a DataFrame."""
    try:
        with open("database/transactions.txt", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Type", "Category", "Description", "Amount"])

    def parse_line(line: str):
        line = line.strip()
        if not line:
            return None
        # Try comma first, then pipe
        for sep in [",", "|"]:
            parts = [p.strip() for p in line.split(sep)]
            if len(parts) == 5:
                return parts
        return None

    transactions = []
    for line in lines:
        parsed = parse_line(line)
        if not parsed:
            continue
        date_str, trans_type, category, description, amount_paisa = parsed
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            # Normalize type to 'Income' / 'Expense'
            t = trans_type.strip().lower()
            if t == "income":
                norm_type = "Income"
            elif t == "expense":
                norm_type = "Expense"
            else:
                norm_type = trans_type.strip().title()

            amount = int(amount_paisa) / 100  # stored in paisa

            transactions.append({
                "Date": date,
                "Type": norm_type,
                "Category": category.strip(),
                "Description": description.strip(),
                "Amount": amount,
            })
        except Exception:
            continue

    if not transactions:
        return pd.DataFrame(columns=["Date", "Type", "Category", "Description", "Amount"])

    return pd.DataFrame(transactions)

# --- UI Components ---
def display_dashboard(df: pd.DataFrame):
    st.header("Monthly Financial Overview")
    current_month = datetime.now().month
    current_year = datetime.now().year
    df_month = df[(df['Date'].dt.month == current_month) & (df['Date'].dt.year == current_year)]

    # --- Metrics ---
    total_income = df_month[df_month['Type'] == 'Income']['Amount'].sum()
    total_expenses = df_month[df_month['Type'] == 'Expense']['Amount'].sum()
    current_balance = total_income - total_expenses
    savings_rate = (current_balance / total_income) if total_income > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Balance", f"₹{current_balance:,.2f}")
    col2.metric("Total Income", f"₹{total_income:,.2f}")
    col3.metric("Total Expenses", f"₹{total_expenses:,.2f}")
    col4.metric("Savings Rate", f"{savings_rate:.1%}")

    st.divider()

    # --- Charts ---
    col1, col2 = st.columns(2)

    # ---- Spending by Category ----
    with col1:
        st.subheader("Spending by Category")
        expense_by_cat = (
            df_month[df_month['Type'] == 'Expense']
            .groupby('Category')['Amount']
            .sum()
        )
        if not expense_by_cat.empty:
            fig = px.pie(
                values=expense_by_cat.values,
                names=expense_by_cat.index,
                hole=.3,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expenses recorded this month.")

    # ---- Income vs. Expenses Trend ----
    with col2:
        st.subheader("Income vs. Expenses Trend")
        if not df_month.empty:
            df_trend = df_month.copy()
            df_trend['Day'] = df_trend['Date'].dt.day

            trend = (
                df_trend
                .groupby(['Day', 'Type'])['Amount']
                .sum()
                .reset_index()
                .pivot(index='Day', columns='Type', values='Amount')
                .fillna(0)
                .reset_index()
            )

            y_cols = [c for c in ['Income', 'Expense'] if c in trend.columns]

            if y_cols:
                fig = px.line(
                    trend,
                    x='Day',
                    y=y_cols,
                    color_discrete_map={
                        'Income': SUCCESS_COLOR,
                        'Expense': WARNING_COLOR
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No income/expense data available for this month.")
        else:
            st.info("No transactions recorded this month.")

    st.divider()

    # --- Recent Transactions ---
    st.subheader("Recent Transactions")
    st.dataframe(
        df.sort_values("Date", ascending=False).head(5),
        use_container_width=True,
        hide_index=True
    )

def display_all_transactions(df: pd.DataFrame):
    st.header("All Recorded Transactions")

    if df.empty:
        st.info("No transactions to display.")
        return

    # --- Filtering ---
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("Start date", df['Date'].min().date())
    with col2:
        end_date = st.date_input("End date", df['Date'].max().date())
    with col3:
        categories = st.multiselect(
            "Filter by category",
            df['Category'].unique(),
            default=list(df['Category'].unique())
        )

    if not categories:
        st.info("Please select at least one category.")
        return

    filtered_df = df[
        (df['Date'].dt.date >= start_date) &
        (df['Date'].dt.date <= end_date) &
        (df['Category'].isin(categories))
    ]

    st.dataframe(
        filtered_df.sort_values("Date", ascending=False),
        use_container_width=True,
        hide_index=True
    )

def display_budget_analysis():
    st.header("Budget Analysis (Coming Soon)")
    st.info("This feature is under construction. You will be able to set and track your budgets here.")

def display_financial_health():
    st.header("Financial Health Score (Coming Soon)")
    st.info("This feature is under construction. You will be able to see your financial health score here.")

# --- Main App ---
def main():
    """Main function to run the Streamlit dashboard."""
    st.title("Finance Tracker Pro")

    df = load_transactions()

    if df.empty:
        st.warning("No transactions found. Add some transactions in the CLI to see your dashboard.")
        return

    # --- Sidebar ---
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page",
        ["Dashboard", "All Transactions", "Budget Analysis", "Financial Health"]
    )

    if page == "Dashboard":
        display_dashboard(df)
    elif page == "All Transactions":
        display_all_transactions(df)
    elif page == "Budget Analysis":
        display_budget_analysis()
    elif page == "Financial Health":
        display_financial_health()

if __name__ == "__main__":
    main()

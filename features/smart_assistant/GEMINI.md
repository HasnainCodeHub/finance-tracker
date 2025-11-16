# Day 5: Smart Assistant & Recommendations

## Today's Goal
Provide users with actionable, intelligent recommendations based on their financial data.

## Learning Focus
- Rule-based logic
- Pattern recognition
- Generating human-like recommendations
- Proactive alerting

## Fintech Concepts
- **Financial Coach**: An automated system providing guidance.
- **Actionable Insights**: Recommendations that users can act on immediately.
- **Proactive Alerts**: Notifications about potential issues (e.g., upcoming bills, low balance).

## Features to Build

### 1. Recommendation Engine
A function that runs a series of checks on the user's financial data and generates a list of recommendations.

Checks to perform:
- **High Spending in a Category**: "You've spent a lot on 'Shopping' this month. Consider reviewing your spending."
- **Unusual Spending**: "Your spending on 'Food' was 50% higher this week than your average."
- **Upcoming Bill Reminder**: "You have a 'Netflix' bill of 15.99 due in 3 days." (Requires bill tracking feature)
- **Low Balance Alert**: "Your balance is running low. You have 50.00 remaining."
- **Savings Opportunity**: "You have some unbudgeted income this month. Consider saving it."
- **Budget Overspending Alert**: "You are over budget in 'Entertainment'. Try to limit spending in this area."

### 2. Display Recommendations
- A new option in the main menu: "Smart Assistant".
- When selected, it displays a list of recommendations in a `rich.panel.Panel`.
- Each recommendation should be clear and concise.

## Success Criteria
✅ Generates at least 3 different types of recommendations.
✅ Recommendations are relevant to the user's data.
✅ Recommendations are displayed clearly.
✅ The system is extensible for adding new recommendation rules.

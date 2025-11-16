# Day 6: Data Management & Portability

## Today's Goal
Allow users to import and export their financial data, ensuring data portability and backup capabilities.

## Learning Focus
- Working with CSV and JSON formats
- File I/O operations
- Data validation and error handling during import

## Fintech Concepts
- **Data Portability**: The ability for users to move their data from one service to another.
- **Data Backup & Restore**: Creating copies of data for safety and restoring it when needed.
- **Open Financial Data**: Standardized data formats that allow for interoperability.

## Features to Build

### 1. Export to CSV
- A function to export all transactions from `transactions.txt` into a CSV file.
- The CSV file should have the following columns: `Date`, `Type`, `Category`, `Description`, `Amount`.
- The user should be prompted for the filename/path to save the CSV file.

### 2. Export to JSON
- A function to export all transactions from `transactions.txt` into a JSON file.
- The JSON file should be an array of objects, where each object represents a transaction.
- The user should be prompted for the filename/path to save the JSON file.

### 3. Import from CSV
- A function to import transactions from a CSV file.
- The CSV file must have the same columns: `Date`, `Type`, `Category`, `Description`, `Amount`.
- The function should validate the data in each row.
- Valid transactions should be appended to `transactions.txt`.
- The user should be shown a summary of how many transactions were imported and how many failed.

## Success Criteria
✅ Can export all transactions to a CSV file.
✅ Can export all transactions to a JSON file.
✅ Can import transactions from a CSV file.
✅ The import process is robust and handles errors gracefully.
✅ Data is correctly formatted in the exported files.

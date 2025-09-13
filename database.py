import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            monthly_limit REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(date, amount, description, category):
    """Add a new expense to the database."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, amount, description, category)
        VALUES (?, ?, ?, ?)
    ''', (date, amount, description, category))
    conn.commit()
    conn.close()

def get_expenses(start_date=None, end_date=None, category=None):
    """Retrieve expenses from the database with optional filters."""
    conn = sqlite3.connect('expenses.db')
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if category:
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY date DESC"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_total_spent(category=None, month=None, year=None):
    """Get total amount spent, optionally filtered by category, month, year."""
    conn = sqlite3.connect('expenses.db')
    query = "SELECT SUM(amount) FROM expenses WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if month and year:
        query += " AND strftime('%m', date) = ? AND strftime('%Y', date) = ?"
        params.extend([f"{month:02d}", str(year)])
    cursor = conn.cursor()
    cursor.execute(query, params)
    total = cursor.fetchone()[0] or 0.0
    conn.close()
    return total

def set_budget(category, monthly_limit):
    """Set or update monthly budget for a category."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO budgets (category, monthly_limit)
        VALUES (?, ?)
    ''', (category, monthly_limit))
    conn.commit()
    conn.close()

def get_budget(category):
    """Get the monthly budget for a category."""
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT monthly_limit FROM budgets WHERE category = ?", (category,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0.0

def export_expenses_to_csv(filename):
    """Export all expenses to a CSV file."""
    df = get_expenses()
    df.to_csv(filename, index=False)

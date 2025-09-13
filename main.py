import streamlit as st
import pandas as pd
from datetime import datetime
from database import init_db, add_expense, get_expenses, set_budget, export_expenses_to_csv
from categorization import auto_categorize
from visualization import plot_pie_chart, plot_monthly_trends, get_image_base64
from utils import check_budget_alerts, split_bill, generate_ai_insights, filter_expenses, export_to_csv

# Initialize database
init_db()

# Function to add sample data
def add_sample_data():
    sample_expenses = [
        ('2023-10-01', 50.0, 'Grocery shopping at supermarket', 'groceries'),
        ('2023-10-02', 20.0, 'Bus ticket', 'travel'),
        ('2023-10-03', 100.0, 'Electricity bill', 'bills'),
        ('2023-10-04', 30.0, 'Movie tickets', 'entertainment'),
        ('2023-10-05', 200.0, 'New shoes', 'shopping'),
        ('2023-10-06', 15.0, 'Pharmacy', 'health'),
        ('2023-10-07', 75.0, 'Dinner at restaurant', 'entertainment'),
    ]
    for date, amount, desc, cat in sample_expenses:
        add_expense(date, amount, desc, cat)
    # Set sample budgets
    set_budget('groceries', 200.0)
    set_budget('entertainment', 100.0)

st.title("Smart Expense Manager")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Add Expense", "View Expenses", "Visualizations", "Budget & Alerts", "Bill Splitter", "AI Insights", "Export"])

# Add sample data button
if st.sidebar.button("Add Sample Data"):
    add_sample_data()
    st.sidebar.success("Sample data added!")

if page == "Add Expense":
    st.header("Add New Expense")
    date = st.date_input("Date", datetime.today())
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    description = st.text_input("Description")
    category = st.selectbox("Category", ["auto"] + list(['groceries', 'travel', 'bills', 'entertainment', 'shopping', 'health', 'other']))
    
    if category == "auto":
        category = auto_categorize(description)
        st.write(f"Auto-categorized as: {category}")
    
    if st.button("Add Expense"):
        add_expense(date.strftime('%Y-%m-%d'), amount, description, category)
        st.success("Expense added successfully!")

elif page == "View Expenses":
    st.header("View Expenses")
    expenses_df = get_expenses()
    if not expenses_df.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox("Filter by Category", ["All"] + list(expenses_df['category'].unique()))
        with col2:
            start_date = st.date_input("Start Date", value=pd.to_datetime(expenses_df['date'].min()))
        with col3:
            end_date = st.date_input("End Date", value=pd.to_datetime(expenses_df['date'].max()))
        
        filtered_df = filter_expenses(expenses_df, 
                                      category=None if category_filter == "All" else category_filter,
                                      start_date=start_date.strftime('%Y-%m-%d'),
                                      end_date=end_date.strftime('%Y-%m-%d'))
        st.dataframe(filtered_df)
        st.write(f"Total Expenses: ${filtered_df['amount'].sum():.2f}")
    else:
        st.write("No expenses found.")

elif page == "Visualizations":
    st.header("Expense Visualizations")
    expenses_df = get_expenses()
    if not expenses_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Pie Chart by Category")
            pie_plt = plot_pie_chart(expenses_df)
            st.pyplot(pie_plt)
        with col2:
            st.subheader("Monthly Trends")
            trend_plt = plot_monthly_trends(expenses_df)
            st.pyplot(trend_plt)
    else:
        st.write("No data to visualize.")

elif page == "Budget & Alerts":
    st.header("Budget Management & Alerts")
    category = st.selectbox("Category", ['groceries', 'travel', 'bills', 'entertainment', 'shopping', 'health', 'other'])
    budget = st.number_input("Monthly Budget", min_value=0.0, step=0.01)
    if st.button("Set Budget"):
        set_budget(category, budget)
        st.success("Budget set!")
    
    alerts = check_budget_alerts()
    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.info("All budgets are under control.")

elif page == "Bill Splitter":
    st.header("Bill Splitter")
    total_amount = st.number_input("Total Bill Amount", min_value=0.0, step=0.01)
    num_people = st.number_input("Number of People", min_value=1, step=1)
    if st.button("Split Bill"):
        splits = split_bill(total_amount, num_people)
        st.write("Bill Split:")
        for person, amount in splits.items():
            st.write(f"{person}: ${amount:.2f}")

elif page == "AI Insights":
    st.header("AI Insights")
    insights = generate_ai_insights()
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.write("Not enough data for insights.")

elif page == "Export":
    st.header("Export Expenses")
    expenses_df = get_expenses()
    if not expenses_df.empty:
        filename = st.text_input("Filename (without extension)", "expenses")
        if st.button("Export to CSV"):
            export_to_csv(expenses_df, f"{filename}.csv")
            st.success(f"Exported to {filename}.csv")
    else:
        st.write("No expenses to export.")

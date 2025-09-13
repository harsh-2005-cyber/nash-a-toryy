import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from io import BytesIO
import base64

def plot_pie_chart(expenses_df):
    """Generate a pie chart of expenses by category."""
    category_sums = expenses_df.groupby('category')['amount'].sum()
    plt.figure(figsize=(6,6))
    plt.pie(category_sums, labels=category_sums.index, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')
    plt.tight_layout()
    return plt

def plot_monthly_trends(expenses_df):
    """Generate a line plot of monthly expense trends."""
    expenses_df['date'] = pd.to_datetime(expenses_df['date'])
    expenses_df['month'] = expenses_df['date'].dt.to_period('M')
    monthly_sums = expenses_df.groupby('month')['amount'].sum()
    plt.figure(figsize=(8,4))
    sns.lineplot(x=monthly_sums.index.astype(str), y=monthly_sums.values)
    plt.xticks(rotation=45)
    plt.title('Monthly Expense Trends')
    plt.xlabel('Month')
    plt.ylabel('Total Spent')
    plt.tight_layout()
    return plt

def get_image_base64(plt):
    """Convert a matplotlib plot to a base64 encoded PNG image."""
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_base64

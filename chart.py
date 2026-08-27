import sqlite3
import pandas as pd
import plotly.express as px

# Connect to database
connection = sqlite3.connect("database/sales.db")

# Get sales by sub-category
query = """
SELECT "Sub-Category", SUM(Sales) AS Total_Sales
FROM sales
GROUP BY "Sub-Category"
ORDER BY Total_Sales DESC
"""

df = pd.read_sql_query(query, connection)

connection.close()

# Create line chart
fig = px.line(
    df,
    x="Sub-Category",
    y="Total_Sales",
    title="Sales by Sub-Category"
)

# Display chart
fig.show()
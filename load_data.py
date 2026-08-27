import pandas as pd
import sqlite3
import os

# Load cleaned data
df = pd.read_csv("data/cleaned_data.csv")

# Make sure database folder exists
os.makedirs("database", exist_ok=True)

# Create SQLite database
connection = sqlite3.connect("database/sales.db")

# Create sales table
df.to_sql("sales", connection, if_exists="replace", index=False)

# Check number of rows
cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM sales")

count = cursor.fetchone()[0]

print("Database created successfully!")
print("Number of rows:", count)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables=cursor.fetchall()
print("tables in database:")
for table in tables:
    print(table[0])

connection.close()
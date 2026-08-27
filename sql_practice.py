import sqlite3
connection=sqlite3.connect("database/sales.db")
cursor=connection.cursor()
cursor.execute("""SELECT "sub-category",SUM(Sales) AS total_sales FROM sales GROUP BY "sub-category" ORDER BY total_sales DESC LIMIT 10""")
results=cursor.fetchall()
print("top 10 sub- categories by Sales:")
for row in results:
    print(row)
 
import os
import sqlite3
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
from dotenv import load_dotenv
from google import genai
#load api key
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    print("API key not found")
    exit()
# connect to the gemini
client=genai.Client(api_key=api_key)

# ask the user a question
question=input("ask a question about your sales data:")

# tell gemini about our database
prompt=f"""you are a sql expect.
convert the users question into SQLite SQL.
Database table:sales
Available columns:
Ship Mode
Segment
Country
State
Postal Code
Region Category
Sub-Category
Sales
Quantity
Discount
Profit

User question:
{question}
Return ONLY the SQL query.
Do not eexplain anything."""

# gemini generates sql
response=client.models.generate_content(model="gemini-3.6-flash",contents=prompt)
sql_query=response.text.strip()
print("\n generated sql:")
print(sql_query)

# removd markdown code fences it gemini adds them
sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

# connect to Sqlite
db_path=os.path.join(BASE_DIR,"database","sales.db")
connection=sqlite3.connect(db_path)
cursor=connection.cursor()
try:
    #execute geminis sql
    cursor.execute(sql_query)
    #get results
    results=cursor.fetchall()
    print("\nResults:")
    for row in results:
        print(row)
except sqlite3.Error as error:
    print("\nSQL Error:",error)
finally:
    connection.close()

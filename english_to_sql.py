import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    print("API key not found")
    exit()
client= genai.Client(api_key=api_key)
question="show the top 5 sub-categories by sales."
prompt=f"""you are a sql expert. 
convert the following english question into sqllite sql.
database table name: sales
Available columns:
Ship Mode
Segment
Country
City
State
Postal Code
Region
Category
sub-Category
Sales
Quantity
Discount
Profit

English question:
{question}
Return ONLY the SQL query.
Do not explain anything."""
response=client.models.generate_content(model="gemini-3.6-flash",contents=prompt)
print("generated sql:")
print(response.text)
import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# Streamlit page
st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI SQL Assistant")

st.write(
    "Ask questions about your sales data using natural language."
)

# User question
question = st.text_input(
    "Ask a question about your sales data:"
)

# Submit
if st.button("Submit"):

    if not question:
        st.warning("Please enter a question.")
        st.stop()

    # Gemini SQL prompt
    prompt = f"""
You are a SQL expert.

Convert the user's English question into SQLite SQL.

Database table name: sales

Available columns:
Ship Mode
Segment
Country
City
State
Postal Code
Region
Category
Sub-Category
Sales
Quantity
Discount
Profit

User question:
{question}

Rules:
- Use only the columns listed above.
- Use SQLite SQL syntax.
- Return ONLY the SQL query.
- Do not explain the query.
"""

    # Generate SQL
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        sql_query = response.text.strip()

        # Remove Markdown code fences
        if sql_query.startswith(""):
            parts = sql_query.split("\n", 1)

            if len(parts) == 2:
                sql_query = parts[1]

        if sql_query.endswith(""):
            sql_query = sql_query.rsplit("```", 1)[0]

        sql_query = sql_query.strip()

    except Exception as error:
        st.error(f"Gemini error: {error}")
        st.stop()

    # Display SQL
    st.subheader("Generated SQL")

    st.code(
        sql_query,
        language="sql"
    )

    # Database path
    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    db_path = os.path.join(
        base_dir,
        "database",
        "sales.db"
    )

    # Execute SQL
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(sql_query)

        results = cursor.fetchall()

        # Column names
        column_names = [
            description[0]
            for description in cursor.description
        ]

        # Results
        st.subheader("Results")

        if results:

            table_data = []

            for row in results:
                table_data.append(
                    dict(zip(column_names, row))
                )

            st.dataframe(
                table_data,
                use_container_width=True
            )

        else:
            st.info("The query returned no results.")

        # Chart
        if results and len(column_names) >= 2:

            st.subheader("Chart")

            chart_data = {}

            for row in results:
                chart_data[row[0]] = row[1]

            st.bar_chart(chart_data)

        # AI Business Summary
        if results:

            summary_prompt = f"""
You are a professional business analyst.

The user asked:
{question}

The SQL query used:
{sql_query}

The actual results from the sales database are:
{results}

Analyze ONLY the actual results provided above.

Write a simple business summary.

Include:
1. The highest-performing item.
2. The lowest-performing item among the results.
3. One useful business insight.

Do not invent data.
Do not mention SQL or programming.
Keep the summary short and easy to understand.
Use 3 or 4 sentences.
"""

            summary_response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=summary_prompt
            )

            st.subheader("🤖 AI Business Summary")

            st.write(
                summary_response.text
            )

        connection.close()

    except sqlite3.Error as error:
        st.error(f"SQL Error: {error}")

    except Exception as error:
        st.error(f"Error: {error}")
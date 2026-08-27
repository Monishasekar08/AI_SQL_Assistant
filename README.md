# 🤖 AI SQL Assistant

An AI-powered data analytics dashboard that converts natural-language questions into SQL queries and provides interactive business insights from sales data.

## 📌 Project Overview

AI SQL Assistant allows users to ask questions about sales data in simple English.

The application uses Google Gemini AI to convert the user's question into an SQL query, executes the query on a SQLite database, and displays the results with charts and business insights.

## ✨ Features

- 💬 Ask questions in natural language
- 🤖 AI-powered English-to-SQL conversion
- 🗄️ SQL query execution using SQLite
- 📊 Interactive data visualization
- 📈 Sales analytics dashboard
- 💡 AI-generated business insights
- 📋 Display SQL query and query results
- 🎯 Easy-to-use Streamlit interface

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- SQL
- SQLite
- Google Gemini AI
- Streamlit
- Matplotlib

## 📂 Project Structure

```text
AI_SQL_Assistant/
│
├── data/
│   ├── Superstore.csv
│   └── cleaned_data.csv
│
├── src/
│   └── data_cleaning.py
│
├── app.py
├── chart.py
├── english_to_sql.py
├── execute_ai_sql.py
├── gemini_test.py
├── load_data.py
├── sql_practice.py
├── requirements.txt
├── README.md
└── .gitignore

▶️ How to Run:

1. Clone the repository
git clone https://github.com/Monishasekar08/AI_SQL_Assistant.git
2. Open the project
cd AI_SQL_Assistant
3. Create a virtual environment
python -m venv .venv
4. Activate the virtual environment
Windows:
.venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
6. Add your Gemini API key
Create a .env file and add your Gemini API key:
GEMINI_API_KEY=your_api_key_here
7. Run the Streamlit application
streamlit run app.py
The application will open in your browser.

💬 Example Questions

Users can ask questions such as:
What are the top 5 sub-categories by sales?
Show total sales by region.
Which category has the highest profit?
Show sales by category.
What are the best-performing products?

📊 Dashboard Workflow:

User Question
      ↓
Gemini AI
      ↓
English → SQL
      ↓
SQLite Database
      ↓
Query Results
      ↓
Charts
      ↓
Business Insights

🎯 Project Goal:

The goal of this project is to make data analysis easier by allowing users to interact with sales data using natural language instead of writing SQL queries manually.

👩‍💻 Author:

Monisha Sekar
MSc Computer Science | Data Analytics Enthusiast
import os
import sqlite3

import streamlit as st
from dotenv import load_dotenv
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ================================
       MAIN BACKGROUND
       ================================ */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99, 102, 241, 0.20),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(168, 85, 247, 0.18),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #080d1c 0%,
                #111827 50%,
                #1e1b4b 100%
            );
    }

    .block-container {
        max-width: 1250px;
        padding-top: 30px;
        padding-bottom: 40px;
    }


    /* ================================
       GENERAL TEXT
       ================================ */

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #ffffff !important;
    }

    .stApp p {
        color: #f1f5f9 !important;
    }

    .stApp label {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: #e2e8f0 !important;
    }


    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0f172a,
                #1e1b4b,
                #312e81
            );

        border-right: 1px solid rgba(255,255,255,0.15);
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] p {
        color: #e2e8f0 !important;
    }


    /* ================================
       HERO
       ================================ */

    .hero-container {
        background:
            linear-gradient(
                135deg,
                #4338ca,
                #6d28d9,
                #a21caf
            );

        padding: 38px 42px;

        border-radius: 25px;

        border: 1px solid rgba(255,255,255,0.20);

        box-shadow:
            0 20px 50px rgba(0,0,0,0.40);

        margin-bottom: 32px;
    }

    .hero-badge-text {
        color: #ddd6fe !important;

        font-size: 13px;

        font-weight: 800;

        letter-spacing: 1.5px;
    }

    .hero-title-text {
        color: #ffffff !important;

        font-size: 44px;

        font-weight: 900;

        line-height: 1.15;

        margin-top: 8px;
    }

    .hero-description-text {
        color: #f5f3ff !important;

        font-size: 16px;

        line-height: 1.65;

        max-width: 850px;

        margin-top: 12px;
    }


    /* ================================
       ASK YOUR DATA
       ================================ */

    .stApp h2 {
        color: #ffffff !important;

        font-size: 28px !important;

        font-weight: 850 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #e2e8f0 !important;

        font-size: 16px !important;

        font-weight: 500 !important;
    }


    /* ================================
       TEXT INPUT
       ================================ */

    .stTextInput label {
        color: #ffffff !important;

        font-size: 16px !important;

        font-weight: 800 !important;
    }

    .stTextInput input {
        background-color: #0f172a !important;

        color: #ffffff !important;

        border: 2px solid #6366f1 !important;

        border-radius: 13px !important;

        font-size: 16px !important;

        padding: 14px 16px !important;

        min-height: 52px !important;
    }

    .stTextInput input::placeholder {
        color: #cbd5e1 !important;

        opacity: 1 !important;
    }

    .stTextInput input:focus {
        border-color: #a78bfa !important;

        box-shadow:
            0 0 0 3px rgba(167,139,250,0.25) !important;
    }


    /* ================================
       BUTTON
       ================================ */

    .stButton > button {
        width: 100%;

        min-height: 52px;

        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6,
                #a855f7
            ) !important;

        color: #ffffff !important;

        border: none !important;

        border-radius: 13px !important;

        font-size: 16px !important;

        font-weight: 800 !important;

        box-shadow:
            0 10px 25px rgba(99,102,241,0.35);
    }

    .stButton > button:hover {
        color: #ffffff !important;

        transform: translateY(-2px);

        box-shadow:
            0 15px 30px rgba(139,92,246,0.45);
    }


    /* ================================
       METRIC CARDS
       ================================ */

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #1e293b,
                #172554
            ) !important;

        border: 1px solid rgba(129,140,248,0.40);

        padding: 20px !important;

        border-radius: 18px;

        box-shadow:
            0 10px 25px rgba(0,0,0,0.30);
    }

    [data-testid="stMetricLabel"] {
        color: #e2e8f0 !important;

        font-size: 14px !important;

        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;

        font-size: 30px !important;

        font-weight: 900 !important;
    }


    /* ================================
       SQL CODE
       ================================ */

    [data-testid="stCodeBlock"] {
        border-radius: 15px !important;

        border: 1px solid rgba(99,102,241,0.50);

        box-shadow:
            0 10px 25px rgba(0,0,0,0.30);
    }


    /* ================================
       DATAFRAME
       ================================ */

    [data-testid="stDataFrame"] {
        border-radius: 15px;

        overflow: hidden;

        box-shadow:
            0 10px 25px rgba(0,0,0,0.25);
    }


    /* ================================
       BUSINESS INSIGHTS
       ================================ */

    [data-testid="stAlert"] {
        border-radius: 16px !important;
    }

    [data-testid="stAlert"] p {
        color: #ffffff !important;

        font-size: 15px !important;

        line-height: 1.7 !important;

        font-weight: 500 !important;
    }


    /* ================================
       FOOTER
       ================================ */

    .footer-container {
        text-align: center;

        margin-top: 45px;

        padding-top: 20px;

        border-top: 1px solid rgba(255,255,255,0.10);
    }

    .footer-main-text {
        color: #e2e8f0 !important;

        font-size: 13px;

        font-weight: 700;
    }

    .footer-sub-text {
        color: #94a3b8 !important;

        font-size: 12px;

        margin-top: 5px;
    }


    /* ================================
       STREAMLIT CLEANUP
       ================================ */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GEMINI API
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "❌ Gemini API key not found. Please check your .env file."
    )
    st.stop()

client = genai.Client(
    api_key=api_key
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# 🤖 AI SQL Assistant")

    st.markdown("### Smart Sales Analytics")

    st.divider()

    st.markdown("### 📊 Dashboard")

    st.write(
        "Ask questions about your sales data using natural language."
    )

    st.divider()

    st.markdown("### 🧠 Technologies")

    st.write("🐍 Python")
    st.write("🤖 Gemini AI")
    st.write("🗄️ SQLite")
    st.write("📊 Streamlit")
    st.write("📈 Data Analytics")

    st.divider()

    st.markdown("### 💡 Example Questions")

    st.write("• Show top 5 sub-categories by sales")
    st.write("• Show total sales")
    st.write("• Show sales by region")
    st.write("• Show profit by category")
    st.write("• Show top 10 sub-categories")


# ============================================================
# HERO
# IMPORTANT:
# No visible HTML tags are used here.
# ============================================================

st.markdown(
    '<div class="hero-container">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-badge-text">✨ AI-POWERED DATA ANALYTICS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title-text">🤖 AI SQL Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-description-text">'
    'Transform natural-language business questions into SQL, '
    'analyze your sales database, visualize results, '
    'and receive AI-powered business insights.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ASK YOUR DATA
# ============================================================

st.header("💬 Ask Your Data")

st.caption(
    "Ask your sales data anything in simple English."
)


# ============================================================
# QUESTION INPUT
# ============================================================

question = st.text_input(
    "Your question",
    placeholder=(
        "Example: Show me the top 10 sub-categories by sales."
    )
)

analyze = st.button(
    "🔍 Analyze Data"
)


# ============================================================
# ANALYZE
# ============================================================

if analyze:

    if not question:

        st.warning(
            "⚠️ Please enter a question first."
        )

        st.stop()


    # ========================================================
    # GEMINI PROMPT
    # ========================================================

    prompt = f"""
You are an expert SQL data analyst.

Convert the user's natural-language question into SQLite SQL.

Database table:
sales

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
- Use only the available columns.
- Use SQLite syntax.
- Use exact column names where necessary.
- Return ONLY the SQL query.
- Do not explain the SQL.
- Do not use Markdown code fences.
"""


    # ========================================================
    # GENERATE SQL
    # ========================================================

    with st.spinner(
        "🤖 Gemini is generating your SQL..."
    ):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            sql_query = response.text.strip()

            # Remove Markdown code fences if returned
            if sql_query.startswith("```"):

                lines = sql_query.splitlines()

                if len(lines) > 1:
                    lines = lines[1:]

                if (
                    lines
                    and lines[-1].strip() == "```"
                ):
                    lines = lines[:-1]

                sql_query = "\n".join(
                    lines
                ).strip()

        except Exception as error:

            st.error(
                f"❌ Gemini Error: {error}"
            )

            st.stop()


    # ========================================================
    # GENERATED SQL
    # ========================================================

    st.header("🧠 Generated SQL")

    st.caption(
        "✨ Generated automatically by Gemini AI"
    )

    st.code(
        sql_query,
        language="sql"
    )


    # ========================================================
    # DATABASE PATH
    # ========================================================

    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    db_path = os.path.join(
        base_dir,
        "database",
        "sales.db"
    )


    # ========================================================
    # EXECUTE SQL
    # ========================================================

    try:

        connection = sqlite3.connect(
            db_path
        )

        cursor = connection.cursor()

        cursor.execute(
            sql_query
        )

        results = cursor.fetchall()

        column_names = [
            description[0]
            for description in cursor.description
        ]


        # ====================================================
        # ANALYSIS OVERVIEW
        # ====================================================

        st.header(
            "📊 Analysis Overview"
        )

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "📊 Rows Returned",
                len(results)
            )


        with col2:

            st.metric(
                "🧠 AI Status",
                "Analyzed"
            )


        with col3:

            st.metric(
                "🗄️ Database",
                "SQLite"
            )


        # ====================================================
        # RESULTS
        # ====================================================

        st.header(
            "📋 Analysis Results"
        )

        if results:

            table_data = []

            for row in results:

                table_data.append(
                    dict(
                        zip(
                            column_names,
                            row
                        )
                    )
                )

            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No results were returned."
            )


        # ====================================================
        # CHART
        # ====================================================

        if results and len(column_names) >= 2:

            st.header(
                "📈 Data Visualization"
            )

            chart_data = {}

            for row in results:

                try:

                    chart_data[
                        str(row[0])
                    ] = float(row[1])

                except (
                    ValueError,
                    TypeError
                ):

                    pass


            if chart_data:

                st.bar_chart(
                    chart_data,
                    use_container_width=True
                )

            else:

                st.info(
                    "This result is not suitable for a numeric chart."
                )


        # ====================================================
        # AI BUSINESS INSIGHTS
        # ====================================================

        if results:

            summary_prompt = f"""
You are a professional business analyst.

User question:
{question}

SQL query:
{sql_query}

Actual database results:
{results}

Analyze ONLY the actual results.

Provide:
1. The most important finding.
2. The highest-performing item if applicable.
3. The lowest-performing item if applicable.
4. One practical business insight.

Do not invent numbers.
Do not mention SQL, Python, Gemini, or programming.
Do not make unsupported assumptions.

Write 3 to 4 clear sentences.
"""


            with st.spinner(
                "💡 Generating business insights..."
            ):

                try:

                    summary_response = (
                        client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=summary_prompt
                        )
                    )

                    summary_text = (
                        summary_response.text.strip()
                    )

                except Exception as error:

                    summary_text = (
                        "Unable to generate business "
                        f"summary: {error}"
                    )


            st.header(
                "💡 AI Business Insights"
            )

            st.info(
                "🤖 Business Analyst Summary\n\n"
                + summary_text
            )


        # ====================================================
        # CLOSE DATABASE
        # ====================================================

        connection.close()


    except sqlite3.Error as error:

        st.error(
            f"❌ SQL Error: {error}"
        )

    except Exception as error:

        st.error(
            f"❌ Application Error: {error}"
        )


# ============================================================
# FOOTER
# IMPORTANT:
# No HTML is used here.
# ============================================================

st.divider()

st.caption(
    "AI SQL Assistant • Smart Sales Analytics Dashboard"
)

st.caption(
    "Built with Python • SQLite • Gemini AI • Streamlit"
)
import streamlit as st
from pathlib import Path
import urllib
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import pyodbc
import sqlite3
from langchain_groq import ChatGroq

# --- Page Setup ---
st.set_page_config(page_title="Langchain: Chat with SQL", page_icon="🦜")
st.title("🦜 Langchain: Chat with SQL")

# --- Constants ---
LOCAL_DB = "USE_LOCALDB"
SSMS_DB = "USE_SSMS"
DB_OPTIONS = ["Use SQLite3 DATABASE - Student.db", "Connect to your SSMS SQL Database"]

# --- Sidebar Inputs ---
api_key = st.sidebar.text_input(label="Enter your Groq API Key", type="password")
selected_opt = st.sidebar.radio("Choose the DB you want to chat with:", options=DB_OPTIONS)

# --- Early Exit if API Key is Missing ---
if not api_key:
    st.info("Please provide your Groq API key.")
    st.stop()

# --- Initialize LLM Safely ---
@st.cache_resource
def get_llm(api_key):
    return ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

llm = get_llm(api_key)

# --- Determine DB Type ---
db_uri = LOCAL_DB if selected_opt == DB_OPTIONS[0] else SSMS_DB

# --- SSMS Inputs ---
ssms_host = ssms_user = ssms_pwd = ssms_db = None
if db_uri == SSMS_DB:
    ssms_host = st.sidebar.text_input("SSMS Host")
    ssms_user = st.sidebar.text_input("SSMS User")
    ssms_pwd = st.sidebar.text_input("SSMS Password", type="password")
    ssms_db = st.sidebar.text_input("SSMS Database Name")

# --- Database Config ---
@st.cache_resource(ttl="2h")
def configure_db(db_uri, ssms_host=None, ssms_user=None, ssms_pwd=None, ssms_db=None):
    if db_uri == LOCAL_DB:
        db_path = (Path(__file__).parent / "Student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite://", creator=creator))

    elif db_uri == SSMS_DB:
        if not all([ssms_host, ssms_user, ssms_pwd, ssms_db]):
            st.error("All SSMS connection parameters are required.")
            st.stop()

        connection_string = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={ssms_host};"
            f"DATABASE={ssms_db};"
            f"UID={ssms_user};"
            f"PWD={ssms_pwd};"
            "TrustServerCertificate=yes;"
        )
        odbc_str = urllib.parse.quote_plus(connection_string)
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={odbc_str}")
        return SQLDatabase(engine)

# --- Load DB ---
db = configure_db(db_uri, ssms_host, ssms_user, ssms_pwd, ssms_db) if db_uri == SSMS_DB else configure_db(db_uri)

##toolkit
toolkit = SQLDatabaseToolkit(db =db,llm=llm)
agent =create_sql_agent(llm=llm,toolkit=toolkit,verbose=True,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)


if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role":"assistant","content":"How can I help You?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({'role':'user','content':user_query})
    st.chat_message('user').write(user_query)

    with st.chat_message('assistant'):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query,callbacks=[streamlit_callback])
        st.session_state.messages.append({'role':'assistant','content':response})
        st.write(response)

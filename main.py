import streamlit as st
import psycopg2

st.title('medical database')

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


tab1, tab2 = st.tabs(["Search", "Reporting"])

with st.container():
    tab1.subheader("A tab with a chart")
    tab1.write("tab1")

with st.container():
    tab2.subheader("A tab with the data")
    tab2.write("tab2")


# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from public.user;")

# Print results.

for row in rows:
    st.write(row)



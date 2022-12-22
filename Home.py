import streamlit as st
import psycopg2


### Layout ###
st.title("Medical Database")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.write("# Welcome to Medical Database! 👋")

tab1, tab2, tab3 = st.tabs(["Medicine Side Effects", 
                            "Analysis",
                            "Your profile"])

### End of Layout ###

with tab1:
    st.header("Side Effects of Medicines")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    import tab1 as tab1i
    ### database ###
    
    # Initialize connection.
    # Uses st.experimental_singleton to only run once.
    
    #@st.experimental_singleton
    #def init_connection():
    #    return psycopg2.connect(**st.secrets["postgres"])

    #conn = init_connection()

    # Perform query.
    # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    #@st.experimental_memo(ttl=600)
    #def run_query(query):
        #with conn.cursor() as cur:
            #cur.execute(query)
            #return cur.fetchall()

    #rows = run_query("SELECT * from public.user;")

    # Print results.

    #for row in rows:
        #st.write(row)

with tab2:
    st.header("Analysing Side Effects")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("Your Profile")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
    
    
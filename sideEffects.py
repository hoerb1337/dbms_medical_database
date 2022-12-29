import streamlit as st
import psycopg2

# Backend service
#import sideEffectsService
import database

class render_tab1:
    def __init__(self):
        st.write("Browse for side effects of selected medicines")
        
        db = database.db_connection()
        db_connection = db.connect_postgres()
        db_cur = db_connection.cursor()
        db_cur.execute("select commercial_name from dbms.medicines;")
        for record in db_cur:
            st.write(f"{record[0]}")
        
        medicine_selection = st.multiselect('Select up to two medicines:',
                                [
                                    'Green', 'Yellow', 'Red', 'Blue'
                                    ]
                                )

        st.write('You selected:', medicine_selection)
        
        agree = st.checkbox('I want side effects of combination')

        if agree:
            st.write('Great!')
        
        st.button(label="Lookup side effects")

        #self.name = name
        #self.age = age


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

if __name__ == "__main__":
    pass
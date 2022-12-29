import streamlit as st
#import psycopg2

# Backend service
#import sideEffectsService
#import database

class render_tab1:
    def __init__(self):
        st.subheader("Browse for side effects of selected medicines")

        options = st.multiselect('Select up to two medicines:',
                                ['Green', 'Yellow', 'Red', 'Blue'],
                                ['Yellow', 'Red']
                                )

        st.write('You selected:', options)
        
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
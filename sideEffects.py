import streamlit as st
#import psycopg2

# Backend service
#import sideEffectsService
#import database

class render_tab1:
    def __init__(self):
        st.write("Browse for side effects of selected medicines")

        options = st.multiselect('Select up to two medicines:',
                                ['Green', 'Yellow', 'Red', 'Blue'],
                                ['Yellow', 'Red']
                                )

        st.write('You selected:', options)
        
        col1, col2 = st.columns([1, 3], gap="small")
        with col1:
            agree = st.checkbox('I want side effects of combination')

            if agree:
                st.write('Great!')
        
        with col2:
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
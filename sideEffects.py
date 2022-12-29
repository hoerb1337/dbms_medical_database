import streamlit as st
import psycopg2

# Backend service
import sideEffectsService


class render_tab1:
    def __init__(self):
        st.write("Browse and report for side effects of selected medicines")
        
        # Call Backendservice
        callSideEffectsBackend = sideEffectsService.data4SideEffects()
        # Get list of medicines
        getListMedicines = callSideEffectsBackend.list_medicines()
        
        # Multiselect
        medicine_selection = st.multiselect('Select up to two medicines:',
                                            getListMedicines
                                            )
        # Check number of meds
        check_nr_meds = callSideEffectsBackend.max_nr_medicines(medicine_selection)

        if check_nr_meds == 200:
            st.write('You selected:', medicine_selection)
            agree = st.checkbox('I want side effects of combination')

            if agree:
                st.write('Great!')
        
            st.button(label="Lookup side effects")
        else:
            st.error("You chose more than two medicines. Please select only two medicines.")
        
        # 
        

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
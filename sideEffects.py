import streamlit as st
import psycopg2
import pandas as pd

# Backend service
import sideEffectsService


class render_tab1:
    def __init__(self):
        st.write("Browse and report for side effects of selected medicines")
        
    def selection(self):
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
            #st.write('You selected:', medicine_selection)
            combo = False
            if st.checkbox('I want side effects of combination'):
                combo = True
            
            st.write(combo)
            
            return medicine_selection, combo
            
        elif check_nr_meds == 422:
            st.warning("Please choose at least one medicine.")
        elif check_nr_meds == 401:
            st.error("You chose more than two medicines. Please select only two medicines.")
        
    def display_sideEffects(self, selected_meds, combo):
        # No combination of meds
        if combo == False:
            # Call Backendservice
            callSideEffectsBackend = sideEffectsService.data4SideEffects()
            listSideEffects_med1, listSideEffects_med2 = callSideEffectsBackend.get_listSideEffects(selected_meds[0], selected_meds[1])
            d = {'col1': listSideEffects_med1, 'col2': listSideEffects_med2}
            df = pd.DataFrame(data=d)
            st.dataframe(df)
            
        elif combo == True:
            pass

if __name__ == "__main__":
    pass
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
        check_nr_meds, nr_selected_meds = callSideEffectsBackend.max_nr_medicines(medicine_selection)

        if check_nr_meds == 200:
            #st.write('You selected:', medicine_selection)
            combo = "False"
            if st.checkbox('I want side effects of combination'):
                combo = "True"

            return medicine_selection, combo, nr_selected_meds
            
        elif check_nr_meds == 422:
            st.warning("Please choose at least one medicine.")
            combo = None
            return medicine_selection, combo, nr_selected_meds
        elif check_nr_meds == 401:
            st.error("You chose more than two medicines. Please select only two medicines.")
            combo = None
            return medicine_selection, combo, nr_selected_meds
        
    def display_sideEffects(self, nr_selected_meds, selected_meds, combo):
        # No combination of meds
        if combo == "False":
            
            # Call Backendservice
            callSideEffectsBackend = sideEffectsService.data4SideEffects()
            if nr_selected_meds == 2:
                listSideEffects_med1 = callSideEffectsBackend.get_listSideEffects(selected_meds[0])
                listSideEffects_med2 = callSideEffectsBackend.get_listSideEffects(selected_meds[1])
                d1 = {'Side effects from' + selected_meds[0]: listSideEffects_med1}
                d2 = {'Side effects from' + selected_meds[1]: listSideEffects_med2}
                df1 = pd.DataFrame(data=d1)
                df2 = pd.DataFrame(data=d2)
                concat = pd.concat([df1, df2], ignore_index=False, axis=1)
                st.dataframe(concat, use_container_width=True)
            elif nr_selected_meds == 1:
                listSideEffects_med1 = callSideEffectsBackend.get_listSideEffects(selected_meds[0])
                d1 = {'Side effects from' + selected_meds[0]: listSideEffects_med1}
                df1 = pd.DataFrame(data=d1)
                st.dataframe(df1, use_container_width=True)
        elif combo == "True":
            pass

if __name__ == "__main__":
    pass
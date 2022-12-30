import streamlit as st
import pandas as pd

# Backend service
import sideEffectsService


class render_tab1:
    def __init__(self):
        st.subheader("Browse and report for side effects of selected medicines")
        
    def selection(self):
        # Call Backendservice
        callSideEffectsBackend = sideEffectsService.data4SideEffects()
        # Get list of medicines
        getListMedicines = callSideEffectsBackend.list_medicines()
        
        # Multiselect UI
        medicine_selection = st.multiselect('Select up to two medicines:',
                                            getListMedicines)
        # Check number of meds
        check_nr_meds, nr_selected_meds = callSideEffectsBackend.max_nr_medicines(medicine_selection)

        if check_nr_meds == 200:
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
            
            # 2 chosen meds
            if nr_selected_meds == 2:
                listSideEffects_med1 = callSideEffectsBackend.get_listSideEffects(selected_meds[0])
                listSideEffects_med2 = callSideEffectsBackend.get_listSideEffects(selected_meds[1])
                
                # Create dataframes
                df1 = callSideEffectsBackend.create_DataFrame(selected_meds[0], listSideEffects_med1)
                df2 = callSideEffectsBackend.create_DataFrame(selected_meds[1], listSideEffects_med2)

                concat_dfs = pd.concat([df1, df2], ignore_index=False, axis=1)
                return st.dataframe(concat_dfs, use_container_width=True)
            
            # 1 chosen med
            elif nr_selected_meds == 1:
                listSideEffects_med1 = callSideEffectsBackend.get_listSideEffects(selected_meds[0])
                
                # Create dataframe
                df1 = callSideEffectsBackend.create_DataFrame(selected_meds[0], listSideEffects_med1)
                return st.dataframe(df1, use_container_width=True)
        
        # Combination of meds
        elif combo == "True":
            pass

if __name__ == "__main__":
    pass
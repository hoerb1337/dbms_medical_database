# External libraries
import streamlit as st


# Backend modules
import analysisService
#

class render_tab2:
    
    def __init__(self):
        st.info("Perform a reverse lookup:\n" +
                "You report your own set of side effect symptoms, " +
                "and we find for you the closest prediction of " +
                "medicines that you could have taken.")

    def select_side_effects(self):
        st.subheader("1. Selection of own side effect symptoms:")
        # Call Backendservice
        callAnalysisBackend = analysisService.data4Analysis()
        
        if st.checkbox('I am taking two medicines in combination',
                       key="checkbox"):
            # Get list of side effects from combo medicines
            st.experimental_rerun
            list_sideEffects = callAnalysisBackend.get_sideEffects(combo="True")

        else:
            # Get list of side effects from mono medicines
            list_sideEffects = callAnalysisBackend.get_sideEffects(combo="False")
        
        # Multiselect UI
        selected_sideEffects = st.multiselect('Select your set of side effects:',
                                                    list_sideEffects,
                                                    key="selected_sideEffects",
                                                    max_selections=2)
        st.write(selected_sideEffects)
        # Check number of meds
        #check_nr_meds, nr_selected_meds = callSideEffectsBackend.max_nr_medicines(medicine_selection)

        #if check_nr_meds == 200:
            #combo = "False"
            #if nr_selected_meds == 2:
                #if st.checkbox('I want side effects of combination'):
                    #combo = "True"

            #return medicine_selection, combo, nr_selected_meds
            
        #elif check_nr_meds == 422:
            #st.warning("Please choose at least one medicine.")
            #combo = None
            #return medicine_selection, combo, nr_selected_meds

        #elif check_nr_meds == 401:
            #st.error("You chose more than two medicines. Please select only two medicines.")
            #combo = None
            #return medicine_selection, combo, nr_selected_meds
        #selected_sideEffects = None

        return selected_sideEffects



if __name__ == "__main__":
    pass
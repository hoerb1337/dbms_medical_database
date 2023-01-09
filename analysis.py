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

    def show_selection_sideEffects(self):
        """UI for choosing side effects by user.

        Args:
            None
        Returns:
            selected_sideEffects: list of chosen side effects
            type: list
            nr_sideEffects: number of chosen side effects
            type: int
        """

        st.subheader("1. Selection of own side effect symptoms:")
        # Call Backendservice
        callAnalysisBackend = analysisService.data4Analysis()
        
        # Checkbox
        if st.checkbox('I am taking two medicines in combination',
                       key="checkbox"):
            
            # Get list of side effects from combo medicines
            combo="True"
            list_sideEffects = callAnalysisBackend.get_sideEffects(combo)

        else:
            # Get list of side effects from mono medicines
            combo="False"
            list_sideEffects = callAnalysisBackend.get_sideEffects(combo)
        
        # Multiselect UI
        selected_sideEffects = st.multiselect('Select your set of side effects:',
                                              list_sideEffects,
                                              key="selected_sideEffects")

        # normalise list of selected side effects
        selected_sideEffects_name, selected_sideEffects_id = callAnalysisBackend.norm_list_se(selected_sideEffects)

        nr_sideEffects = len(selected_sideEffects_name)
        if nr_sideEffects < 1:
            st.warning("Please choose at least one side effect symptom.")

        return selected_sideEffects_name, selected_sideEffects_id, nr_sideEffects, combo
    
    
    def show_reverse_lookup(self, selected_sideEffects_name,
                            selected_sideEffects_id,
                            nr_sideEffects, combo):
        """UI for displaying reverse lookup results.

        Args:
            selected_sideEffects:
            type: list
            nr_sideEffects:
            type: int
        Returns:
            selected_sideEffects: list of chosen side effects
            type: dataframe
        """
        
        # Button:
        if nr_sideEffects >= 1:
            btn_lookup_meds = st.button(label="Lookup potential medicines")
        
            callAnalysisBackend = analysisService.data4Analysis()
        
            # If button clicked:
            if btn_lookup_meds:
                # Start reverse lookup and get results
                results_reLookup = callAnalysisBackend.do_reverse_lookup(selected_sideEffects_name,
                                                                         selected_sideEffects_id,
                                                                         nr_sideEffects,
                                                                         combo)
                
                # Display results from reverse lookup as dataframe
                st.subheader("2. Possible medicines taken")
                
                # Show metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.caption("Most matched selected side effects:")
                    st.metric(label="Ibuprofen", value="86%", delta=None)

                with col2:
                    st.caption("Matched vs. unmatched side effects:")
                    st.metric(label="Ibuprofen", value="2%", delta=None)
                
                with st.expander("See more details of analysis"):
                    st.write(results_reLookup)
                
                return results_reLookup



if __name__ == "__main__":
    pass
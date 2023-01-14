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
                # Start reverse lookup and get results as dataframe
                df, total_nr_meds_found, med_high_p_name, med_high_p_name2, med_high_p_pct, med_high_p_prop, med_high_p_user, med_high_p_total = callAnalysisBackend.do_reverse_lookup(selected_sideEffects_name, selected_sideEffects_id,nr_sideEffects,combo)
                
                st.markdown("<br>", unsafe_allow_html=True)

                # Display results from reverse lookup as dataframe
                st.subheader("2. Results: Possible medicines taken")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Show metrics
                if combo == "False":
                    col1, col2, col3, col4, col5 = st.columns(5, gap="large")
                    
                    # KPI1
                    with col1:
                        #st.caption("Nr. meds with at least one matched side effect:")
                        st.metric(label="Closest Predicted Medicine taken", value=med_high_p_name, delta=None)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.metric(label="Matched side effects", value=med_high_p_pct, delta=None)
                        
                        
                    # KPI2
                    with col2:
                        #st.caption("Closest Predicted Medicine")
                        st.metric(label="Total nr. potential meds", value=total_nr_meds_found, delta=None)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.metric(label="Matched side effects from all listed side effects",
                                  value=med_high_p_total, delta=None)
                        
                    # KPI3
                    with col3:
                        #st.caption("Highest percentage matched side effects:")
                        #st.metric(label="Matched side effects", value=med_high_p_pct, delta=None)
                        st.metric(label="Probability vs. all other meds", value=med_high_p_prop, delta=None)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.metric(label="User Reports for this medicine", value=med_high_p_user, delta=None)


                    # KPI4
                    #with col4:
                        #st.caption("Probability compared to all possible medicines:")
                        #st.metric(label="Probability vs. all other meds", value=med_high_p_prop, delta=None)
                    
                    # KPI5
                    #with col5:
                        #st.caption("Probability compared to all possible medicines:")
                        #st.metric(label="Matched side effects compared to all listed side effects for this medicine",
                                  #value=med_high_p_total, delta=None)
                
                elif combo == "True":
                    col1, col2, col3, col4 = st.columns(4)
                    
                    # KPI1
                    with col1:
                        pass
                    
                    # KPI2
                    with col2:
                        pass
                    
                    # KPI3
                    with col3:
                        pass

                    # KPI4
                    with col4:
                        pass
                
                # Details of analysis
                with st.expander("See more details of analysis"):
                    st.write(df)
                
                return df

class render_tab3:
    def __init__(self):
        st.info("Analysis of drugs with shared proteins:\n" +
                "Do drugs with shared proteins have common side effects?")
    
    def show_protein_analysis(self):
        """UI for displaying results of shared protein analysis.

        Args:
            selected_sideEffects:
            type: list
            nr_sideEffects:
            type: int
        Returns:
            selected_sideEffects: list of chosen side effects
            type: dataframe
        """
        


        return None


if __name__ == "__main__":
    pass
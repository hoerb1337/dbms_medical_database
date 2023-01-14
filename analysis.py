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
                
                explained_calc = "Information about the prediction"
                st.warning(explained_calc)

                tooltip = """
                        <style>
                        .tooltip {
                        position: relative;
                        display: inline-block;
                        }

                        .tooltip .tooltiptext {
                        visibility: hidden;
                        width: 120px;
                        background-color: #555;
                        color: #fff;
                        text-align: center;
                        border-radius: 6px;
                        padding: 5px 0;
                        position: absolute;
                        z-index: 1;
                        bottom: 125%;
                        left: 50%;
                        margin-left: -60px;
                        opacity: 0;
                        transition: opacity 0.3s;
                        }

                        .tooltip .tooltiptext::after {
                        content: "";
                        position: absolute;
                        top: 100%;
                        left: 50%;
                        margin-left: -5px;
                        border-width: 5px;
                        border-style: solid;
                        border-color: #555 transparent transparent transparent;
                        }

                        .tooltip:hover .tooltiptext {
                        visibility: visible;
                        opacity: 1;
                        }
                        </style>
                        """

                st.markdown(tooltip, unsafe_allow_html=True)
                
                # Show metrics
                if combo == "False":
                    col1, col2, col3 = st.columns(3, gap="large")
                    
                    # KPI1
                    with col1:
                        #st.caption("                                        ")
                        tooltip_kpi1 = """
                        <div class="tooltip">Closest Predicted Medicine <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                        <span class="tooltiptext">Tooltip text</span>
                        </div> 
                         """

                        tooltip_kpi2 = """
                        <div class="tooltip">Total nr. potential meds <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                        <span class="tooltiptext">Tooltip text</span>
                        </div> 
                         """
                        st.markdown(tooltip_kpi1, unsafe_allow_html=True)
                        st.subheader(med_high_p_name)
                        # st.metric(label="Closest Predicted Medicine", value=med_high_p_name, delta=None)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown(tooltip_kpi2, unsafe_allow_html=True)
                        st.subheader(total_nr_meds_found)
                        #st.metric(label="Total nr. potential meds", value=total_nr_meds_found, delta=None, label_visibility="hidden")
                        
                        
                    # KPI2
                    with col2:
                        st.caption("                                        ")
                        st.metric(label="Matched side effects vs. selected", value=med_high_p_pct, delta=None)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.metric(label="Matched side effects from all listed side effects",
                                  value=med_high_p_total, delta=None)
                        
                    # KPI3
                    with col3:
                        st.caption("                                        ")
                        st.metric(label="Probability vs. all other meds", value=med_high_p_prop, delta=None)
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.metric(label="User Reports for this medicine", value=med_high_p_user, delta=None)

                
                elif combo == "True":
                    col1, col2, col3, col4 = st.columns(4, gap="large")
                    
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
# External libraries
import streamlit as st


# Backend modules
import analysisService
#

class render_tab2:
    
    def __init__(self):
        """Display information for tab2."""
        
        info_text = """
                    Perform a Reverse Lookup Analysis:
                    
                    1. Choose whether you are taking medicines in combination.
                    2. Select your own set of felt side effect symptoms from medicines you are taking.
                    3. We find for you the closest prediction of medicine that you could have taken.
                    
                    More details on how we perform the predicition is provided with the results.
                    """
        st.info(info_text)
        st.markdown("<br>", unsafe_allow_html=True)


    def show_selection_sideEffects(self):
        """UI for choosing side effects by user.

        Args:
            None
        Returns:
            selected_sideEffects_name: name of selected side effects w/o id
            type: str items in list
            selected_sideEffects_id: id of side effect
            type: str items in list
            nr_sideEffects: number of selected side effects by user
            type: int
            combo: "True" or "False"
            type: str
            selected_sideEffects: names + id of selected side effects,
            in the form ['<name side effect (id)>', '...', ...]
            type: str items in list
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

        # normalise list of selected side effects:
        # extract ids from side effects description
        selected_sideEffects_name, selected_sideEffects_id = callAnalysisBackend.norm_list_se(selected_sideEffects)

        nr_sideEffects = len(selected_sideEffects_name)
        if nr_sideEffects < 1:
            st.warning("Please choose at least one side effect symptom.")

        return selected_sideEffects_name, selected_sideEffects_id, nr_sideEffects, combo, selected_sideEffects
    
    
    def show_reverse_lookup(self, selected_sideEffects_name,
                            selected_sideEffects_id,
                            nr_sideEffects, combo):
        """UI for displaying reverse lookup results.

        Args:
            selected_sideEffects_name: name of selected side effects w/o id
            type: str items in list
            selected_sideEffects_id: id of side effect
            type: str items in list
            nr_sideEffects: number of selected side effects by user
            type: int
            combo: "True" or "False"
            type: str
        Returns:
            med_high_p_name: commercial name of predicted medicine
            type: str
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
                
                info_box_style = """
                        <style>
                        .info_box {background-color: #000;}
                        </style>
                        """
                explained_calc = """
                                <div class="info_box">
                                <b>Information about the procedure of prediction:</b><br>
                                <br>
                                In general, the analysis follows a multiple-stage/criteria approach
                                to make the prediction:<br>
                                <ol>
                                <li>
                                Calculate, for each medicine registered in the database,
                                how many of selected side effects match all listed side effects for the medicine.
                                Only the medicines with at least one matched side effect are further considered.
                                </li>
                                <li>
                                
                                the more selected side effects
                                match the
                                </li>
                                </ol>
                                </div>
                                """
                
                st.markdown(explained_calc, unsafe_allow_html=True)

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
                col1, col2, col3 = st.columns(3, gap="large")
                    
                # KPI1
                with col1:
                    tooltip_kpi1 = """
                                    <div class="tooltip">Closest Predicted Medicine 1 <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">Tooltip text</span>
                                    </div> 
                                    """

                    st.markdown(tooltip_kpi1, unsafe_allow_html=True)
                    st.subheader(med_high_p_name)
                    
                    if combo == "True":
                        tooltip_kpi1_1 = """
                                        <div class="tooltip">Closest Predicted Medicine 2 <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                        <span class="tooltiptext">Tooltip text</span>
                                        </div> 
                                        """

                        st.markdown(tooltip_kpi1_1, unsafe_allow_html=True)
                        st.subheader(med_high_p_name2)
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    tooltip_kpi2 = """
                                    <div class="tooltip">Total # potential meds <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">Tooltip text</span>
                                    </div> 
                                    """
                    st.markdown(tooltip_kpi2, unsafe_allow_html=True)
                    st.subheader(total_nr_meds_found)
                        
                        
                # KPI2
                with col2:
                        
                    tooltip_kpi3 = """
                                    <div class="tooltip">Matched slected side effects
                                    <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">Tooltip text</span>
                                    </div> 
                                    """

                    st.markdown(tooltip_kpi3, unsafe_allow_html=True)
                    st.subheader(med_high_p_pct)
                        
                    st.markdown("<br>", unsafe_allow_html=True)

                    tooltip_kpi4 = """
                                    <div class="tooltip">Matched side effects vs. all side effects
                                    <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">Tooltip text</span>
                                    </div> 
                                    """
                    st.markdown(tooltip_kpi4, unsafe_allow_html=True)
                    st.subheader(med_high_p_total)
                        
                # KPI3
                with col3:

                    tooltip_kpi5 = """
                                    <div class="tooltip">Probability compared to all other meds <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">Tooltip text</span>
                                    </div> 
                                    """

                    st.markdown(tooltip_kpi5, unsafe_allow_html=True)
                    st.subheader(med_high_p_prop)
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    tooltip_kpi6 = """
                                    <div class="tooltip">User Reports for this medicine <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">Tooltip text</span>
                                    </div> 
                                    """
                    st.markdown(tooltip_kpi6, unsafe_allow_html=True)
                    st.subheader(med_high_p_user)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Details of analysis
                with st.expander("See full table with all data from all medicines with at least one matched side effect"):
                    st.write(df)
                
                return med_high_p_name


if __name__ == "__main__":
    pass
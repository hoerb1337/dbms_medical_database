# External libraries
import streamlit as st


# Backend modules
import analysisService
#

class render_tab2:
    
    def __init__(self):
        """Display information for tab2."""

        info_box_tab2 = """
                    <div class="info_box">
                    <h5>Perform Reverse Lookup Analysis:</h5>
                    <p>In general, the analysis follows a multiple-stage/criteria approach
                    to make the prediction:</p>
                    <ol>
                    <li>Choose whether you are taking medicines in combination.</li>
                    <li>Select your own set of felt side effect symptoms from medicines you are taking.</li>
                    <li>We find for you the closest prediction of medicines that you could have taken.</li>
                    </ol>
                    <p>More details on how we perform the predicition is provided with the results.</p>
                    <p>Hint: Since the number of side effects per medicine is high (>100),
                    the prediction becomes naturally more precise with higher number of selected side effects.</p>
                    </div>
                    """
                    
        st.markdown(info_box_tab2, unsafe_allow_html=True)


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

        # Normalise list of selected side effects:
        # extract ids from side effects description
        selected_sideEffects_name, selected_sideEffects_id = callAnalysisBackend.norm_list_se(selected_sideEffects)

        nr_sideEffects = len(selected_sideEffects_name)
        if nr_sideEffects < 1:
            st.warning("Please choose at least one side effect symptom.")

        if combo == "True":
                st.warning("Notice: The processesing of reverse lookup may take few moments given the large amount of data.")

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
                df, total_nr_meds_found, med_high_p_name, med_high_p_name2, med_high_p_pct, med_high_p_prop, med_high_p_user, med_high_p_total, med_high_p_name_2, med_high_p_name2_2, med_high_p_pct_2, med_high_p_prop_2, med_high_p_user_2, med_high_p_total_2 = callAnalysisBackend.do_reverse_lookup(selected_sideEffects_name, selected_sideEffects_id,nr_sideEffects,combo)
                
                st.markdown("<br>", unsafe_allow_html=True)

                # Display results from reverse lookup as dataframe
                st.subheader("2. Results: Possible medicines taken")
                
                # Show metrics
                col1, col2, col3 = st.columns(3, gap="large")
                    
                # KPI1
                with col1:
                    tooltip_kpi1 = """
                                    <div class="tooltip"> Closest Predicted Medicine (1) <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">
                                    You can find more details to the prediction
                                    within the expanders further down. 
                                    </span>
                                    </div> 
                                    """
                    
                    st.markdown(tooltip_kpi1, unsafe_allow_html=True)
                    st.subheader(med_high_p_name)
                    st.write(med_high_p_name_2)
                    
                    if combo == "True":
                        tooltip_kpi1_1 = """
                                        <div class="tooltip">Closest Predicted Medicine (2) <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                        <span class="tooltiptext">
                                        You can find more details to the prediction
                                        within the expanders further down.
                                        </span>
                                        </div> 
                                        """

                        st.markdown(tooltip_kpi1_1, unsafe_allow_html=True)
                        st.subheader(med_high_p_name2)
                        st.write(med_high_p_name2_2)
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    tooltip_kpi2 = """
                                    <div class="tooltip">Total number of potential meds <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">
                                    All medicines with at least one matched side effect.
                                    </span>
                                    </div> 
                                    """
                    st.markdown(tooltip_kpi2, unsafe_allow_html=True)
                    st.subheader(total_nr_meds_found)
                        
                        
                # KPI2
                with col2:
                        
                    tooltip_kpi3 = """
                                    <div class="tooltip">Matched selected side effects
                                    <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">
                                    Matched selected side effects compared
                                    to number of selected side effects.
                                    </span>
                                    </div> 
                                    """

                    st.markdown(tooltip_kpi3, unsafe_allow_html=True)
                    st.subheader(med_high_p_pct)
                    st.write(med_high_p_pct_2)
                        
                    st.markdown("<br>", unsafe_allow_html=True)

                    tooltip_kpi4 = """
                                    <div class="tooltip">Matched side effects vs. all side effects
                                    <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">
                                    Matched selected side effects compared
                                    to the total number of side effects registered
                                    in database for the medicine.
                                    </span>
                                    </div> 
                                    """
                    st.markdown(tooltip_kpi4, unsafe_allow_html=True)
                    st.subheader(med_high_p_total)
                    st.write(med_high_p_total_2)
                        
                # KPI3
                with col3:

                    tooltip_kpi5 = """
                                    <div class="tooltip">Probability compared to all other meds <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">
                                    Probability compared to all other medicines with at
                                    least one matched side effect.
                                    </span>
                                    </div> 
                                    """

                    st.markdown(tooltip_kpi5, unsafe_allow_html=True)
                    st.subheader(med_high_p_prop)
                    st.write(med_high_p_prop_2)
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    tooltip_kpi6 = """
                                    <div class="tooltip">User Reports for this medicine <img src="https://static.vecteezy.com/system/resources/previews/000/442/530/original/information-vector-icon.jpg" width="15px" height="15px">
                                    <span class="tooltiptext">
                                    Popularity of the medicine based on proportion of resports for a medicine by users (tab1).
                                    </span>
                                    </div> 
                                    """
                    st.markdown(tooltip_kpi6, unsafe_allow_html=True)
                    st.subheader(med_high_p_user)
                    st.write(med_high_p_user_2)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Explaination of predection
                with st.expander("Explaination for the prediction"):
                    explained_calc = """
                                    <div class="expander">
                                    <h5>Information about the procedure of prediction:</h5>
                                    In general, the analysis follows a multiple-stage/criteria approach
                                    to make the prediction:<br>
                                    <ol>
                                    <li>
                                    Calculate, for each medicine registered in the database,
                                    how many of selected side effects match all listed side
                                    effects for the medicine. Only the medicines with at least
                                    one matched side effect are further considered.
                                    Medicine with highest proportion is selected.
                                    </li>
                                    <li>
                                    If there are multiple medicines with highest proportion of 
                                    matched side effects, the next criterium is the popularity
                                    of reported side effects by users (tab1).
                                    </li>
                                    <li>
                                    If there are any reports for the medicines yet, the next criterium
                                    is the proportion of the number of matched side effects for each medicine
                                    to the total number of listed side effects for the medicine.<br><br>
                                    </li>
                                    </ol>
                                    Additional information on each criteria is
                                    provided by clicking on the information symbol.
                                    </div>
                                    """
                    
                    st.markdown(explained_calc, unsafe_allow_html=True)

                # Full table
                with st.expander("See full table with all data from all medicines with at least one matched side effect"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.write(df)
                    st.markdown("<br>", unsafe_allow_html=True)
                
                return med_high_p_name


if __name__ == "__main__":
    pass
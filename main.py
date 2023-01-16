# External libraries
import streamlit as st

# Frontend modules
import sideEffects
import analysis
import user
import protein

# Backend sevices
import userService

class Frontend:
    
    def __init__(self):
        st.set_page_config(layout="wide")

        # Hide burger menu
        hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
        st.markdown(hide_menu_style, unsafe_allow_html=True)
        
        # Webapp title
        st.title("Welcome to the Medical Database")
        
        # User management:
        userAuthenticated = user.UserUI()
        
        # Check if user logged-in is already in database.
        # If not, register the user in database. Get user data
        # to save their access history.
        userData = userAuthenticated.authenticate()

        # Navigation bar
        tab1, tab2, tab3, tab4 = st.tabs(["Lookup and Report Side Effects", 
                                    "Reverse Lookup Analysis",
                                    "Shared Protein Analysis",
                                    "Your Usage Data"])
        #
        
        # Tab1: sideEffects
        with tab1:
            tab1_rendered = sideEffects.render_tab1()
            
            # Return list of selected medicines
            selected_meds, combo, nr_selected_meds = tab1_rendered.selection()
            
            # Start search for side effects
            if combo != None:
                # Show dataframe/side effects
                tab1_rendered.lookup_sideEffects(nr_selected_meds,
                                                selected_meds, combo)
                    
            # Reporting side effects:
            if nr_selected_meds >=1 and nr_selected_meds <=2:
                # list of selected own side effects/multi select UI 
                medicine1_side_effects, medicine2_side_effects = tab1_rendered.select_own_side_effects(combo,
                                                                                                       nr_selected_meds,
                                                                                                       selected_meds)

                # Reporting Button
                if st.button(label="Report side effects", key="reporting"):
                    # Post own side effects to database
                    tab1_rendered.report_side_effects(combo, nr_selected_meds,
                                                      selected_meds, medicine1_side_effects,
                                                      medicine2_side_effects, userData["id"])
                    
                    # Store usage data from user in database
                    store_usage_date = userService.UsageData()
                    store_usage_date.post_usage_data_se(userData["id"], selected_meds, combo,
                                                        medicine1_side_effects, medicine2_side_effects)
                    
                    # Process reporting in frontend
                    session_sate = st.session_state.keys()
                    tab1_rendered.process_reporting(session_sate)
        # End of tab1

        # Tab2: reverse lookup analysis
        with tab2:
            tab2_rendered = analysis.render_tab2()

            # 1. Selection side effects
            selected_sideEffects_name,selected_sideEffects_id, nr_sideEffects, combo, selected_sideEffects = tab2_rendered.show_selection_sideEffects()
            # 2. perform reverse lookup and display results
            predicted_med = tab2_rendered.show_reverse_lookup(selected_sideEffects_name,
                                              selected_sideEffects_id,
                                              nr_sideEffects, combo)    
            #st.write(predicted_med)
            # Store usage data from user in database
            if predicted_med != None:
                store_usage_data = userService.UsageData()
                store_usage_data.post_usage_data_reLookup(userData["id"], selected_sideEffects, 
                                                        predicted_med, combo)
        # End of tab2

        # Tab3: shared protein analysis
        with tab3:
            tab3_rendered = protein.render_tab3()
            analysis_executed = tab3_rendered.show_protein_analysis()
            if analysis_executed != None:
                store_usage_data = userService.UsageData()
                analysis_executed = "Execute Analysis"
                store_usage_data.post_usage_data_protein(userData["id"], analysis_executed)
            
            st.markdown("<br>", unsafe_allow_html=True) 
            
            analysis_details_executed = tab3_rendered.show_protein_analysis_details()
            #st.write(analysis_executed)
            #st.write(analysis_details_executed)
            if analysis_details_executed != None:
                store_usage_data = userService.UsageData()
                analysis_details_executed = "Execute Query"
                store_usage_data.post_usage_data_protein(userData["id"], analysis_details_executed)
        # End of tab3

        # Tab4: usage data
        with tab4:
            tab4_rendered = user.render_tab4()
            tab4_rendered.show_accessHistory_tab1()
            tab4_rendered.show_accessHistory_tab2()
            tab4_rendered.show_accessHistory_tab3()
            #st.header("Access history")
        # End of tab4


if __name__ == "__main__":
    rendered_frondend = Frontend()
    
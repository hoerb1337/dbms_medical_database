# External libraries
import streamlit as st

# Frontend modules
import sideEffects
import analysis
import user

# Backend sevices
import userService

class Frontend:
    
    def __init__(self):
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
        tab1, tab2, tab3 = st.tabs(["Medicine Side Effects", 
                                    "Analysis Module",
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
                    store_usage_date = userService.UserManagament()
                    store_usage_date.post_usage_date(userData["id"], selected_meds, combo,
                                                    medicine1_side_effects, medicine2_side_effects)
                    
                    # Process reporting in frontend
                    session_sate = st.session_state.keys()
                    tab1_rendered.process_reporting(session_sate)
        # End of tab1

        # Tab2: analysis
        with tab2:
            tab2_rendered = analysis.render_tab2()
            
            # Reverse Lookup
            tab1 = tab2_rendered.tab1
            with tab1:
                # 1. Selection side effects
                selected_sideEffects_name,selected_sideEffects_id, nr_sideEffects, combo = tab2_rendered.show_selection_sideEffects()
                # 2. perform reverse lookup and siplay results
                tab2_rendered.show_reverse_lookup(selected_sideEffects_name,
                                                selected_sideEffects_id,
                                                nr_sideEffects, combo)
            
            # Analysis of drugs with shared proteins
            tab2 = tab2_rendered.tab2
            with tab2:
                tab2_rendered.show_protein_analysis()

        #

        # Tab3: user
        with tab3:
            #self.tab3_rendered = user.render_tab3()
            st.header("Access history")
        #


if __name__ == "__main__":
    rendered_frondend = Frontend()
    
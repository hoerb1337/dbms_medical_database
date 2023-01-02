# External libraries
import streamlit as st
# import psycopg2

# Frontend modules
import sideEffects
#import analysis
#import user
#

class Layout:
    
    def __init__(self):
        
        # Hide burger menu
        hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
        st.markdown(hide_menu_style, unsafe_allow_html=True)
        
        # Webapp title
        st.title("Medical Database")
        
        # Navigation bar
        tab1, tab2, tab3 = st.tabs(["Medicine Side Effects", 
                                    "Analysis",
                                    "Your Access History"])
        #

        # Tab1: sideEffects
        with tab1:
            tab1_rendered = sideEffects.render_tab1()
            
            # Return list of selected medicines
            selected_meds, combo, nr_selected_meds = tab1_rendered.selection()

            # Start search for side effects
            if combo != None:
                if st.button(label="Lookup side effects"):
                    
                    # Show dataframe
                    df = tab1_rendered.display_sideEffects(nr_selected_meds, selected_meds, combo)
                    
            # Reporting side effects
            if df != None:
                if st.button(label="Continue for reporting own side effects"):
                    
                    # list of selected own side effects 
                    medicine1_side_effects, medicine2_side_effects = tab1_rendered.select_own_side_effects(combo, nr_selected_meds, selected_meds)

                    # Post own side effects to database
                    if st.button(label="Report side effects"):
                        tab1_rendered.report_side_effects(combo, nr_selected_meds, selected_meds, medicine1_side_effects, medicine2_side_effects)

                    
        #

        # Tab2: analysis
        with tab2:
            #self.tab2_rendered = analysis.render_tab2()
            st.header("Analysis")
        #

        # Tab3: user
        with tab3:
            #self.tab3_rendered = user.render_tab3()
            st.header("Access history")
        #


if __name__ == "__main__":
    rendered_layout = Layout()
    
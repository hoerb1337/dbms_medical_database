# External libraries
import streamlit as st
import webbrowser  
from streamlit_autorefresh import st_autorefresh
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
            
            #st.write(st.session_state)
            # Start search for side effects
            if combo != None:
                #if st.button(label="Lookup side effects", key="lookup"):
                    
                # Show dataframe/side effects
                displayed_side_effects = tab1_rendered.lookup_sideEffects(nr_selected_meds, selected_meds, combo)
                    
            # Reporting side effects
            
            #st.write(nr_selected_meds)
            #st.write(selected_meds)
            #st.write(combo)          
            if nr_selected_meds >=1 and nr_selected_meds <=2:
            # list of selected own side effects/multi select UI 
                medicine1_side_effects, medicine2_side_effects = tab1_rendered.select_own_side_effects(combo, nr_selected_meds, selected_meds)
            #st.write(medicine1_side_effects)
            #st.write(medicine2_side_effects)
            # Post own side effects to database
                if st.button(label="Report side effects", key="cont_reporting"):
                    tab1_rendered.report_side_effects(combo, nr_selected_meds, selected_meds, medicine1_side_effects, medicine2_side_effects)
                    
                    
                    #st.write("Click here to [continue](https://hoerb1337-dbms-medical-database-main-dev-93dds9.streamlit.app/)")
                    
                    #if st.button(label="Continue"):
                        #del st.session_state["medicines_selected"]
                    for key in st.session_state.keys():
                        del st.session_state[key]
                        #st.write(st.session_state)
                    
                    st.success("Thank you! Your provided side effects have been successfully reported.")

                    n = 1000
                    while n >= 0:
                        n = n-1
                    st.experimental_rerun()
                    #st_autorefresh(interval=1000, limit=2, key="fizzbuzzcounter")
                        #st_autorefresh(interval=1000, limit=2, key="fizzbuzzcounter")
                    
                    
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
    
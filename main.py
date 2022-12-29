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
        st.header("Medical Database")
        
        # Navigation bar
        tab1, tab2, tab3 = st.tabs(["Medicine Side Effects", 
                                    "Analysis",
                                    "Your Access History"])
        #

        # Tab1: sideEffects
        with tab1:
            self.tab1_rendered = sideEffects.render_tab1()
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
    
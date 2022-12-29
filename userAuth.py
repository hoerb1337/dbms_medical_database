# external libraries
import streamlit as st
import psycopg2

# frontend modules
import main

# backend modules
import userService


# Layout
st.title("Welcome to the Medical Database!")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Registration", "Login"])
#

# User registration
with tab1:
        st.header("Register your email address")
        # Text:
        # "Please provide your email address for using our service.
        #  It allows you to track your history of usage"
        # < Insert Input field1 for email address > 
        # < Insert Input field1 for email address >
        # < Insert button for activation/confirmation >:
                # < Call register_user = userService.registration()>:
                        # If check on consistency successfull:
                                # If email not yet in DB: 
                                                # Open main.py
                                        # Else:
                                                # Error message: email already registered. Please use Login tab
                        # Else:
                                # Error message: email addresses not consistend. Please fix email addresses
#

# User registration
with tab2:
        st.header("Login with your email address")
        # Text:
        # "Please provide your registered email address for using our service.
        # < Insert Input field for email address > 
        # < Insert button for activation/confirmation >:
                # < Call login_user = userService.registration()>:
                # < Check on availability of email in DB>
                # If check on consistency successfull:
                        # < Call register_user = userService.registration()>:
                                # If email not yet in DB: 
                                        # Open main.py
                                # Else:
                                        # Error message: email already registered. Please use Login tab
                # Else:
                        # Error message: email addresses not consistend. Please fix email addresses
#
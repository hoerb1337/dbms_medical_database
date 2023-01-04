# External libraries
import streamlit as st


# Backend modules
import userService
#

class UserUI:
    
    def __init__(self):
        st.write("hello1")

    def authenticate(self):
        user = userService.UserManagament()
    
        return user.get_user_auth()

    def accessHistory(self):
        pass

if __name__ == "__main__":
    pass
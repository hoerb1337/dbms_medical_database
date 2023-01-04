# External libraries
import streamlit as st


# Backend modules
import userService
#

class UserUI:
    
    def __init__(self):
        pass

    def authenticate(self):
        user = userService.UserManagament.get_user_auth()

    def accessHistory(self):
        pass

if __name__ == "__main__":
    pass
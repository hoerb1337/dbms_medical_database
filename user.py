# External libraries
import streamlit as st
import json


# Backend modules
import userService
#

class UserUI:
    
    def __init__(self):
        pass

    def authenticate(self):
        user = userService.UserManagament()
        
        # User data as JSON
        userData = user.get_user_auth()
        st.write(type(userData))
        # check if user is already in database
        # user is in db
        if user.get_user_status_db(userData["id"]) == 200:
            user.edit_user(userData)
    
        # user not yet in db
        elif user.get_user_status_db(userData["id"]) == 400:
            user.post_user(userData)

        return userData

    def accessHistory(self):
        pass

if __name__ == "__main__":
    pass
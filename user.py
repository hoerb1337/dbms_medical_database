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
        st.write(userData)
        st.write(userData["id"])
        # check if user is already in database
        # user is in db
        user_checked = user.get_user_status_db(userData["id"])
        if user_checked == 200:
            user.edit_user(userData)
    
        # user not yet in db
        elif user_checked == 400:
            user.post_user(userData)

        return userData

    def accessHistory(self):
        pass

if __name__ == "__main__":
    pass
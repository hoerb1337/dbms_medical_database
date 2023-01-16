# External libraries
import streamlit as st


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

        # check if user is already in database
        # user is in db
        if userData != "Error":
            user_checked = user.get_user_status_db(userData["id"])

            if user_checked == 200:
                user.edit_user(userData)
        
            # user not yet in db
            elif user_checked == 400:
                user.post_user(userData)

        return userData

class render_tab4:
    def __init__(self):
        st.info("Access history")
    
    def accessHistory_tab1(self):
        pass

    def accessHistory_tab2(self):
        pass

    def accessHistory_tab3(self):
        pass

if __name__ == "__main__":
    pass
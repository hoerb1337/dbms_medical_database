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
    
    def show_user(self, userID):
        
        get_user = userService.UserManagament()
        email, last_act = get_user.get_user_data_db(userID)
        
        welcome_msg = "Welcome " + email + "! Your last acivity was on: " + last_act + "."
        
        st.write(welcome_msg)

        return email, last_act

    def show_accessHistory_tab1(self, userID):
        with st.expander("Usage data for lookup and reporting side effects"):
            get_usage_data = userService.UsageData()
            df = get_usage_data.get_usage_data_se(userID)
            st.write(df)
        
        return df
 
    def show_accessHistory_tab2(self, userID):
        with st.expander("Usage data for reverse lookup analysis"):
            get_usage_data = userService.UsageData()
            df = get_usage_data.get_usage_data_relookup(userID)
            st.write(df)
        
        return df

    def show_accessHistory_tab3(self, userID):
        with st.expander("Usage data for protein analysis"):
            get_usage_data = userService.UsageData()
            df = get_usage_data.get_usage_data_protein(userID)
            st.write(df)
        
        return df

if __name__ == "__main__":
    pass
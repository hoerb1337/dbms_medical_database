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
    """UI elements for tab4: Your Usage Data"""
    def __init__(self, userID):

        get_user = userService.UserManagament()
        email, last_act = get_user.get_user_data_db(userID)
        
        last_act_1 = str(int(last_act[-9:-6:])+1)
        st.write(last_act1)
        last_act1 = last_act[0:10:] + last_act_1 + last_act[-7::]
        st.write(last_act1)

        info_box_tab4 = "<div class='info_box'><h5>Your Usage data:</h5><p>Welcome " + email + "! Your last acivity was on: " + last_act + ".</p><p>Browse for the history of all your actions on the Medical Database.</p></div>"
                    
        st.markdown(info_box_tab4, unsafe_allow_html=True)


    def show_accessHistory_tab1(self, userID):
        """UI for access history tab1 within an expander.

        Args:
            userID: id from user
            type: int
        Returns:
            df: table for usage data for tab1
            type: dataframe
            len: nr. of entries in table 
            type: int
        """

        with st.expander("Usage data for lookup and reporting side effects"):
            get_usage_data = userService.UsageData()
            df, len = get_usage_data.get_usage_data_se(userID)
            if len > 0:
                st.write(df)
            else:
                st.write("Any activity registered yet.")
        
        return df, len
 
    def show_accessHistory_tab2(self, userID):
        """UI for access history tab2 within an expander.

        Args:
            userID: id from user
            type: int
        Returns:
            df: table for usage data for tab2
            type: dataframe
            len: nr. of entries in table 
            type: int
        """

        with st.expander("Usage data for reverse lookup analysis"):
            get_usage_data = userService.UsageData()
            df, len = get_usage_data.get_usage_data_relookup(userID)
            if len > 0:
                st.write(df)
            else:
                st.write("Any activity registered yet.")
        
        return df, len

    def show_accessHistory_tab3(self, userID):
        """UI for access history tab3 within an expander.

        Args:
            userID: id from user
            type: int
        Returns:
            df: table for usage data for tab3
            type: dataframe
            len: nr. of entries in table 
            type: int
        """

        with st.expander("Usage data for protein analysis"):
            get_usage_data = userService.UsageData()
            df, len = get_usage_data.get_usage_data_protein(userID)
            if len > 0:
                st.write(df)
            else:
                st.write("Any activity registered yet.")
        
        return df, len

if __name__ == "__main__":
    pass
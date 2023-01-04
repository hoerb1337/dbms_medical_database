import streamlit as st
import requests

# Backend services
import database

class UserManagament:
    def __init__(self):
        pass

    def get_user_auth(self):
        """Get user data from service provider (SP)

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """

        # Get token from SP
        params = st.experimental_get_query_params()
        token = params.get("token")
        if token:
            token = token[0]

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("https://api.dashboardauth.com/get-user",
                                headers=headers)
        
        if response.status_code == 200:
            st.write(response.json())
            return response.json()
        else:
            st.write("Invalid token")
            return 400


    def get_user_db(self):
        pass
        # Open db connection
        #db = database.db_connection()
        #db_connection, db_cur = db.connect_postgres()
        #db_cur.execute("SELECT commercial_name FROM dbms.medicines;")
    
    def post_user(self):
        pass

    def edit_user(self):
        pass



if __name__ == "__main__":
    pass
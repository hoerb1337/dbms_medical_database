import streamlit as st
import requests

# Backend services
import database

class UserManagament:
    def __init__(self):
        pass

    def get_user_auth(self):
        """Get user data from login service provider (SP).

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
            #st.write(f"token {token}")
        else:
            token = "Error"
            #st.write("No token")

        # Get user data
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            "https://api.dashboardauth.com/get-user", headers=headers,
        )
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code

    def get_user_status_db(self, userID):
        """Check if user already exists in db.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """

        # Open db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        db_cur.execute("""SELECT id FROM dbms.user where id = %(userID)s;""", {'userID': userID})

        list_user = []
        for user_i in db_cur:
            list_user.append(f"{user_i[0]}")

        if len(list_user) == 1:
            status_msg = 200
        elif len(list_user) == 0:
            status_msg = 400

        # Close connection
        db.disconnect_postgres(db_connection, db_cur)

        return status_msg
    
    def get_user_data_db(self):
        pass
        # Open db connection
        #db = database.db_connection()
        #db_connection, db_cur = db.connect_postgres()
        #db_cur.execute("SELECT commercial_name FROM dbms.medicines;")
    
        return 

    def post_user(self, userData):
        """Create new user data in db.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """

        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        db_cur.execute("""insert into dbms.user (id, email, last_active) values (%(id)s, %(email)s, %(last_active)s);""",
                       {'id': userData["id"], 'email': userData["email"], 'last_active': userData["last_active"]})
        
        db_connection.commit()
        
        # Close connection
        db.disconnect_postgres(db_connection, db_cur)
        
        status_msg = 200
        
        return status_msg

    def edit_user(self, userData):
        """Edit user data in db. Right now only last_active is changed.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """

        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        db_cur.execute("""UPDATE dbms.user SET last_active = %(lastActive)s where id = %(userID)s;""",
                      {'lastActive': userData["last_active"], 'userID': userData["id"]})
        
        db_connection.commit()
        
        # Close connection
        db.disconnect_postgres(db_connection, db_cur)
        
        status_msg = 200
        
        return status_msg

    def post_usage_date(self, userData, selected_meds,
                        combo, medicine1_side_effects, 
                        medicine2_side_effects):
        """Edit user data in db. Right now only last_active is changed.

        Args:
            userData: id from user
            type: int
        Returns:
            sum over n:
            type: 
        """
        
        side_effects1_conc = ""
        for side_effect_i in medicine1_side_effects:
            side_effects1_conc = side_effect_i + ", " + side_effects1_conc

        st.write(side_effects1_conc)
        st.write(medicine1_side_effects)
        
        # db connection
        #db = database.db_connection()
        #db_connection, db_cur = db.connect_postgres()
        #db_cur.execute("""UPDATE dbms.user SET last_active = %(lastActive)s where id = %(userID)s;""",
                      #{'lastActive': userData["last_active"], 'userID': userData["id"]})
        
        #db_connection.commit()
        
        # Close connection
        #db.disconnect_postgres(db_connection, db_cur)
        
        status_msg = 200
        
        return status_msg


if __name__ == "__main__":
    pass
import streamlit as st
import requests
import pandas as pd

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
            no_token = "Error"
            #st.write("No token")

        # Get user data
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            "https://api.dashboardauth.com/get-user", headers=headers,
        )
        if response.status_code == 200:
            return response.json()
        else:
            return no_token

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

class UsageData:
    def __init__(self):
        pass

    def post_usage_data_se(self, userData, selected_meds,
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
        
        # Only one med selected
        if len(selected_meds) == 1:
            # more than one side effect
            if len(medicine1_side_effects) > 1:
                # transform list of side effects into concenated string
                side_effects1_conc = ""
                for side_effect_i in medicine1_side_effects:
                    side_effects1_conc = side_effect_i + ", " + side_effects1_conc
            else:
                side_effects1_conc = medicine1_side_effects[0]
            
            # db connection
            db = database.db_connection()
            db_connection, db_cur = db.connect_postgres()
            db_cur.execute("""insert into dbms.user_side_effects_history (user_id, access_date, selected_medicine1, selected_medicine2, combo, reported_side_effect1, reported_side_effect2) values (%(userID)s, now(), %(selected_medicine1)s, 'null', %(combo)s, %(reported_side_effect1)s, 'null');""",
                        {'userID': userData, 'selected_medicine1': selected_meds[0], 'combo': combo, 'reported_side_effect1': side_effects1_conc})

        # Two meds selected
        elif len(selected_meds) == 2:
            if combo == "False":
                # more than one side effect of med1
                if len(medicine1_side_effects) > 1:
                    # transform list of side effects into concenated string
                    side_effects1_conc = ""
                    for side_effect_i in medicine1_side_effects:
                        side_effects1_conc = side_effect_i + ", " + side_effects1_conc
                else:
                    side_effects1_conc = medicine1_side_effects[0]
                
                # more than one side effect of med2
                if len(medicine2_side_effects) > 1:
                    # transform list of side effects into concenated string
                    side_effects2_conc = ""
                    for side_effect_i in medicine2_side_effects:
                        side_effects2_conc = side_effect_i + ", " + side_effects2_conc
                else:
                    side_effects2_conc = medicine2_side_effects[0]
            
                # db connection
                db = database.db_connection()
                db_connection, db_cur = db.connect_postgres()
                db_cur.execute("""insert into dbms.user_side_effects_history (user_id, access_date, selected_medicine1, selected_medicine2, combo, reported_side_effect1, reported_side_effect2) values (%(userID)s, now(), %(selected_medicine1)s, %(selected_medicine2)s, %(combo)s, %(reported_side_effect1)s, %(reported_side_effect2)s);""",
                            {'userID': userData, 'selected_medicine1': selected_meds[0], 'selected_medicine2': selected_meds[1], 'combo': combo, 'reported_side_effect1': side_effects1_conc, 'reported_side_effect2': side_effects2_conc})
            
            elif combo == "True":
                if len(medicine1_side_effects) > 1:
                    # transform list of side effects into concenated string
                    side_effects1_conc = ""
                    for side_effect_i in medicine1_side_effects:
                        side_effects1_conc = side_effect_i + ", " + side_effects1_conc
                else:
                    side_effects1_conc = medicine1_side_effects[0]

                # db connection
                db = database.db_connection()
                db_connection, db_cur = db.connect_postgres()
                db_cur.execute("""insert into dbms.user_side_effects_history (user_id, access_date, selected_medicine1, selected_medicine2, combo, reported_side_effect1, reported_side_effect2) values (%(userID)s, now(), %(selected_medicine1)s, %(selected_medicine2)s, %(combo)s, %(reported_side_effect1)s, 'null');""",
                            {'userID': userData, 'selected_medicine1': selected_meds[0], 'selected_medicine2': selected_meds[1], 'combo': combo, 'reported_side_effect1': side_effects1_conc})

        db_connection.commit()
        
        # Close connection
        db.disconnect_postgres(db_connection, db_cur)
        
        status_msg = 200
        
        return status_msg

    def post_usage_data_reLookup(self, userData,
                                selected_sideEffects, 
                                predicted_med, combo):
        """Edit user data in db. Right now only last_active is changed.

        Args:
            userData: id from user
            type: int
        Returns:
            sum over n:
            type: 
        """
        # db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        if len(selected_sideEffects) > 1:
            # transform list of selected side effects w/ stitch into concenated string
            side_effects1_conc = ""
            for side_effect_i in selected_sideEffects:
                side_effects1_conc = side_effect_i + ", " + side_effects1_conc
        else:
            side_effects1_conc = selected_sideEffects[0]
        
        query = "insert into dbms.user_relookup_history (user_id, access_date, selected_side_effects, predicted_med, combo) values (" + str(userData) + ", now(), '" + side_effects1_conc + "', '" + predicted_med + "', '" + combo + "');"

        db_cur.execute(query)
        
        db_connection.commit()
        
        db.disconnect_postgres(db_connection, db_cur)
        
        status_msg = 200
        
        return status_msg


    def post_usage_data_protein(self, userData,
                                analysis_type_executed):
        """Edit user data in db. Right now only last_active is changed.

        Args:
            userData: id from user
            type: int
        Returns:
            sum over n:
            type: 
        """
        # db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
            
        query = "insert into dbms.user_protein_history (user_id, access_date, analysis_type) values (" + str(userData) + ", now(), '" + analysis_type_executed + "');"

        db_cur.execute(query)
        
        db_connection.commit()
        
        db.disconnect_postgres(db_connection, db_cur)
        
        status_msg = 200
        
        return status_msg

    def get_usage_data_se(self, userData):
        """Edit user data in db. Right now only last_active is changed.

        Args:
            userData: id from user
            type: int
        Returns:
            sum over n:
            type: 
        """
        
        # db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        query = "select useh.access_date, useh.selected_medicine1, useh.selected_medicine2, useh.combo, useh.reported_side_effect1, useh.reported_side_effect2 from dbms.user_side_effects_history useh where user_id = " + str(userData) + ";"

        st.write(query)
        db_cur.execute(query)
        query_result = db_cur.fetchall()
        
        access_date = []
        selected_medicine1 = []
        selected_medicine2 = []
        combo = []
        reported_side_effect1 = []
        reported_side_effect2 = []

        # Fill empty lists with data from query
        for row_i in query_result:
            access_date.append(f"{row_i[0]}")
            selected_medicine1.append(f"{row_i[1]}")
            selected_medicine2.append(f"{row_i[2]}")
            combo.append(f"{row_i[3]}")
            reported_side_effect1.append(f"{row_i[4]}")
            reported_side_effect2.append(f"{row_i[5]}")
        
        # dataframes
        df1_definition_names = {'Access Date': access_date}
        df1 = pd.DataFrame(data=df1_definition_names)
        df2_definition_names = {'Selected Medicine 1': selected_medicine1}
        df2 = pd.DataFrame(data=df2_definition_names)
        df3_definition_names = {'Selected Medicine 2': selected_medicine2}
        df3 = pd.DataFrame(data=df3_definition_names)
        df4_definition_names = {'Medicine Combination': combo}
        df4 = pd.DataFrame(data=df4_definition_names)
        df5_definition_names = {'Reported Side Effects for Med.1': reported_side_effect1}
        df5 = pd.DataFrame(data=df5_definition_names)
        db.disconnect_postgres(db_connection, db_cur)
        df6_definition_names = {'Reported Side Effects for Med.2': reported_side_effect2}
        df6 = pd.DataFrame(data=df6_definition_names)
        
        concat_dfs = pd.concat([df1, df2, df3, df4, df5, df5], ignore_index=False, axis=1)
        
        db.disconnect_postgres(db_connection, db_cur)

        return concat_dfs


    def get_usage_data_relookup(self, userData):
        """Edit user data in db. Right now only last_active is changed.

        Args:
            userData: id from user
            type: int
        Returns:
            sum over n:
            type: 
        """
        
        # db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        query = "select useh.access_date, useh.selected_side_effects, useh.predicted_med, useh.combo from dbms.user_relookup_history useh where user_id = " + str(userData) + ";"

        db_cur.execute(query)
        query_result = db_cur.fetchall()
        
        access_date = []
        selected_side_effects = []
        predicted_med = []
        combo = []

        # Fill empty lists with data from query
        for row_i in query_result:
            access_date.append(f"{row_i[0]}")
            selected_side_effects.append(f"{row_i[1]}")
            predicted_med.append(f"{row_i[2]}")
            combo.append(f"{row_i[3]}")
        
        # dataframes
        df1_definition_names = {'Access Date': access_date}
        df1 = pd.DataFrame(data=df1_definition_names)
        df2_definition_names = {'Selected Side Effects': selected_side_effects}
        df2 = pd.DataFrame(data=df2_definition_names)
        df3_definition_names = {'Predicted Medicine': predicted_med}
        df3 = pd.DataFrame(data=df3_definition_names)
        df4_definition_names = {'Medicine Combination': combo}
        df4 = pd.DataFrame(data=df4_definition_names)
        
        concat_dfs = pd.concat([df1, df2, df3, df4], ignore_index=False, axis=1)
        
        db.disconnect_postgres(db_connection, db_cur)

        return concat_dfs

    def get_usage_data_protein(self, userData):
        """Edit user data in db. Right now only last_active is changed.

        Args:
            userData: id from user
            type: int
        Returns:
            sum over n:
            type: 
        """
        
        # db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        query = "select useh.access_date, useh.analysis_type from dbms.user_protein_history useh where user_id = " + str(userData) + ";"

        db_cur.execute(query)
        query_result = db_cur.fetchall()
        
        access_date = []
        analysis_type = []

        # Fill empty lists with data from query
        for row_i in query_result:
            access_date.append(f"{row_i[0]}")
            analysis_type.append(f"{row_i[1]}")
        
        # dataframes
        df1_definition_names = {'Access Date': access_date}
        df1 = pd.DataFrame(data=df1_definition_names)
        df2_definition_names = {'Type of Execution': analysis_type}
        df2 = pd.DataFrame(data=df2_definition_names)
        
        concat_dfs = pd.concat([df1, df2], ignore_index=False, axis=1)
        
        db.disconnect_postgres(db_connection, db_cur)

        return concat_dfs

if __name__ == "__main__":
    pass
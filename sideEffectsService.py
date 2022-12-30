import streamlit as st
import psycopg2
import pandas as pd

# Backend service
import database

class data4SideEffects:
    def __init__(self):
        pass

    def list_medicines(self):
        # Open connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        db_cur.execute("SELECT commercial_name FROM dbms.medicines;")
        list_medicines = []
        for medicine_i in db_cur:
            list_medicines.append(f"{medicine_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_medicines
        
    def max_nr_medicines(self, selected_medicines):
        if len(selected_medicines) > 2:
            nr_meds = 401
        elif len(selected_medicines) == 0:
            nr_meds = 422
        else:
            nr_meds = 200
        
        return nr_meds, len(selected_medicines)

    def get_listSideEffects(self, selected_meds):
        # Open db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        # Exec query 
        db_cur.execute("""select individual_side_effect_name from dbms.medicines m0, dbms.medicine_mono m1 where m0.stitch = m1.stitch and m0.commercial_name = %(medname)s;""", {'medname': selected_meds})
        list_meds1_sideEffects = []
        for sideEffect_i in db_cur:
            list_meds1_sideEffects.append(f"{sideEffect_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_meds1_sideEffects
    
    def create_DataFrame(self, selected_meds, listSideEffects):
        df_definition = {'Side effects from ' + selected_meds: listSideEffects}
        df = pd.DataFrame(data=df_definition)
        
        return df
    

    def get_listSideEffects_combo(self, selected_meds):
        # Open db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        # Exec query 
        db_cur.execute("""select mc.combo_side_effect_name from dbms.medicines_combo mc, dbms.medicines m0, dbms.medicines m1 where mc.stitch1 = m0.stitch and mc.stitch2 = m1.stitch and ((m0.commercial_name = %(medname1)s and m1.commercial_name= %(medname2)s) or (m0.commercial_name = %(medname2)s and m1.commercial_name= %(medname1)s));""", {'medname1': selected_meds[0], 'medname2': selected_meds[1]})
        list_meds1_sideEffects = []
        for sideEffect_i in db_cur:
            list_meds1_sideEffects.append(f"{sideEffect_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_meds1_sideEffects

    def create_DataFrame_combo(self, selected_meds, listSideEffects):
        df_definition = {'Side effects from ' + selected_meds[0] + 'and ' + selected_meds[1]: listSideEffects}
        df = pd.DataFrame(data=df_definition)
        
        return df
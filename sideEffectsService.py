import streamlit as st
import psycopg2

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
        
        return nr_meds

    def get_listSideEffects(self, selected_meds1, selected_meds2):
        # Open db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        # Exec query1 
        db_cur.execute("""select individual_side_effect_name from dbms.medicines m0, dbms.medicine_mono m1 where m0.stitch = m1.stitch and m0.commercial_name = %(medname)s;""", {'medname': selected_meds1})
        list_meds1_sideEffects = []
        for sideEffect_i in db_cur:
            list_meds1_sideEffects.append(f"{sideEffect_i[0]}")
        
        # Exec query2 
        db_cur.execute("select individual_side_effect_name from dbms.medicines m0, dbms.medicine_mono m1 where m0.stitch = m1.stitch and m0.commercial_name = 'dasatinib';")
        list_meds2_sideEffects = []
        for sideEffect_i in db_cur:
            list_meds2_sideEffects.append(f"{sideEffect_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_meds1_sideEffects, list_meds2_sideEffects
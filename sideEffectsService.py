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
        df_definition = {'Side effects from the combination of ' + selected_meds[0] + ' and ' + selected_meds[1]: listSideEffects}
        df = pd.DataFrame(data=df_definition)
        
        return df

# Reporting from here:
    def list_side_effects_mono(self, selected_meds):
        """Get list of side effects from mono medicines in the database.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """

        # Open connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        db_cur.execute("""select mm.individual_side_effect_name from dbms.medicines m0, dbms.medicine_mono mm where m0.stitch = mm.stitch and m0.commercial_name = %(medname)s;""", {'medname': selected_meds})
        list_side_effects_mono = []
        for side_effect_i in db_cur:
            list_side_effects_mono.append(f"{side_effect_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_side_effects_mono

    def list_side_effects_combo(self, selected_meds):
        """Get list of side effects from combo medicines in the database.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """

        # Open connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        db_cur.execute("""select mc.combo_side_effect_name from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2 and m0.commercial_name = %(medname1)s and m1.commercial_name = %(medname2)s;""", {'medname1': selected_meds[0], 'medname2': selected_meds[1]})
        list_side_effects_combo = []
        for side_effect_i in db_cur:
            list_side_effects_combo.append(f"{side_effect_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_side_effects_combo

    
    def report_side_effects_mono(self, nr_selected_meds,
                                selected_meds,
                                medicine1_side_effects,
                                medicine2_side_effects):
        """Report own side effects from mono medicines to the database.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """

        # Open connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        
        if nr_selected_meds == 2:
            for side_effect_i in medicine1_side_effects:
                # Exec query 
                db_cur.execute("""INSERT INTO dbms.mono_side_effects_reported(commercial_name, reported_by, reporting_date, individual_side_effect_name) VALUES (%(medname1)s, 100, now(), %(medicine1_side_effects)s);""", {'medname1': selected_meds[0], 'medicine1_side_effects': side_effect_i})

            for side_effect_j in medicine2_side_effects:
                db_cur.execute("""INSERT INTO dbms.mono_side_effects_reported(commercial_name, reported_by, reporting_date, individual_side_effect_name) VALUES (%(medname2)s, 100, now(), %(medicine2_side_effects)s);""", {'medname2': selected_meds[1], 'medicine2_side_effects': side_effect_j})

            db_connection.commit()

        elif nr_selected_meds == 1:
            st.write("test")
            #db = database.db_connection()
            #db_connection, db_cur = db.connect_postgres()
            #db_cur.execute("""INSERT INTO dbms.mono_side_effects_reported(commercial_name, reported_by, reporting_date, individual_side_effect_name) VALUES (%(medname1)s, %(reported_by)s, %(date)s, %(medicine1_side_effects)s);""", {'medname1': 'adfddsdsf', 'reported_by': '99', 'date': '2002-02-02', 'medicine1_side_effects': 'test'})
            #db_connection.commit()
            #db_cur.execute("""INSERT INTO dbms.mono_side_effects_reported (commercial_name, reported_by, reporting_date, individual_side_effect_name) VALUES (%s, %s, %s, %s);""", ('commercial_name1', 100, '2002-02-02', 'individual_side_effect_name'))
            for side_effect_i in medicine1_side_effects:
                # Exec query 
                #st.write(side_effect_i)
                #db = database.db_connection()
                #db_connection, db_cur = db.connect_postgres()
                db_cur.execute("""INSERT INTO dbms.mono_side_effects_reported(commercial_name, reported_by, reporting_date, individual_side_effect_name) VALUES (%(medname1)s, 100, now(), %(medicine1_side_effects)s);""", {'medname1': selected_meds[0], 'medicine1_side_effects': side_effect_i})
                db_connection.commit()
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        status_msg = 200

        return status_msg

    
    def report_side_effects_combo(self, selected_meds,
                                  side_effects_combo):
        """Report own side effects from combo medicines to the database.

        Args:
            n: 
            type: 
        Returns:
            sum over n:
            type: 
        """

        # Open connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        
        for side_effect_i in side_effects_combo:
            # Exec query 
            db_cur.execute("""INSERT INTO dbms.combo_side_effects_reported(commercial_name1, commercial_name2, reported_by, reporting_date, combo_side_effect_name) VALUES (%(medname1)s, %(medname2)s, 100, now(), %(combo_side_effects)s);""", {'medname1': selected_meds[0], 'medname2': selected_meds[1], 'combo_side_effects': side_effect_i})
        
        db_connection.commit()
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        status_msg = 200

        return status_msg


if __name__ == "__main__":
    pass
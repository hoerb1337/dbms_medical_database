import streamlit as st
import psycopg2
import pandas as pd

# Backend service
import database

class data4SideEffects:
    """Provides all necessary methods to obtain data
    for the UI of tab1.
    """

    def __init__(self):
        pass

    def list_medicines(self):
        """Provides all medicines registered in database.
        
        Used as list for selection of medicines.

        Args:
            none 
        Returns:
            list_medicines: list of medicines with name
            and stitch
            type: list
        """

        # Open connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        
        # Execute Query
        db_cur.execute("SELECT concat(commercial_name, ' (', stitch, ')') as com_name_stitch FROM dbms.medicines ORDER BY com_name_stitch;")
        
        # Process result
        list_medicines = []
        for medicine_i in db_cur:
            list_medicines.append(f"{medicine_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_medicines
        
    def max_nr_medicines(self, selected_medicines):
        """Calculates number of medicines selected
        by user and provides status for further 
        processing.

        Args:
            selected_medicines: list of selected meds
            type: list 
        Returns:
            nr_meds: 200(ok), 401(too many), 422(not enough)
            type: int
            len(selected_medicines): number selected medicines
            type: int
        """

        if len(selected_medicines) > 2:
            nr_meds = 401
        elif len(selected_medicines) == 0:
            nr_meds = 422
        else:
            nr_meds = 200
        
        return nr_meds, len(selected_medicines)

    def norm_list_meds(self, medicine_selection):
        """Normalise selected meds to commerical name w/o stich.

        Args:
            medicine_selection: list of selected meds with stitch
            type: list 
        Returns:
            norm_medicine_selection: list of selected meds
            without stitch
            type: list
        """

        len_list = len(medicine_selection)
        norm_medicine_selection = []
        for i in range(len_list):
            len_sel_med = len(medicine_selection[i])
            norm_medicine_selection.append(medicine_selection[i][:len_sel_med-15:])
        
        return norm_medicine_selection


    def get_listSideEffects(self, selected_meds):
        """Provides a list of side effects with their ids
        registred in the database for one given medicine.

        Queries table for mono medicines.

        Args:
            selected_meds: commercial name of one selected med
            type: str 
        Returns:
            list_meds1_sideEffects: list of side effects for mono meds.,
            e.g. ['<side effect name> (<id>)', '...', ...]
            type: list
        """

        # Open db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        # Exec query 
        db_cur.execute("""select concat(individual_side_effect_name, ' (', individual_side_effect, ')') as se_name_se_id from dbms.medicines m0, dbms.medicine_mono m1 where m0.stitch = m1.stitch and m0.commercial_name like %(medname)s order by se_name_se_id;""", {'medname': selected_meds})
        
        list_meds1_sideEffects = []
        for sideEffect_i in db_cur:
            list_meds1_sideEffects.append(f"{sideEffect_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_meds1_sideEffects
    

    def create_DataFrame(self, selected_meds, listSideEffects):
        """Creates one column for a given list of side effects
        for a given mono medicine as a dataframe.

        Args:
            selected_meds: commercial name of one selected med
            type: str
            listSideEffects: list of side effects for selected_meds
            type: list  
        Returns:
            df: List of side effects represented as a dataframe with
            an attribute title 'Side effects from <commercial name>'
            type: dataframe
        """

        df_definition = {'Side effects from ' + selected_meds: listSideEffects}
        df = pd.DataFrame(data=df_definition)
        
        return df
    

    def get_listSideEffects_combo(self, selected_meds):
        """Provides a list of side effects with their ids
        registred in the database for two combined medicines.

        Queries table for combo medicines.

        Args:
            selected_meds: commercial names of two selected meds
            type: str 
        Returns:
            list_meds1_sideEffects: list of side effects for combo meds.,
            e.g. ['<side effect name> (<id>)', '...', ...]
            type: list
        """
        
        # Open db connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()

        # Exec query 
        db_cur.execute("""select concat(combo_side_effect_name, ' (', polypharmacy_side_effect, ')') as se_name_se_id from dbms.medicines_combo mc, dbms.medicines m0, dbms.medicines m1 where mc.stitch1 = m0.stitch and mc.stitch2 = m1.stitch and ((m0.commercial_name like %(medname1)s and m1.commercial_name like %(medname2)s) or (m0.commercial_name like %(medname2)s and m1.commercial_name like %(medname1)s)) order by se_name_se_id;""", {'medname1': selected_meds[0], 'medname2': selected_meds[1]})

        # Process query result
        list_meds1_sideEffects = []
        for sideEffect_i in db_cur:
            list_meds1_sideEffects.append(f"{sideEffect_i[0]}")
        
        # Close connection
        db.disconnect_postgres(db_connection, db_cur)

        return list_meds1_sideEffects


    def create_DataFrame_combo(self, selected_meds, listSideEffects):
        """Creates one column for a given list of side effects
        for given combo medicines as a dataframe.

        Args:
            selected_meds: commercial names of two selected meds
            type: str
            listSideEffects: list of side effects for selected_meds
            type: list  
        Returns:
            df: List of side effects represented as a dataframe with
            an attribute title 'Side effects from the combination of
            <commercial name1> and <commercial name2>'
            type: dataframe
        """
        
        df_definition = {'Side effects from the combination of ' + selected_meds[0] + ' and ' + selected_meds[1]: listSideEffects}
        df = pd.DataFrame(data=df_definition)
        
        return df

# Reporting from here:
    def list_side_effects_mono(self, selected_meds):
        """Provides a list of side effects with their ids
        registred in the database for one given medicine.

        Queries table for mono medicines.

        Args:
            selected_meds: commercial name of one selected med
            type: str 
        Returns:
            list_meds1_sideEffects: list of side effects for mono meds.,
            e.g. ['<side effect name> (<id>)', '...', ...]
            type: list
        """

        # Open connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        
        db_cur.execute("""select concat(individual_side_effect_name, ' (', individual_side_effect, ')') as se_name_se_id from dbms.medicines m0, dbms.medicine_mono m1 where m0.stitch = m1.stitch and m0.commercial_name like %(medname)s order by se_name_se_id;""", {'medname': selected_meds})
        
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
        #db_cur.execute("""select mc.combo_side_effect_name from dbms.medicines_combo mc, dbms.medicines m0, dbms.medicines m1 where mc.stitch1 = m0.stitch and mc.stitch2 = m1.stitch and ((m0.commercial_name = %(medname1)s and m1.commercial_name= %(medname2)s) or (m0.commercial_name = %(medname2)s and m1.commercial_name= %(medname1)s)) order by mc.combo_side_effect_name;""", {'medname1': selected_meds[0], 'medname2': selected_meds[1]})
        
        db_cur.execute("""select concat(combo_side_effect_name, ' (', polypharmacy_side_effect, ')') as se_name_se_id from dbms.medicines_combo mc, dbms.medicines m0, dbms.medicines m1 where mc.stitch1 = m0.stitch and mc.stitch2 = m1.stitch and ((m0.commercial_name like %(medname1)s and m1.commercial_name like %(medname2)s) or (m0.commercial_name like %(medname2)s and m1.commercial_name like %(medname1)s)) order by se_name_se_id;""", {'medname1': selected_meds[0], 'medname2': selected_meds[1]})
        
        list_side_effects_combo = []
        for side_effect_i in db_cur:
            list_side_effects_combo.append(f"{side_effect_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_side_effects_combo

    
    def report_side_effects_mono(self, nr_selected_meds,
                                selected_meds,
                                medicine1_side_effects,
                                medicine2_side_effects, userID):
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
                db_cur.execute("""INSERT INTO dbms.mono_side_effects_reported(commercial_name, reported_by, reporting_date, individual_side_effect_name) VALUES (%(medname1)s, %(reported_by)s, now(), %(medicine1_side_effects)s);""", {'medname1': selected_meds[0], 'reported_by': userID, 'medicine1_side_effects': side_effect_i})

            for side_effect_j in medicine2_side_effects:
                db_cur.execute("""INSERT INTO dbms.mono_side_effects_reported(commercial_name, reported_by, reporting_date, individual_side_effect_name) VALUES (%(medname2)s, %(reported_by)s, now(), %(medicine2_side_effects)s);""", {'medname2': selected_meds[1], 'reported_by': userID, 'medicine2_side_effects': side_effect_j})

            db_connection.commit()

        elif nr_selected_meds == 1:
            
            for side_effect_i in medicine1_side_effects:
                # Exec query
                db_cur.execute("""INSERT INTO dbms.mono_side_effects_reported(commercial_name, reported_by, reporting_date, individual_side_effect_name) VALUES (%(medname1)s, %(reported_by)s, now(), %(medicine1_side_effects)s);""", {'medname1': selected_meds[0], 'reported_by': userID, 'medicine1_side_effects': side_effect_i})
                db_connection.commit()
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        status_msg = 200

        return status_msg

    
    def report_side_effects_combo(self, selected_meds,
                                  side_effects_combo, userID):
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
            db_cur.execute("""INSERT INTO dbms.combo_side_effects_reported(commercial_name1, commercial_name2, reported_by, reporting_date, combo_side_effect_name) VALUES (%(medname1)s, %(medname2)s, %(reported_by)s, now(), %(combo_side_effects)s);""", {'medname1': selected_meds[0], 'medname2': selected_meds[1], 'reported_by': userID, 'combo_side_effects': side_effect_i})
        
        db_connection.commit()
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        status_msg = 200

        return status_msg


if __name__ == "__main__":
    pass
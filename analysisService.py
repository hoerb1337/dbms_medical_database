import streamlit as st
import pandas as pd

# Backend service
import database

class data4Analysis:
    def __init__(self):
        pass

    def get_sideEffects(self, combo):
        """Get list of side effects from mono/combo medicines
           stored in database.

        Args:
            combo: "True" or "False"
            type: str 
        Returns:
            list_sideEffects: list of side effects
            type: list
        """

        # Open connection
        db = database.db_connection()
        db_connection, db_cur = db.connect_postgres()
        if combo == "True":
            db_cur.execute("select distinct mc.combo_side_effect_name " + 
                           "from dbms.medicines m0, dbms.medicines m1, dbms.medicines_combo mc " + 
                           "where m0.stitch = mc.stitch1 and m1.stitch = mc.stitch2;")
            list_sideEffects = []
            for sideEffect_i in db_cur:
                list_sideEffects.append(f"{sideEffect_i[0]}")
        else:
            db_cur.execute("select distinct mm.individual_side_effect_name " +
                           "from dbms.medicines m0, dbms.medicine_mono mm " +
                           "where m0.stitch = mm.stitch;")
            list_sideEffects = []
            for sideEffect_i in db_cur:
                list_sideEffects.append(f"{sideEffect_i[0]}")
        
        # Close connection
        close_db_connection = db.disconnect_postgres(db_connection, db_cur)

        return list_sideEffects
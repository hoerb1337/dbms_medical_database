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
        
    #def 
    #db_cur.execute("select commercial_name from dbms.medicines;")
        #nlist = []
        #for record in db_cur:
            #nlist.append(f"{record[0]}") 
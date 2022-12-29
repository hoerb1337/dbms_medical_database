import streamlit as st
import psycopg2

class db_connection:
    def __init__(self):
        self.db_connection_status = "inactive"
    
    # Initialize connection.
    def connect_postgres(self):
        connected_db = psycopg2.connect(**st.secrets["postgres"])
        cur_connected_db = connected_db.cursor()
        self.db_connection_status = "connected"
        
        # Return db connection and cursor
        return connected_db, cur_connected_db
    
    # Disconnect connection
    def disconnect_postgres(self, cur_connected_db, connected_db):
        disconnected_cur = cur_connected_db.close()
        disconnected_db = connected_db.close()
        self.db_connection_status = "disconnected"

        # Return db cursor and db connection
        return disconnected_cur, disconnected_db


if __name__ == "__main__":
    pass
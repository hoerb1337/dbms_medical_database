###### Production Version 1.0 database #####

import streamlit as st
import psycopg2

class db_connection:
    """Methods to connect and disconnect to database."""

    def __init__(self):
        self.db_connection_status = "inactive"
    

    def connect_postgres(self):
        """Creates connection to the PostgreSQL database.

        Args:
            None 
        Returns:
            connected_db: Connection Object 
            type: object
            cur_connected_db: Cursor of connection
            type: object
        """

        connected_db = psycopg2.connect(**st.secrets["postgres"])
        cur_connected_db = connected_db.cursor()
        self.db_connection_status = "connected"
        
        # Return db connection and cursor
        return connected_db, cur_connected_db
    

    def disconnect_postgres(self, cur_connected_db, connected_db):
        """Closes connection to the PostgreSQL database.

        Args:
            cur_connected_db: Cursor of connection
            type: object 
            connected_db: Connection Object 
            type: object
        Returns:
            disconnected_cur: Closed cursor of connection
            type: object
            disconnected_db: Closed connection Object 
            type: object
        """

        disconnected_cur = cur_connected_db.close()
        disconnected_db = connected_db.close()
        self.db_connection_status = "disconnected"

        # Return db cursor and db connection
        return disconnected_cur, disconnected_db


if __name__ == "__main__":
    pass
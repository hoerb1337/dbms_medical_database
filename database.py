import streamlit as st
import psycopg2

class db_connection:
    def __init__(self):
        pass
    
    # Initialize connection.
    def connect_postgres(self):
        return psycopg2.connect(**st.secrets["postgres"])


if __name__ == "__main__":
    pass
import sqlite3

DATABASE_PATH = "notes.db"  # Database file located in the same folder

def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row  # So rows return as dict-like objects
    return connection

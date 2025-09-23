import os
import mysql.connector

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "e-commerce-web"),
}


def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    # Always return dictionary-style results
    conn.cursor_factory = lambda: conn.cursor(dictionary=True)
    return conn

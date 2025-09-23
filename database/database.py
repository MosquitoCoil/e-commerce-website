import os
import mysql.connector

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "e-commerce-web"),
}


def get_db_connection():
    """Return a MySQL connection."""
    return mysql.connector.connect(**db_config)

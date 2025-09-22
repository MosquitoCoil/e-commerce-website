import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "e-commerce-web",
}


def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    # force dict cursor every time
    conn.cursor_factory = lambda: conn.cursor(dictionary=True)
    return conn

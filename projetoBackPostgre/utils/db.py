import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "nova-senha"),
        database=os.getenv("MYSQL_DB", "bot"),
        port=os.getenv("MYSQL_ROOT", "3307")
    )
    return conn

def close_db(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
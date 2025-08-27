import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "projetobot")
    )
    return conn

def close_db(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'), cursor_factory=RealDictCursor)

def save_log(user_id, query, response):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO logs (user_id, query, response) VALUES (%s, %s, %s)",
                (user_id, query, response)
            )
            conn.commit()
    finally:
        conn.close()

def get_user_logs(user_id, limite=10):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM logs WHERE user_id = %s ORDER BY created_at DESC LIMIT %s",
                (user_id, limite)
            )
            return cur.fetchall()
    finally:
        conn.close()

def get_all_logs():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM logs ORDER BY created_at DESC")
            return cur.fetchall()
    finally:
        conn.close()
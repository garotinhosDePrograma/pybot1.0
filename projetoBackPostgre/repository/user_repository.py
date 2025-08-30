import psycopg2
from psycopg2.extras import RealDictCursor
import os
import bcrypt

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'), cursor_factory=RealDictCursor)

def save_user(nome, email, senha):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cur.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s) RETURNING id",
                (nome, email, hashed_senha)
            )
            user_id = cur.fetchone()['id']
            conn.commit()
            return user_id
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            return cur.fetchone()
    finally:
        conn.close()

def get_all_users():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios")
            return cur.fetchall()
    finally:
        conn.close()

def get_user_by_id(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
            return cur.fetchone()
    finally:

        conn.close()

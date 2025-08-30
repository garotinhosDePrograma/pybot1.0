import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'), cursor_factory=RealDictCursor)

def setup_database():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(50) NOT NULL,
                    query TEXT NOT NULL,
                    response TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    os.environ['DATABASE_URL'] = "postgresql://bot_user:w2cs2IJk2EkuwaV58AuNMeTn2TpM2jCI@dpg-d2nt283e5dus739e450g-a/bot_dpp9"
    setup_database()
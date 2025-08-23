from utils.db import get_connection

def find_by_email(email: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from usuarios where email = %s", (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

def find_by_id(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from usuarios where id = %s", (usuario_id))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close
    return usuario

def create_usuario(nome: str, email: str, senha_hash: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "insert into usuarios (nome, email, senha) values (%s, %s, %s)",
        (nome, email, senha_hash)
    )
    conn.commit()
    usuario_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return usuario_id

def update_senha(usuario_id: int, nova_senha_hash: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "update usuarios set senha = %s where id = %s",
        (nova_senha_hash, usuario_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True

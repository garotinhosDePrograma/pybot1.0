from models.user_model import User
from utils.db import get_db
from datetime import datetime
import mysql.connector

class UserRepository:
    def create_usuario(self, nome: str, email: str, senha: str) -> int:
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, senha)
            )
            conn.commit()
            if cursor.lastrowid is None:
                raise ValueError("Falha ao criar usuário: nenhum ID retornado")
            user_id = cursor.lastrowid
            return user_id
        except mysql.connector.Error as e:
            if e.errno == 1062:
                raise ValueError("Email já existe")
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_user_by_email(self, email: str) -> User:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return User(
                id=user_data[0],
                nome=user_data[1],
                email=user_data[2],
                senha=user_data[3],
                criado_em=user_data[4]
            )
        return None

    def save_log(self, usuario_id: int, pergunta: str, resposta: str):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (usuario_id, pergunta, resposta) VALUES (%s, %s, %s)",
            (usuario_id, pergunta, resposta)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_all(self) -> list:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        users_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            {
                "id": user[0],
                "nome": user[1],
                "email": user[2],
                "criado_em": user[4].isoformat()
            } for user in users_data
        ]

    def find_by_id(self, usuario_id: int) -> dict:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return {
                "id": user_data[0],
                "nome": user_data[1],
                "email": user_data[2],
                "criado_em": user_data[4].isoformat()
            }
        return None

    def update_usuario(self, usuario_id: int, nome: str = None, email: str = None) -> bool:
        conn = get_db()
        cursor = conn.cursor()
        updates = []
        params = []
        if nome:
            updates.append("nome = %s")
            params.append(nome)
        if email:
            updates.append("email = %s")
            params.append(email)
        if not updates:
            cursor.close()
            conn.close()
            return False
        params.append(usuario_id)
        query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(query, params)
        conn.commit()
        affected = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return affected

    def update_senha(self, usuario_id: int, nova_senha: str):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET senha = %s WHERE id = %s", (nova_senha, usuario_id))
        conn.commit()
        cursor.close()
        conn.close()

    def delete_usuario(self, usuario_id: int):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def buscar_logs(self, usuario_id: int, limite: int = 10) -> list:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT pergunta, resposta, criado_em FROM logs WHERE usuario_id = %s ORDER BY criado_em DESC LIMIT %s",
            (usuario_id, limite)
        )
        logs_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            {
                "pergunta": log[0],
                "resposta": log[1],
                "criado_em": log[2].isoformat()
            } for log in logs_data
        ]
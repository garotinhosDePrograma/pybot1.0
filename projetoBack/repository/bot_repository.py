from utils.db import get_connection
import datetime

def salvar_interacao(usuario_id: int, pergunta: str, resposta: str):
    conn = get_connection
    cursor = conn.cursor()
    cursor.execute(
        "insert into logs (usuario_id, perginta, resposta, criado_em) values (%s, %s, %s, %s)",
        (usuario_id, pergunta, resposta, datetime.datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True

def buscar_logs(usuario_id: int, limite: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "select * from logs where usuario_id = %s order by criado_em desc limit %s",
        (usuario_id, limite)
    )
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return logs

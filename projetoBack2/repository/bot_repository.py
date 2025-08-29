import json
import os
from datetime import datetime

LOGS_FILE = 'logs.json'

def init_logs_file():
    if not os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, 'w') as f:
            json.dump([], f)

def save_log(user_id, pergunta, resposta):
    init_logs_file()
    with open(LOGS_FILE, 'r') as f:
        logs = json.load(f)
    logs.append({
        'usuario_id': str(user_id),
        'pergunta': pergunta,
        'resposta': resposta,
        'criado_em': datetime.utcnow().isoformat()
    })
    with open(LOGS_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def get_user_logs(user_id, limite=10):
    init_logs_file()
    with open(LOGS_FILE, 'r') as f:
        logs = json.load(f)
    user_logs = [log for log in logs if log['usuario_id'] == str(user_id)]
    return user_logs[-limite:]

def get_all_logs():
    init_logs_file()
    with open(LOGS_FILE, 'r') as f:
        return json.load(f)
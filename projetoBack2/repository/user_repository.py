import json
import os
import bcrypt
from datetime import datetime

USERS_FILE = 'users.json'

def init_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)

def save_user(nome, email, senha):
    init_users_file()
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    user_id = max([user['id'] for user in users], default=0) + 1
    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    users.append({
        'id': user_id,
        'nome': nome,
        'email': email,
        'senha': hashed_senha,
        'criado_em': datetime.utcnow().isoformat()
    })
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    return user_id

def get_user_by_email(email):
    init_users_file()
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    for user in users:
        if user['email'] == email:
            return user
    return None

def get_all_users():
    init_users_file()
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def get_user_by_id(user_id):
    init_users_file()
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    for user in users:
        if user['id'] == user_id:
            return user
    return None
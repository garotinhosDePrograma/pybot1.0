from flask import Blueprint, request, jsonify
from repository.user_repository import save_user, get_user_by_email, get_all_users, get_user_by_id
import jwt
import os
import bcrypt

user_bp = Blueprint('user', __name__)

@user_bp.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    if not all([nome, email, senha]):
        return jsonify({'status': 'error', 'message': 'Campos obrigatórios'}), 400

    if get_user_by_email(email):
        return jsonify({'status': 'error', 'message': 'Email já cadastrado'}), 400

    user_id = save_user(nome, email, senha)
    token = jwt.encode({'user_id': user_id}, os.getenv('SECRET_KEY'), algorithm='HS256')
    return jsonify({'status': 'success', 'token': token})

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    user = get_user_by_email(email)
    if user and bcrypt.checkpw(senha.encode('utf-8'), user['senha'].encode('utf-8')):
        token = jwt.encode({'user_id': user['id']}, os.getenv('SECRET_KEY'), algorithm='HS256')
        return jsonify({'status': 'success', 'token': token})
    return jsonify({'status': 'error', 'message': 'Credenciais inválidas'}), 401

@user_bp.route('/users', methods=['GET'])
def get_all_users_route():
    users = get_all_users()
    return jsonify(users)

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id_route(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({'status': 'error', 'message': 'Usuário não encontrado'}), 404
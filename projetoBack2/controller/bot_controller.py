from flask import Blueprint, request, jsonify
from repository.bot_repository import save_log, get_user_logs, get_all_logs
from datetime import datetime
import os
import jwt

bot_bp = Blueprint('bot', __name__)

@bot_bp.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'status': 'error', 'message': 'Query não fornecida'}), 400
    resposta = f"Resposta para: {query}"
    auth_header = request.headers.get('Authorization')
    user_id = 'anonymous'
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            decoded = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            user_id = decoded['user_id']
        except jwt.InvalidTokenError:
            pass
    save_log(user_id, query, resposta)
    return jsonify({
        'status': 'success',
        'response': resposta,
        'timestamp': datetime.utcnow().isoformat()
    })

@bot_bp.route('/logs/<user_id>', methods=['GET'])
def get_logs(user_id):
    limite = int(request.args.get('limite', 10))
    logs = get_user_logs(user_id, limite)
    return jsonify({
        'status': 'success',
        'total': len(logs),
        'data': logs,
        'timestamp': datetime.utcnow().isoformat()
    })

@bot_bp.route('/logs', methods=['GET'])
def get_all_logs_route():
    logs = get_all_logs()
    return jsonify({
        'status': 'success',
        'total': len(logs),
        'data': logs,
        'timestamp': datetime.utcnow().isoformat()
    })

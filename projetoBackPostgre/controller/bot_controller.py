from flask import Blueprint, request, jsonify
from worker.bot_worker import BotWorker
from repository.user_repository import UserRepository
from utils.auth import token_required, optional_token
from functools import wraps

bot_bp = Blueprint('bot', __name__)
bot_worker = BotWorker()
user_repo = UserRepository()

@bot_bp.route('/query', methods=['POST'])
@optional_token
def handle_query(usuario_id=None):
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"status": "error", "message": "Query não fornecida"}), 400
    try:
        result = bot_worker.process_query(query, usuario_id)
        if result['status'] == 'success' and usuario_id:
            user_repo.save_log(usuario_id, query, f"{result['response']} (Fonte: {result['source']})")
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bot_bp.route('/log', methods=['POST'])
@token_required
def salvar_log(current_user):
    data = request.get_json()
    if not data or not data.get("usuario_id") or not data.get("pergunta") or not data.get("resposta"):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400
    if data["usuario_id"] != current_user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403
    try:
        user_repo.save_log(data["usuario_id"], data["pergunta"], data["resposta"])
        return jsonify({"message": "Interação salva com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bot_bp.route('/logs/<int:usuario_id>', methods=['GET'])
@token_required
def buscar_logs(current_user, usuario_id):
    if usuario_id != current_user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403
    limite = request.args.get("limite", default=10, type=int)
    try:
        logs = user_repo.buscar_logs(usuario_id, limite)
        return jsonify(logs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
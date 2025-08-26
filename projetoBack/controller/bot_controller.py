from flask import Blueprint, request, jsonify
from worker.bot_worker import process_question
from repository.log_repository import save_log, get_logs_by_user
from utils.auth import token_required

bot_bp = Blueprint("bot", __name__)

@bot_bp.route("/ask", methods=["POST"])
@token_required()
def ask(current_user):
    data = request.get_json()
    pergunta = data.get("pergunta")

    if not pergunta:
        return jsonify({"error": "Pergunta não fornecida"}), 400

    resposta = process_question(pergunta)
    save_log(current_user["id"], pergunta, resposta)

    return jsonify({
        "pergunta": pergunta,
        "resposta": resposta
    })


@bot_bp.route("/logs", methods=["GET"])
@token_required()
def logs(current_user):
    logs = get_logs_by_user(current_user["id"])
    return jsonify(logs)

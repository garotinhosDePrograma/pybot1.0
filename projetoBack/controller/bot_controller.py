from flask import request, jsonify
from repository import bot_repository

def salvar_log():
    data = request.get_json()
    if not data or not data.get("usuario_id") or not data.get("pergunta") or not data.get("resposta"):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    try:
        bot_repository.salvar_interacao(
            data["usuario_id"],
            data["pergunta"],
            data["resposta"]
        )
        return jsonify({"message": "Interação salva com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def buscar_logs(usuario_id: int):
    limite = request.args.get("limite", default=10, type=int)
    try:
        logs = bot_repository.buscar_logs(usuario_id, limite)
        return jsonify(logs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


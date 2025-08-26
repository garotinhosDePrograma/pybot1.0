from flask import Blueprint, request, jsonify
from repository import log_repository

log_bp = Blueprint("log", __name__)

@log_bp.route("/", methods=["POST"])
def salvar_interacao():
    data = request.get_json()
    usuario_id = data.get("usuario_id")
    pergunta = data.get("pergunta")
    resposta = data.get("resposta")

    if not usuario_id or not pergunta or not resposta:
        return jsonify({"erro": "usuario_id, pergunta e resposta são obrigatórios"}), 400

    ok = log_repository.salvar_interacao(usuario_id, pergunta, resposta)
    if ok:
        return jsonify({"mensagem": "Log salvo com sucesso"}), 201
    return jsonify({"erro": "Erro ao salvar log"}), 500


@log_bp.route("/<int:usuario_id>", methods=["GET"])
def buscar_logs(usuario_id):
    limite = request.args.get("limite", 10, type=int)
    logs = log_repository.buscar_logs(usuario_id, limite)
    return jsonify(logs), 200



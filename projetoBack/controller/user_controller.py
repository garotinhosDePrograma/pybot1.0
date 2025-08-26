from flask import Blueprint, request, jsonify
from repository import user_repository

user_bp = Blueprint("user", __name__)

@user_bp.route("/", methods=["POST"])
def criar_usuario():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha_hash = data.get("senha") 

    if not nome or not email or not senha_hash:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    try:
        usuario_id = user_repository.create_usuario(nome, email, senha_hash)
        return jsonify({"mensagem": "Usuário criado com sucesso", "id": usuario_id}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@user_bp.route("/<int:usuario_id>", methods=["GET"])
def buscar_usuario(usuario_id):
    usuario = user_repository.find_by_id(usuario_id)
    if usuario:
        return jsonify(usuario), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

@user_bp.route("/<int:usuario_id>", methods=["PUT"])
def atualizar_usuario(usuario_id):
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")

    if not nome and not email:
        return jsonify({"erro": "Nada para atualizar"}), 400

    ok = user_repository.update_usuario(usuario_id, nome, email)
    if ok:
        return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200
    return jsonify({"erro": "Falha ao atualizar usuário"}), 500

@user_bp.route("/<int:usuario_id>", methods=["DELETE"])
def deletar_usuario(usuario_id):
    ok = user_repository.delete_usuario(usuario_id)
    if ok:
        return jsonify({"mensagem": "Usuário deletado com sucesso"}), 200
    return jsonify({"erro": "Falha ao deletar usuário"}), 500

@user_bp.route("/", methods=["GET"])
def listar_usuarios():
    try:
        conn = user_repository.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, email, criado_em FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


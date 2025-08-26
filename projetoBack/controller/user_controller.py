from flask import request, jsonify
from repository import user_repository

def listar_usuarios():
    try:
        usuarios = user_repository.get_all()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def buscar_usuario(usuario_id: int):
    try:
        usuario = user_repository.find_by_id(usuario_id)
        if not usuario:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify(usuario), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def criar_usuario():
    data = request.get_json()
    if not data or not data.get("nome") or not data.get("email") or not data.get("senha"):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400
    
    try:
        usuario_id = user_repository.create_usuario(
            data["nome"], data["email"], data["senha"]
        )
        return jsonify({"id": usuario_id, "message": "Usuário criado com sucesso"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def atualizar_usuario(usuario_id: int):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado enviado"}), 400

    try:
        atualizado = user_repository.update_usuario(
            usuario_id,
            nome=data.get("nome"),
            email=data.get("email")
        )
        if not atualizado:
            return jsonify({"error": "Nada para atualizar"}), 400
        return jsonify({"message": "Usuário atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def atualizar_senha(usuario_id: int):
    data = request.get_json()
    if not data or not data.get("nova_senha"):
        return jsonify({"error": "Nova senha é obrigatória"}), 400

    try:
        user_repository.update_senha(usuario_id, data["nova_senha"])
        return jsonify({"message": "Senha atualizada com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def deletar_usuario(usuario_id: int):
    try:
        user_repository.delete_usuario(usuario_id)
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

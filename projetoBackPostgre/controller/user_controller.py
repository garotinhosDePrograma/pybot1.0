from flask import Blueprint, request, jsonify
from repository.user_repository import UserRepository
from utils.auth import token_required, hash_password, verify_password, create_token

user_bp = Blueprint('user', __name__)
user_repo = UserRepository()

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("senha"):
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    user = user_repo.get_user_by_email(data["email"])
    if not user or not verify_password(data["senha"], user.senha):
        return jsonify({"error": "Credenciais inválidas"}), 401
    token = create_token({"user_id": user.id, "email": user.email})
    return jsonify({"token": token, "user": {"id": user.id, "nome": user.nome, "email": user.email}}), 200

@user_bp.route('/users', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    if not data or not data.get("nome") or not data.get("email") or not data.get("senha"):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400
    try:
        hashed_senha = hash_password(data["senha"])
        usuario_id = user_repo.create_usuario(data["nome"], data["email"], hashed_senha)
        return jsonify({"id": usuario_id, "message": "Usuário criado com sucesso"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno: " + str(e)}), 500

@user_bp.route('/users', methods=['GET'])
@token_required
def listar_usuarios(current_user):
    try:
        usuarios = user_repo.get_all()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/users/<int:usuario_id>', methods=['GET'])
@token_required
def buscar_usuario(current_user, usuario_id):
    if usuario_id != current_user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403
    try:
        usuario = user_repo.find_by_id(usuario_id)
        if not usuario:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify(usuario), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/users/<int:usuario_id>', methods=['PUT'])
@token_required
def atualizar_usuario(current_user, usuario_id):
    if usuario_id != current_user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado enviado"}), 400
    try:
        atualizado = user_repo.update_usuario(
            usuario_id,
            nome=data.get("nome"),
            email=data.get("email")
        )
        if not atualizado:
            return jsonify({"error": "Nada para atualizar"}), 400
        return jsonify({"message": "Usuário atualizado com sucesso"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/users/<int:usuario_id>/password', methods=['PUT'])
@token_required
def atualizar_senha(current_user, usuario_id):
    if usuario_id != current_user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403
    data = request.get_json()
    if not data or not data.get("nova_senha"):
        return jsonify({"error": "Nova senha é obrigatória"}), 400
    try:
        hashed_senha = hash_password(data["nova_senha"])
        user_repo.update_senha(usuario_id, hashed_senha)
        return jsonify({"message": "Senha atualizada com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/users/<int:usuario_id>', methods=['DELETE'])
@token_required
def deletar_usuario(current_user, usuario_id):
    if usuario_id != current_user.id:
        return jsonify({"error": "Acesso não autorizado"}), 403
    try:
        user_repo.delete_usuario(usuario_id)
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
from flask import Blueprint, request, jsonify
from repository.userRepository import find_by_email, create_usuario
from utils.auth import hash_password

usuario_bp = Blueprint("user", __name__)
user_bp = Blueprint("user", __name__)

@usuario_bp.route("/signup", methods=["POST"])
def signuo():
    data = request.get_json()

    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if not nome or not email or not senha:
        return jsonify({"error": "Nome, email e senha são obrigatórios"}), 400
    
    if find_by_email(email):
        return jsonify({"error": "Email já cadastrado"}), 400
    
    senha_hash = hash_password(senha)
    usuario_id = create_usuario(nome, email, senha_hash)

    return jsonify({
        "message": "Usuário cadastrado com sucesso",
        "usuario_id": usuario_id
    }), 201

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    user = get_user_by_email(email)
    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    if not verify_password(senha, user["senha"]):
        return jsonify({"erro": "Senha incorreta"}), 401

    token = create_token({"id": user["id"], "email": user["email"]})

    return jsonify({
        "mensagem": "Login realizado com sucesso",
        "token": token
    }), 200



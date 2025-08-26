from flask import Blueprint, request, jsonify
from repository.user_repository import create_user, get_user_by_email, get_all_users
from utils.auth import generate_token, token_required
from utils.security import verify_password

user_bp = Blueprint("users", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if not nome or not email or not senha:
        return jsonify({"error": "Campos obrigatórios não preenchidos"}), 400

    user = create_user(nome, email, senha)
    if not user:
        return jsonify({"error": "Email já cadastrado"}), 409

    return jsonify({"message": "Usuário registrado com sucesso"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    user = get_user_by_email(email)
    if not user or not verify_password(senha, user["senha"]):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = generate_token(user["id"], user["role"])
    return jsonify({"token": token})


@user_bp.route("/users", methods=["GET"])
@token_required(role="admin")
def list_users():
    users = get_all_users()
    result = [
        {
            "email": u["email"],
            "criado_em": u["criado_em"],
            "status": u["status"],
            "role": u["role"]
        }
        for u in users
    ]
    return jsonify(result)



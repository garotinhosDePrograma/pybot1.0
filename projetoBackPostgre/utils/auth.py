import bcrypt
import jwt
from flask import request, jsonify
from config import Config
from functools import wraps
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def create_token(data: dict, expires_in=3600) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(seconds=expires_in)
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"erro": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"erro": "Token inválido"}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from repository.user_repository import UserRepository
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({"error": "Token é necessário!"}), 401
        decoded = decode_token(token)
        if "erro" in decoded:
            return jsonify({"error": decoded["erro"]}), 401
        repo = UserRepository()
        user = repo.get_user_by_email(decoded.get("email"))
        if not user:
            return jsonify({"error": "Usuário não encontrado!"}), 401
        return f(current_user=user, *args, **kwargs)
    return decorated

def optional_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        usuario_id = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
                decoded = decode_token(token)
                if "erro" not in decoded:
                    usuario_id = decoded.get("user_id")
            except:
                pass
        return f(usuario_id=usuario_id, *args, **kwargs)
    return decorated
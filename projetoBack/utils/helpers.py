import re
from datetime import datetime

def is_valid_email(email: str) -> bool:
    """Valida email com regex simples"""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def current_timestamp() -> str:
    """Retorna timestamp atual formatado"""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def validate_json(required_fields, data):
    """Valida se todos os campos obrigatórios existem em data"""
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Campos ausentes: {', '.join(missing)}"
    return True, ""

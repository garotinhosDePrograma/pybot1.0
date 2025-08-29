from flask import Flask, jsonify
from flask_cors import CORS
from controller.bot_controller import bot_bp
from controller.user_controller import user_bp
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.register_blueprint(bot_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')

@app.route('/api/docs', methods=['GET'])
def docs():
    return jsonify({
        'status': 'success',
        'endpoints': [
            {'path': '/api/cadastro', 'method': 'POST', 'description': 'Cadastra um novo usuário', 'body': {'nome': 'string', 'email': 'string', 'senha': 'string'}, 'response': {'status': 'success', 'token': 'string', 'timestamp': 'string'}},
            {'path': '/api/login', 'method': 'POST', 'description': 'Autentica um usuário', 'body': {'email': 'string', 'senha': 'string'}, 'response': {'status': 'success', 'token': 'string', 'timestamp': 'string'}},
            {'path': '/api/query', 'method': 'POST', 'description': 'Insere uma pergunta/resposta', 'body': {'query': 'string'}, 'headers': {'Authorization': 'Bearer <token> (opcional)'}, 'response': {'status': 'success', 'response': 'string', 'timestamp': 'string'}},
            {'path': '/api/users', 'method': 'GET', 'description': 'Lista todos os usuários', 'response': {'status': 'success', 'total': 'int', 'data': 'array', 'timestamp': 'string'}},
            {'path': '/api/users/<user_id>', 'method': 'GET', 'description': 'Busca usuário por ID', 'response': {'status': 'success', 'data': 'object', 'timestamp': 'string'}},
            {'path': '/api/logs', 'method': 'GET', 'description': 'Lista todos os logs', 'response': {'status': 'success', 'total': 'int', 'data': 'array', 'timestamp': 'string'}},
            {'path': '/api/logs/<user_id>', 'method': 'GET', 'description': 'Lista logs de um usuário', 'query': {'limite': 'int (opcional)'}, 'response': {'status': 'success', 'total': 'int', 'data': 'array', 'timestamp': 'string'}}
        ],
        'timestamp': datetime.utcnow().isoformat()
    })


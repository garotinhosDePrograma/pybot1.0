from flask import Flask
from flask_cors import CORS
from controller.bot_controller import bot_bp
from controller.user_controller import user_bp
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(bot_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
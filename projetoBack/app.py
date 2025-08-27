from flask import Flask
from flask_cors import CORS
from controller.bot_controller import bot_bp
from controller.user_controller import user_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(bot_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
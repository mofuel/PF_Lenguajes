from flask import Flask
from flask_cors import CORS
from app.config.database import db
from app.config.jwt_config import jwt
from dotenv import load_dotenv
import os

# Blueprints
from app.controller.usuario_controller import usuario_bp
from app.controller.reserva_controller import reserva_bp

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Rutas
    app.register_blueprint(usuario_bp, url_prefix="/api/usuario")
    app.register_blueprint(reserva_bp, url_prefix="/api/reserva")

    return app

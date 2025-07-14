from flask import Flask
from flask_cors import CORS
from app.config.database import db
from app.config.jwt_config import jwt
from dotenv import load_dotenv
import os

# Blueprints
from app.controller.usuario_controller import usuario_bp
from app.controller.reserva_controller import reserva_bp
from app.controller.reserva_admin_controller import admin_reserva_bp

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Configuraciones
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)

    # ✅ Configurar CORS correctamente (esto es lo importante)
    CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}}, supports_credentials=True)

    # Registrar Blueprints
    app.register_blueprint(usuario_bp, url_prefix="/api/usuario")
    app.register_blueprint(reserva_bp, url_prefix="/api")
    print("✅ Blueprint de admin registrado correctamente")
    app.register_blueprint(admin_reserva_bp, url_prefix="/api/admin")

    return app

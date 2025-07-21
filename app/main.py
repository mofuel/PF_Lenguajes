from flask import Flask
from flask_cors import CORS
from app.config.database import db           # Conexión con la base de datos
from app.config.jwt_config import jwt        # Configuración de JWT
from dotenv import load_dotenv
import os

# Importación de Blueprints (rutas separadas por módulo)
from app.controller.usuario_controller import usuario_bp
from app.controller.reserva_controller import reserva_bp
from app.controller.reserva_admin_controller import admin_reserva_bp

def create_app():
    app = Flask(__name__)
    load_dotenv()  # Cargar variables de entorno desde .env

    # Configuración de base de datos y JWT
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    # Inicializar extensiones (Base de datos y JWT)
    db.init_app(app)
    jwt.init_app(app)

    # ✅ Configurar CORS (permite peticiones desde el frontend)
    CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}}, supports_credentials=True)

    # Registrar rutas (Blueprints)
    app.register_blueprint(usuario_bp, url_prefix="/api/usuario")
    app.register_blueprint(reserva_bp, url_prefix="/api")
    app.register_blueprint(admin_reserva_bp, url_prefix="/api/admin")
    print("✅ Blueprint de admin registrado correctamente")

    return app

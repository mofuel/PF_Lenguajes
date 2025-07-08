from flask import Blueprint, request, jsonify
from app.service.usuario_service import registrar_usuario
from flask_jwt_extended import create_access_token
from app.repository.usuario_repository import obtener_usuario_por_correo

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/registro", methods=["POST"])
def registro():
    try:
        data = request.json
        nuevo_usuario = registrar_usuario(data)
        return jsonify({"mensaje": "Usuario registrado correctamente."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    correo = data.get("correo")
    contrasena = data.get("password")

    usuario = obtener_usuario_por_correo(correo)
    if not usuario or not usuario.check_password(contrasena):
        return jsonify({"error": "Correo o contraseña incorrectos."}), 401

    token = create_access_token(identity=usuario.id)
    return jsonify({"access_token": token}), 200

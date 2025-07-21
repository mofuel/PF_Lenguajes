# Importaciones necesarias
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service.reserva_service import (
    crear_reserva,
    listar_reservas_usuario,
    cancelar_reserva,
    plaza_ocupada  
)
from datetime import datetime

# Se define el blueprint para las rutas de reservas de usuarios
reserva_bp = Blueprint("reserva", __name__)

# ✅ Ruta de prueba para verificar que el JWT sea válido
@reserva_bp.route("/probar-jwt", methods=["GET"])
@jwt_required()
def probar_jwt():
    usuario_id = get_jwt_identity()
    return jsonify({"mensaje": "JWT válido", "usuario_id": usuario_id}), 200

# ✅ POST /reservar - Crear una reserva
@reserva_bp.route("/reservar", methods=["POST"])
@jwt_required()  # Requiere JWT para identificar al usuario
def reservar():
    try:
        if not request.is_json:
            return jsonify({"error": "El contenido no es JSON válido."}), 400

        data = request.get_json()
        usuario_id = get_jwt_identity()

        # Convertir fechas de string a datetime
        fecha_inicio = datetime.strptime(data["fecha_inicio"], "%Y-%m-%dT%H:%M")
        fecha_fin = datetime.strptime(data["fecha_fin"], "%Y-%m-%dT%H:%M")

        # Validar que la fecha de fin sea posterior a la de inicio
        if fecha_fin <= fecha_inicio:
            return jsonify({"error": "La fecha de fin debe ser posterior a la de inicio."}), 400

        # Validar que la plaza esté disponible en el rango de tiempo
        if plaza_ocupada(data["plaza"], fecha_inicio, fecha_fin):
            return jsonify({"error": "La plaza ya está ocupada en ese horario."}), 400

        # Crear la reserva si todo es válido
        nueva_reserva = crear_reserva(data, usuario_id)
        return jsonify({"mensaje": "Reserva creada correctamente."}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print("🔥 Error inesperado:", str(e))
        traceback.print_exc()
        return jsonify({"error": "Error interno del servidor"}), 500

# ✅ POST /verificar-plaza - Verificar si una plaza está libre
@reserva_bp.route("/verificar-plaza", methods=["POST"])
@jwt_required()  # Requiere autenticación JWT
def verificar_plaza_disponible():
    try:
        data = request.get_json()
        # Convertir fechas para la verificación
        fecha_inicio = datetime.strptime(data["fecha_inicio"], "%Y-%m-%dT%H:%M")
        fecha_fin = datetime.strptime(data["fecha_fin"], "%Y-%m-%dT%H:%M")

        # Comprobar si ya hay una reserva en ese rango de tiempo
        if plaza_ocupada(data["plaza"], fecha_inicio, fecha_fin):
            return jsonify({"error": "Plaza ocupada"}), 409  # 409 = Conflicto

        return jsonify({"disponible": True}), 200  # Plaza libre

    except Exception:
        return jsonify({"error": "Datos inválidos"}), 400

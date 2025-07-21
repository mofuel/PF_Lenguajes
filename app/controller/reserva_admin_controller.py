# Importaciones necesarias para rutas, JWT y lógica de negocio
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service.reserva_service import (
    obtener_todas_reservas,
    obtener_reserva_por_id,
    guardar_reserva,
    eliminar_reserva,
    plaza_ocupada
)
from app.model.reserva import Reserva
from datetime import datetime
from functools import wraps
from app.service.usuario_service import obtener_usuario_por_id  

# Se crea un blueprint para agrupar las rutas de reservas para administradores
admin_reserva_bp = Blueprint("admin_reserva", __name__)

# Middleware personalizado para verificar que el usuario tenga rol admin
def verificar_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        usuario_id = get_jwt_identity()  # Obtiene el ID del usuario desde el token JWT
        usuario = obtener_usuario_por_id(usuario_id)  # Busca al usuario en la BD
        if not usuario or usuario.rol != "admin":
            return jsonify({"error": "Acceso denegado. Se requiere rol admin."}), 403
        return fn(*args, **kwargs)  # Si es admin, continúa con la función original
    return wrapper
    
# ✅ GET /api/admin/reservas - Listar todas las reservas (solo admins)
@admin_reserva_bp.route("/reservas", methods=["GET"])
@jwt_required()       # Requiere autenticación con JWT
@verificar_admin      # Solo permite acceso a usuarios con rol "admin"
def listar_reservas():
    reservas = obtener_todas_reservas()  # Obtiene todas las reservas desde el servicio
    resultado = [
        {
            "id": r.id,
            "placa": r.placa,
            "plaza": r.plaza,
            "fecha_inicio": r.fecha_inicio.strftime("%Y-%m-%dT%H:%M"),  # Formato ISO para frontend
            "fecha_fin": r.fecha_fin.strftime("%Y-%m-%dT%H:%M"),
            "usuario_id": r.usuario_id
        } for r in reservas
    ]
    return jsonify(resultado), 200  # Devuelve lista de reservas en formato JSON


# ✅ GET /api/admin/reservas/<id> - Obtener una reserva por su ID (solo admins)
@admin_reserva_bp.route("/reservas/<int:id>", methods=["GET"])
@jwt_required()        # Requiere autenticación con JWT
@verificar_admin       # Solo permite acceso a usuarios con rol "admin"
def obtener_reserva_admin(id):
    reserva = obtener_reserva_por_id(id)  # Busca la reserva por su ID
    if not reserva:
        return jsonify({"error": "Reserva no encontrada"}), 404  # Si no existe, retorna error 404

    # Devuelve los datos de la reserva en formato JSON
    return jsonify({
        "id": reserva.id,
        "placa": reserva.placa,
        "plaza": reserva.plaza,
        "fecha_inicio": reserva.fecha_inicio.strftime("%Y-%m-%dT%H:%M"),
        "fecha_fin": reserva.fecha_fin.strftime("%Y-%m-%dT%H:%M"),
        "usuario_id": reserva.usuario_id
    }), 200

# ✅ POST /api/admin/reservas - Registrar nueva reserva (solo admins)
@admin_reserva_bp.route("/reservas", methods=["POST"])
@jwt_required()         # Requiere autenticación JWT
@verificar_admin        # Solo usuarios con rol "admin" pueden acceder
def registrar_reserva_admin():
    data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud (JSON)

    try:
        # Convertir las fechas de string a datetime
        fecha_inicio = datetime.strptime(data["fecha_inicio"], "%Y-%m-%dT%H:%M")
        fecha_fin = datetime.strptime(data["fecha_fin"], "%Y-%m-%dT%H:%M")

        # Validar que la fecha de fin sea posterior a la de inicio
        if fecha_fin <= fecha_inicio:
            return jsonify({"error": "La fecha de fin debe ser posterior a la de inicio."}), 400

        # Verificar si la plaza ya está ocupada en ese rango de tiempo
        if plaza_ocupada(data["plaza"], fecha_inicio, fecha_fin):
            return jsonify({"error": "La plaza ya está ocupada en ese horario."}), 400

        # Crear nueva instancia de reserva
        nueva_reserva = Reserva(
            placa=data["placa"],
            plaza=data["plaza"],
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            usuario_id=data["usuario_id"]
        )

        # Guardar en la base de datos
        guardar_reserva(nueva_reserva)
        return jsonify({"mensaje": "Reserva registrada correctamente."}), 201

    except Exception as e:
        return jsonify({"error": "Error al registrar la reserva."}), 400

# ✅ PUT /api/admin/reservas/<id> - Editar reserva
@admin_reserva_bp.route("/reservas/<int:id>", methods=["PUT"])
@jwt_required()
@verificar_admin
def editar_reserva(id):
    reserva = obtener_reserva_por_id(id)
    if not reserva:
        return jsonify({"error": "Reserva no encontrada."}), 404

    data = request.get_json()
    try:
        nueva_plaza = data.get("plaza", reserva.plaza)
        nueva_fecha_inicio = datetime.strptime(data["fecha_inicio"], "%Y-%m-%dT%H:%M")
        nueva_fecha_fin = datetime.strptime(data["fecha_fin"], "%Y-%m-%dT%H:%M")

        if nueva_fecha_fin <= nueva_fecha_inicio:
            return jsonify({"error": "La fecha de fin debe ser posterior a la de inicio."}), 400

        # ✅ Validación de conflicto de plaza, excluyendo la misma reserva
        if plaza_ocupada(nueva_plaza, nueva_fecha_inicio, nueva_fecha_fin, reserva_id=reserva.id):
            return jsonify({"error": "La plaza ya está ocupada en ese horario."}), 400

        # Actualizar campos
        reserva.placa = data.get("placa", reserva.placa)
        reserva.plaza = nueva_plaza
        reserva.fecha_inicio = nueva_fecha_inicio
        reserva.fecha_fin = nueva_fecha_fin
        reserva.usuario_id = data.get("usuario_id", reserva.usuario_id)

        guardar_reserva(reserva)
        return jsonify({"mensaje": "Reserva actualizada correctamente."}), 200

    except Exception as e:
        return jsonify({"error": "Error al actualizar la reserva."}), 400
    

# ✅ DELETE /api/admin/reservas/<id> - Eliminar una reserva (solo admins)
@admin_reserva_bp.route("/reservas/<int:id>", methods=["DELETE"])
@jwt_required()         # Requiere autenticación JWT
@verificar_admin        # Solo usuarios con rol "admin" pueden acceder
def eliminar_reserva_admin(id):
    reserva = obtener_reserva_por_id(id)  # Busca la reserva por ID
    if not reserva:
        return jsonify({"error": "Reserva no encontrada."}), 404

    eliminar_reserva(reserva)  # Elimina la reserva de la base de datos
    return jsonify({"mensaje": "Reserva eliminada correctamente."}), 200

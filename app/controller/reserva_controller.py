from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service.reserva_service import crear_reserva, listar_reservas_usuario, cancelar_reserva

reserva_bp = Blueprint("reserva", __name__)

@reserva_bp.route("/reservar", methods=["POST"])
@jwt_required()
def reservar():
    try:
        data = request.json
        usuario_id = get_jwt_identity()
        nueva_reserva = crear_reserva(data, usuario_id)
        return jsonify({"mensaje": "Reserva creada correctamente."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@reserva_bp.route("/mis-reservas", methods=["GET"])
@jwt_required()
def mis_reservas():
    usuario_id = get_jwt_identity()
    reservas = listar_reservas_usuario(usuario_id)
    resultado = [
        {
            "id": r.id,
            "plaza": r.plaza,
            "fecha_inicio": r.fecha_inicio,
            "fecha_fin": r.fecha_fin
        }
        for r in reservas
    ]
    return jsonify(resultado), 200

@reserva_bp.route("/cancelar/<int:reserva_id>", methods=["DELETE"])
@jwt_required()
def cancelar(reserva_id):
    usuario_id = get_jwt_identity()
    try:
        cancelar_reserva(reserva_id, usuario_id)
        return jsonify({"mensaje": "Reserva cancelada."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403

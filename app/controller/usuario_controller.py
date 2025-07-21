# Importaciones necesarias
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.service.usuario_service import registrar_usuario, listar_usuarios
from app.repository.usuario_repository import obtener_usuario_por_correo, obtener_usuario_por_id

# Se define el blueprint de rutas de usuario
usuario_bp = Blueprint("usuario", __name__)

# ✅ POST /registro - Registro de nuevo usuario
@usuario_bp.route("/registro", methods=["POST"])
def registro():
    try:
        data = request.json
        nuevo_usuario = registrar_usuario(data)
        return jsonify({"mensaje": "Usuario registrado correctamente."}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# ✅ POST /login - Inicio de sesión y generación de JWT
@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    correo = data.get("correo")
    contrasena = data.get("password")

    usuario = obtener_usuario_por_correo(correo)
    if not usuario or not usuario.check_password(contrasena):
        return jsonify({"error": "Correo o contraseña incorrectos."}), 401

    # Generar token con el ID del usuario
    token = create_access_token(identity=str(usuario.id))
    return jsonify({
        "access_token": token,
        "nombre": usuario.nombre,
        "rol": usuario.rol
    }), 200

# ✅ GET /listar - Listar todos los usuarios (solo admin)
@usuario_bp.route("/listar", methods=["GET"])
@jwt_required()
def listar():
    usuario_id = get_jwt_identity()
    usuario_actual = obtener_usuario_por_id(usuario_id)

    if not usuario_actual or usuario_actual.rol != "admin":
        return jsonify({"error": "Acceso denegado"}), 403

    usuarios = listar_usuarios()
    resultado = [
        {
            "id": u.id,
            "nombre": u.nombre,
            "apellido": u.apellido,
            "correo": u.correo,
            "dni": u.dni,
            "telefono": u.telefono,
            "rol": u.rol
        }
        for u in usuarios
    ]
    return jsonify(resultado), 200

# ✅ PUT /<usuario_id> - Editar usuario (solo admin)
@usuario_bp.route("/<int:usuario_id>", methods=["PUT"])
@jwt_required()
def editar(usuario_id):
    usuario_actual_id = get_jwt_identity()
    usuario_actual = obtener_usuario_por_id(usuario_actual_id)

    if not usuario_actual or usuario_actual.rol != "admin":
        return jsonify({"error": "Acceso denegado"}), 403

    usuario = obtener_usuario_por_id(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Actualizar campos recibidos
    data = request.json
    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.apellido = data.get("apellido", usuario.apellido)
    usuario.correo = data.get("correo", usuario.correo)
    usuario.dni = data.get("dni", usuario.dni)
    usuario.telefono = data.get("telefono", usuario.telefono)
    usuario.rol = data.get("rol", usuario.rol)

    from app.config.database import db
    db.session.commit()

    return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200

# ✅ DELETE /<usuario_id> - Eliminar usuario (solo admin)
@usuario_bp.route("/<int:usuario_id>", methods=["DELETE"])
@jwt_required()
def eliminar(usuario_id):
    usuario_actual_id = get_jwt_identity()
    usuario_actual = obtener_usuario_por_id(usuario_actual_id)

    if not usuario_actual or usuario_actual.rol != "admin":
        return jsonify({"error": "Acceso denegado"}), 403

    usuario = obtener_usuario_por_id(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    from app.config.database import db
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200

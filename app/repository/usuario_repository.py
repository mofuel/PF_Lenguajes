from app.model.usuario import Usuario
from app.config.database import db

def guardar_usuario(usuario: Usuario):
    db.session.add(usuario)
    db.session.commit()

def obtener_usuario_por_correo(correo: str):
    return Usuario.query.filter_by(correo=correo).first()

def obtener_usuario_por_dni(dni: str):
    return Usuario.query.filter_by(dni=dni).first()

def obtener_usuario_por_id(user_id: int):
    return Usuario.query.get(user_id)

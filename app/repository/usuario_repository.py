# Importa el modelo Usuario y la base de datos
from app.model.usuario import Usuario
from app.config.database import db

# Guarda un nuevo usuario en la base de datos
def guardar_usuario(usuario: Usuario):
    db.session.add(usuario)
    db.session.commit()

# Busca un usuario por su correo electrónico
def obtener_usuario_por_correo(correo: str):
    return Usuario.query.filter_by(correo=correo).first()

# Busca un usuario por su DNI
def obtener_usuario_por_dni(dni: str):
    return Usuario.query.filter_by(dni=dni).first()

# Busca un usuario por su ID
def obtener_usuario_por_id(user_id: int):
    return Usuario.query.get(user_id)

# Obtiene todos los usuarios registrados
def obtener_todos_los_usuarios():
    return Usuario.query.all()

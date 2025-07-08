from app.model.usuario import Usuario
from app.repository.usuario_repository import (
    guardar_usuario,
    obtener_usuario_por_correo,
    obtener_usuario_por_dni
)

def registrar_usuario(data):
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    dni = data.get("dni")
    telefono = data.get("telefono")
    correo = data.get("correo")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # Validaciones básicas
    if password != confirm_password:
        raise ValueError("Las contraseñas no coinciden.")

    if obtener_usuario_por_correo(correo):
        raise ValueError("Ya existe un usuario con ese correo.")

    if obtener_usuario_por_dni(dni):
        raise ValueError("Ya existe un usuario con ese DNI.")

    # Crear instancia del usuario
    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        telefono=telefono,
        correo=correo
    )
    nuevo_usuario.set_password(password)

    # Guardar en la base de datos
    guardar_usuario(nuevo_usuario)
    return nuevo_usuario

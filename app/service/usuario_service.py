# Importa el modelo Usuario y funciones del repositorio
from app.model.usuario import Usuario
from app.repository.usuario_repository import (
    guardar_usuario,
    obtener_usuario_por_correo,
    obtener_usuario_por_dni,
    obtener_todos_los_usuarios
)

# Registra un nuevo usuario con validaciones básicas
def registrar_usuario(data):
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    dni = data.get("dni")
    telefono = data.get("telefono")
    correo = data.get("correo")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # Validar que las contraseñas coincidan
    if password != confirm_password:
        raise ValueError("Las contraseñas no coinciden.")

    # Verificar si ya existe un usuario con el mismo correo
    if obtener_usuario_por_correo(correo):
        raise ValueError("Ya existe un usuario con ese correo.")

    # Verificar si ya existe un usuario con el mismo DNI
    if obtener_usuario_por_dni(dni):
        raise ValueError("Ya existe un usuario con ese DNI.")

    # Crear una nueva instancia de usuario
    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        telefono=telefono,
        correo=correo
    )
    nuevo_usuario.set_password(password)  # Encripta la contraseña

    # Guarda el usuario en la base de datos
    guardar_usuario(nuevo_usuario)
    return nuevo_usuario

# Lista todos los usuarios registrados
def listar_usuarios():
    return obtener_todos_los_usuarios()

# Obtiene un usuario por su ID
def obtener_usuario_por_id(id):
    return Usuario.query.get(id)

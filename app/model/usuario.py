from app.config.database import db  # Conexión con la base de datos usando SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  # Para manejo seguro de contraseñas
from datetime import datetime  # Para registrar la fecha de creación del usuario

class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # ID único autoincremental
    nombre = db.Column(db.String(100), nullable=False)  # Nombre del usuario 
    apellido = db.Column(db.String(100), nullable=False)  # Apellido del usuario 
    dni = db.Column(db.String(20), unique=True, nullable=False)  # DNI único 
    telefono = db.Column(db.String(15), nullable=False)  # Teléfono del usuario 
    correo = db.Column(db.String(120), unique=True, nullable=False)  # Correo único 
    contrasena_hash = db.Column(db.String(255), nullable=False)  # Contraseña encriptada 
    rol = db.Column(db.String(20), default='usuario')  # Rol del usuario ('usuario' por defecto)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de creación del usuario

    reservas = db.relationship('Reserva', backref='usuario', lazy=True)
    # Relación uno a muchos: un usuario puede tener muchas reservas

    def set_password(self, contrasena):
        """Encripta y guarda la contraseña"""
        self.contrasena_hash = generate_password_hash(contrasena)

    def check_password(self, contrasena):
        """Verifica si la contraseña ingresada coincide con la guardada"""
        return check_password_hash(self.contrasena_hash, contrasena)

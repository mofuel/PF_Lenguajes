from app.config.database import db  # Importa el objeto de conexión a la base de datos
from datetime import datetime  # Para manejar fechas y horas


class Reserva(db.Model):
    __tablename__ = 'reservas'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  
    # ID único autoincremental para cada reserva

    fecha_reserva = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
    # Fecha y hora en que se realiza la reserva (por defecto: ahora)

    fecha_inicio = db.Column(db.DateTime, nullable=False)  
    # Fecha y hora de inicio de la reserva

    fecha_fin = db.Column(db.DateTime, nullable=False)  
    # Fecha y hora de fin de la reserva

    placa = db.Column(db.String(20), nullable=False)
    #Placa del vehiculo a reservar

    plaza = db.Column(db.String(10), nullable=False)
    #Plaza del vehiculo a reservar

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  
    # ID del usuario que realiza la reserva (clave foránea que apunta a la tabla usuarios)

    

    def __repr__(self):
        return f"<Reserva {self.id} - Usuario: {self.usuario_id}"

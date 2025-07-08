from app.config.database import db
from datetime import datetime

class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    fecha_reserva = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    plaza = db.Column(db.String(20), nullable=False)

    # Relación con Usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

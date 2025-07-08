from app.model.reserva import Reserva
from app.config.database import db

def guardar_reserva(reserva: Reserva):
    db.session.add(reserva)
    db.session.commit()

def obtener_reservas_por_usuario(usuario_id: int):
    return Reserva.query.filter_by(usuario_id=usuario_id).all()

def obtener_reserva_por_id(reserva_id: int):
    return Reserva.query.get(reserva_id)

def eliminar_reserva(reserva: Reserva):
    db.session.delete(reserva)
    db.session.commit()

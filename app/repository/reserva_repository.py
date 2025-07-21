# Importa el modelo Reserva y la base de datos
from app.model.reserva import Reserva
from app.config.database import db

# Guarda una nueva reserva en la base de datos
def guardar_reserva(reserva: Reserva):
    db.session.add(reserva)
    db.session.commit()

# Obtiene todas las reservas de un usuario específico
def obtener_reservas_por_usuario(usuario_id: int):
    return Reserva.query.filter_by(usuario_id=usuario_id).all()

# Busca una reserva por su ID
def obtener_reserva_por_id(reserva_id: int):
    return Reserva.query.get(reserva_id)

# Elimina una reserva existente
def eliminar_reserva(reserva: Reserva):
    db.session.delete(reserva)
    db.session.commit()

# Devuelve todas las reservas en la base de datos
def obtener_todas_reservas():
    return Reserva.query.all()

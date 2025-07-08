from app.model.reserva import Reserva
from app.repository.reserva_repository import (
    guardar_reserva,
    obtener_reservas_por_usuario,
    obtener_reserva_por_id,
    eliminar_reserva
)

def crear_reserva(data, usuario_id):
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")
    plaza = data.get("plaza")

    if not fecha_inicio or not fecha_fin or not plaza:
        raise ValueError("Faltan datos obligatorios.")

    nueva_reserva = Reserva(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        plaza=plaza,
        usuario_id=usuario_id
    )
    guardar_reserva(nueva_reserva)
    return nueva_reserva

def listar_reservas_usuario(usuario_id):
    return obtener_reservas_por_usuario(usuario_id)

def cancelar_reserva(reserva_id, usuario_id):
    reserva = obtener_reserva_por_id(reserva_id)
    if not reserva:
        raise ValueError("Reserva no encontrada.")
    if reserva.usuario_id != usuario_id:
        raise PermissionError("No puedes cancelar esta reserva.")
    
    eliminar_reserva(reserva)

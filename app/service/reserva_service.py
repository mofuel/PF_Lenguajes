from app.model.reserva import Reserva
from app.config.database import db
from app.repository.reserva_repository import (
    guardar_reserva,
    obtener_reservas_por_usuario,
    obtener_reserva_por_id,
    eliminar_reserva,
    obtener_todas_reservas
)

from datetime import datetime

def crear_reserva(data, usuario_id):
    try:
        # Convertir fechas de string a datetime
        fecha_inicio_str = data.get("fecha_inicio")
        fecha_fin_str = data.get("fecha_fin")
        plaza = data.get("plaza")
        placa = data.get("placa")

        if not fecha_inicio_str or not fecha_fin_str or not plaza:
            raise ValueError("Faltan datos obligatorios.")

        # ✅ Convertimos las fechas
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%dT%H:%M")
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%dT%H:%M")

        if fecha_fin <= fecha_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la de inicio.")

        nueva_reserva = Reserva(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            plaza=plaza,
            placa=placa,
            usuario_id=usuario_id
        )
        guardar_reserva(nueva_reserva)
        return nueva_reserva
    except ValueError as e:
        raise e
    except Exception:
        raise ValueError("Datos inválidos en la reserva. Verifica los formatos.")


def listar_reservas_usuario(usuario_id):
    return obtener_reservas_por_usuario(usuario_id)

def cancelar_reserva(reserva_id, usuario_id):
    reserva = obtener_reserva_por_id(reserva_id)
    if not reserva:
        raise ValueError("Reserva no encontrada.")
    if reserva.usuario_id != usuario_id:
        raise PermissionError("No puedes cancelar esta reserva.")
    
    eliminar_reserva(reserva)

def obtener_todas_reservas():
    return Reserva.query.all()

def plaza_ocupada(plaza, fecha_inicio, fecha_fin, reserva_id=None):
    query = Reserva.query.filter(
        Reserva.plaza == plaza,
        Reserva.fecha_fin > fecha_inicio,
        Reserva.fecha_inicio < fecha_fin
    )
    if reserva_id:  # Si se está editando una reserva, exclúyela del check
        query = query.filter(Reserva.id != reserva_id)

    return db.session.query(query.exists()).scalar()

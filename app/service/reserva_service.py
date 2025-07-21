# Importaciones del modelo y base de datos
from app.model.reserva import Reserva
from app.config.database import db

# Importaciones del repositorio de reservas
from app.repository.reserva_repository import (
    guardar_reserva,
    obtener_reservas_por_usuario,
    obtener_reserva_por_id,
    eliminar_reserva,
    obtener_todas_reservas
)

from datetime import datetime

# Crea una nueva reserva con validaciones
def crear_reserva(data, usuario_id):
    try:
        # Obtener datos desde el formulario o frontend
        fecha_inicio_str = data.get("fecha_inicio")
        fecha_fin_str = data.get("fecha_fin")
        plaza = data.get("plaza")
        placa = data.get("placa")

        # Validar que no falten datos obligatorios
        if not fecha_inicio_str or not fecha_fin_str or not plaza:
            raise ValueError("Faltan datos obligatorios.")

        # Convertir fechas de string a objetos datetime
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%dT%H:%M")
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%dT%H:%M")

        # Verificar que la fecha de fin sea posterior a la de inicio
        if fecha_fin <= fecha_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la de inicio.")

        # Crear instancia de reserva
        nueva_reserva = Reserva(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            plaza=plaza,
            placa=placa,
            usuario_id=usuario_id
        )

        # Guardar la reserva en la base de datos
        guardar_reserva(nueva_reserva)
        return nueva_reserva
    except ValueError as e:
        raise e
    except Exception:
        raise ValueError("Datos inválidos en la reserva. Verifica los formatos.")

# Lista todas las reservas de un usuario específico
def listar_reservas_usuario(usuario_id):
    return obtener_reservas_por_usuario(usuario_id)

# Cancela una reserva si pertenece al usuario
def cancelar_reserva(reserva_id, usuario_id):
    reserva = obtener_reserva_por_id(reserva_id)
    if not reserva:
        raise ValueError("Reserva no encontrada.")
    if reserva.usuario_id != usuario_id:
        raise PermissionError("No puedes cancelar esta reserva.")
    
    eliminar_reserva(reserva)

# Devuelve todas las reservas (útil para admin o pruebas)
def obtener_todas_reservas():
    return Reserva.query.all()

# Verifica si una plaza está ocupada en el rango dado
def plaza_ocupada(plaza, fecha_inicio, fecha_fin, reserva_id=None):
    query = Reserva.query.filter(
        Reserva.plaza == plaza,
        Reserva.fecha_fin > fecha_inicio,
        Reserva.fecha_inicio < fecha_fin
    )
    # Si se edita una reserva, excluye esa reserva del chequeo
    if reserva_id:
        query = query.filter(Reserva.id != reserva_id)

    # Retorna True si existe conflicto (plaza ocupada), False si está libre
    return db.session.query(query.exists()).scalar()

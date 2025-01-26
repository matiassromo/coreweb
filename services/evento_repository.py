from models import Evento, Asistencia, db
from sqlalchemy.orm import aliased
from datetime import datetime

class EventoRepository:
    def obtener_eventos(self, start_date, end_date):
        # Filtrar por fechas de asistencia
        if start_date and end_date:
            eventos = Evento.query.join(Asistencia).filter(
                db.func.date(Asistencia.fecha_asistencia).between(start_date, end_date)
            ).group_by(Evento.id_evento).all()
        else:
            # Si no hay fechas, obtener todos los eventos
            eventos = Evento.query.all()
        
        return eventos

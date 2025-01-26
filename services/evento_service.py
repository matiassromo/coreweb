from models import Evento, Asistencia
from services.evento_repository import EventoRepository
from datetime import datetime

class EventService:
    def __init__(self, evento_repository: EventoRepository):
        self.evento_repository = evento_repository

    def filtrar_eventos(self, start_date, end_date):
        # Llamamos al repositorio para obtener los eventos filtrados
        return self.evento_repository.obtener_eventos(start_date, end_date)

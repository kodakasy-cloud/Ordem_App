from datetime import datetime, timedelta, date
from typing import List, Optional
from app.modules.calendar.model.event import Event
from app.services.storage import StorageService
from app.utils.helpers import generate_id

class CalendarController:
    """Controlador do módulo de calendário"""
    
    def __init__(self, storage_service: StorageService):
        self.storage = storage_service
        self.events: List[Event] = []
        self.current_date = datetime.now()
        self.current_view = "month"  # month, week, list
        self.load_events()
    
    def load_events(self):
        """Carrega eventos do armazenamento"""
        events_data = self.storage.load_calendar_events()
        self.events = [Event.from_dict(event_data) for event_data in events_data]
        self.sort_events()
    
    def save_events(self):
        """Salva eventos no armazenamento"""
        events_data = [event.to_dict() for event in self.events]
        self.storage.save_calendar_events(events_data)
    
    def sort_events(self):
        """Ordena eventos por data e horário"""
        self.events.sort(key=lambda e: (e.date, e.start_time or time.min))
    
    # Navegação
    def next_period(self):
        """Avança para o próximo período baseado na visualização atual"""
        if self.current_view == "month":
            # Vai para o próximo mês
            if self.current_date.month == 12:
                self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
            else:
                self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        elif self.current_view == "week":
            self.current_date += timedelta(days=7)
        else:  # list
            self.current_date += timedelta(days=30)
    
    def previous_period(self):
        """Volta para o período anterior baseado na visualização atual"""
        if self.current_view == "month":
            # Vai para o mês anterior
            if self.current_date.month == 1:
                self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
            else:
                self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        elif self.current_view == "week":
            self.current_date -= timedelta(days=7)
        else:  # list
            self.current_date -= timedelta(days=30)
    
    def go_to_today(self):
        """Volta para a data atual"""
        self.current_date = datetime.now()
    
    def set_view(self, view: str):
        """Muda a visualização atual (month, week, list)"""
        if view in ["month", "week", "list"]:
            self.current_view = view
    
    # Gerenciamento de eventos
    def add_event(self, title: str, date: datetime, 
                  start_time=None, end_time=None, 
                  description: str = "", color: str = "#3498db") -> Optional[Event]:
        """Adiciona um novo evento"""
        # Verificar conflito de horário
        if self.has_conflict(date, start_time, end_time):
            return None
        
        event = Event(
            id="",  # Será gerado automaticamente
            title=title,
            date=date,
            start_time=start_time,
            end_time=end_time,
            description=description,
            color=color
        )
        self.events.append(event)
        self.sort_events()
        self.save_events()
        return event
    
    def edit_event(self, event_id: str, title: str, date: datetime,
                   start_time=None, end_time=None,
                   description: str = "", color: str = "#3498db") -> bool:
        """Edita um evento existente"""
        # Verificar conflito (excluindo o próprio evento)
        if self.has_conflict(date, start_time, end_time, exclude_id=event_id):
            return False
        
        for i, event in enumerate(self.events):
            if event.id == event_id:
                updated_event = Event(
                    id=event_id,
                    title=title,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    description=description,
                    color=color
                )
                self.events[i] = updated_event
                self.sort_events()
                self.save_events()
                return True
        return False
    
    def delete_event(self, event_id: str) -> bool:
        """Remove um evento"""
        initial_count = len(self.events)
        self.events = [e for e in self.events if e.id != event_id]
        
        if len(self.events) < initial_count:
            self.save_events()
            return True
        return False
    
    def get_events_for_date(self, target_date: date) -> List[Event]:
        """Retorna eventos de uma data específica"""
        return [
            event for event in self.events
            if event.date.date() == target_date
        ]
    
    def get_events_for_range(self, start_date: date, end_date: date) -> List[Event]:
        """Retorna eventos em um período"""
        return [
            event for event in self.events
            if start_date <= event.date.date() <= end_date
        ]
    
    def get_event_by_id(self, event_id: str) -> Optional[Event]:
        """Busca evento por ID"""
        for event in self.events:
            if event.id == event_id:
                return event
        return None
    
    def get_all_events(self) -> List[Event]:
        """Retorna todos os eventos"""
        return self.events.copy()
    
    def has_conflict(self, event_date: datetime, start_time=None, end_time=None, exclude_id: str = None) -> bool:
        """Verifica se há conflito de horário com outro evento"""
        for event in self.events:
            if exclude_id and event.id == exclude_id:
                continue
            
            if event.date.date() != event_date.date():
                continue
            
            # Se não tem horário definido, só conflita se for o mesmo dia
            if not start_time and not event.start_time:
                return True
            
            # Se um tem horário e outro não
            if (start_time and not event.start_time) or (not start_time and event.start_time):
                continue
            
            # Ambos têm horário - verificar sobreposição
            if start_time and event.start_time:
                new_start = datetime.combine(event_date.date(), start_time)
                new_end = datetime.combine(event_date.date(), end_time) if end_time else new_start
                event_start = datetime.combine(event_date.date(), event.start_time)
                event_end = datetime.combine(event_date.date(), event.end_time) if event.end_time else event_start
                
                if max(new_start, event_start) < min(new_end, event_end):
                    return True
        
        return False
    
    def get_upcoming_events(self, days: int = 7) -> List[Event]:
        """Retorna eventos dos próximos dias"""
        today = datetime.now().date()
        future_date = today + timedelta(days=days)
        return self.get_events_for_range(today, future_date)
    
    # Informações da visualização atual
    def get_month_days(self) -> List[date]:
        """Retorna todos os dias do mês atual em uma grid"""
        first_day = self.current_date.replace(day=1)
        start_date = first_day - timedelta(days=first_day.weekday())
        
        # 6 semanas para cobrir completamente o mês
        month_days = []
        for i in range(42):
            day = start_date + timedelta(days=i)
            month_days.append(day.date())
        
        return month_days
    
    def get_week_days(self) -> List[date]:
        """Retorna os dias da semana atual"""
        start = self.current_date - timedelta(days=self.current_date.weekday())
        return [(start + timedelta(days=i)).date() for i in range(7)]
    
    def get_month_name(self) -> str:
        """Retorna nome do mês atual"""
        return self.current_date.strftime("%B %Y")
    
    def get_week_range(self) -> str:
        """Retorna o período da semana atual"""
        week_days = self.get_week_days()
        return f"{week_days[0].strftime('%d/%m')} - {week_days[-1].strftime('%d/%m/%Y')}"
    
    def get_current_date_info(self) -> dict:
        """Retorna informações da data atual"""
        return {
            'year': self.current_date.year,
            'month': self.current_date.month,
            'month_name': self.current_date.strftime("%B"),
            'day': self.current_date.day,
            'weekday': self.current_date.strftime("%A")
        }
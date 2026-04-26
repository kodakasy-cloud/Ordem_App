from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional
from app.utils.helpers import generate_id

@dataclass
class Event:
    """Modelo de evento do calendário"""
    id: str
    title: str
    date: datetime
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: str = ""
    color: str = "#3498db"  # Azul padrão
    
    def __post_init__(self):
        if not self.id:
            self.id = generate_id(self.title, self.date.isoformat())
    
    @property
    def start_datetime(self) -> datetime:
        """Retorna datetime combinando data e hora de início"""
        if self.start_time:
            return datetime.combine(self.date.date(), self.start_time)
        return self.date
    
    @property
    def end_datetime(self) -> datetime:
        """Retorna datetime combinando data e hora de término"""
        if self.end_time:
            return datetime.combine(self.date.date(), self.end_time)
        return self.date.replace(hour=23, minute=59)
    
    @property
    def duration_minutes(self) -> int:
        """Retorna duração do evento em minutos"""
        delta = self.end_datetime - self.start_datetime
        return int(delta.total_seconds() / 60)
    
    @property
    def time_display(self) -> str:
        """Retorna string formatada do horário"""
        if self.start_time:
            start_str = self.start_time.strftime("%H:%M")
            if self.end_time:
                end_str = self.end_time.strftime("%H:%M")
                return f"{start_str} - {end_str}"
            return start_str
        return "Dia todo"
    
    def to_dict(self) -> dict:
        """Converte evento para dicionário (para serialização)"""
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date.isoformat(),
            'start_time': self.start_time.strftime('%H:%M:%S') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M:%S') if self.end_time else None,
            'description': self.description,
            'color': self.color
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        """Cria evento a partir de dicionário"""
        date = datetime.fromisoformat(data['date'])
        start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time() if data.get('start_time') else None
        end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time() if data.get('end_time') else None
        
        return cls(
            id=data['id'],
            title=data['title'],
            date=date,
            start_time=start_time,
            end_time=end_time,
            description=data.get('description', ''),
            color=data.get('color', '#3498db')
        )
    
    def __str__(self):
        if self.start_time:
            return f"{self.start_time.strftime('%H:%M')} - {self.title}"
        return self.title
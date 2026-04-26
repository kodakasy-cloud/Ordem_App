import json
import os
from typing import List, Optional
from datetime import datetime, date
from .event import Event

class Storage:
    def __init__(self, filename: str = "calendar_events.json"):
        self.filename = filename
        self.events: List[Event] = []
        self.load()
    
    def save(self):
        """Salva todos os eventos no arquivo"""
        try:
            data = [event.to_dict() for event in self.events]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar eventos: {e}")
            return False
    
    def load(self):
        """Carrega eventos do arquivo"""
        if not os.path.exists(self.filename):
            self.events = []
            return
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.events = [Event.from_dict(event_data) for event_data in data]
        except Exception as e:
            print(f"Erro ao carregar eventos: {e}")
            self.events = []
    
    def add_event(self, event: Event) -> bool:
        """Adiciona um novo evento"""
        # Verificar se já existe evento com mesmo ID
        if any(e.id == event.id for e in self.events):
            return False
        
        self.events.append(event)
        return self.save()
    
    def update_event(self, event_id: str, updated_event: Event) -> bool:
        """Atualiza um evento existente"""
        for i, event in enumerate(self.events):
            if event.id == event_id:
                self.events[i] = updated_event
                return self.save()
        return False
    
    def delete_event(self, event_id: str) -> bool:
        """Remove um evento"""
        initial_count = len(self.events)
        self.events = [e for e in self.events if e.id != event_id]
        
        if len(self.events) < initial_count:
            return self.save()
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
    
    def clear_all(self):
        """Remove todos os eventos"""
        self.events = []
        self.save()
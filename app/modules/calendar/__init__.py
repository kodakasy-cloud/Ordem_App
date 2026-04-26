"""
Módulo de Calendário
Gerencia eventos, compromissos e lembretes
"""

from .controller.calendar_controller import CalendarController
from .view.calendar_view import CalendarView
from .model.event import Event

__all__ = ['CalendarController', 'CalendarView', 'Event']
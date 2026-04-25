"""
Modules - Módulos funcionais da aplicação
"""
from app.modules.calendar.controller.controller import CalendarController
from app.modules.notes.controller import NotesController
from app.modules.daily.controller import DailyController
from app.modules.finance.controller import FinanceController
from app.modules.setting.controller import SettingController

__all__ = [
    'CalendarController',
    'NotesController',
    'DailyController',
    'FinanceController',
    'SettingController'
]
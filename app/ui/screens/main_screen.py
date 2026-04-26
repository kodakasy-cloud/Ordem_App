"""
Tela principal do aplicativo
Contém o sidebar e a área de conteúdo
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional

from app.ui.components.sidebar import Sidebar
from app.core.router import Router
from app.services.storage import StorageService


class MainScreen(ttk.Frame):
    """Tela principal com sidebar e área de conteúdo"""
    
    def __init__(self, parent, router: Router, storage_service: StorageService,
                 active_module: str, colors: dict):
        super().__init__(parent)
        self.parent = parent
        self.router = router
        self.storage_service = storage_service
        self.active_module = active_module
        self.colors = colors
        
        self.content_frame: Optional[ttk.Frame] = None
        self.current_view: Optional[ttk.Frame] = None
        
        self.setup_ui()
        self.load_module(active_module)
    
    def setup_ui(self):
        """Configura a interface da tela principal"""
        # Configura layout principal
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Cria o sidebar
        self.sidebar = Sidebar(
            self.paned_window,
            self.router,
            self.on_module_selected,
            self.colors
        )
        self.paned_window.add(self.sidebar, weight=1)
        
        # Cria o frame de conteúdo
        self.content_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.content_frame, weight=4)
        
        # Configura o frame de conteúdo
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
    
    def on_module_selected(self, module_id: str):
        """Callback quando um módulo é selecionado no sidebar"""
        if self.router.navigate_to(module_id):
            self.load_module(module_id)
    
    def load_module(self, module_id: str):
        """Carrega e exibe o módulo selecionado"""
        # Limpa o conteúdo atual
        if self.current_view:
            self.current_view.destroy()
        
        # Obtém o controlador do módulo
        controller = self.router.get_module_controller(module_id)
        if not controller:
            self.show_error(f"Módulo '{module_id}' não encontrado")
            return
        
        # Carrega a view do módulo
        module_info = self.router.get_module_info(module_id)
        
        # Importa a view correspondente ao módulo
        if module_id == "calendar":
            from app.modules.calendar.view.calendar_view import CalendarView
            self.current_view = CalendarView(
                self.content_frame,
                controller,
                self.on_module_selected
            )
        elif module_id == "notes":
            from app.modules.notes.view import NotesView
            self.current_view = NotesView(
                self.content_frame,
                controller
            )
        elif module_id == "daily":
            from app.modules.daily.view import DailyView
            self.current_view = DailyView(
                self.content_frame,
                controller
            )
        elif module_id == "finance":
            from app.modules.finance.view import FinanceView
            self.current_view = FinanceView(
                self.content_frame,
                controller
            )
        elif module_id == "setting":
            from app.modules.setting.view import SettingView
            self.current_view = SettingView(
                self.content_frame,
                controller,
                self.storage_service
            )
        else:
            self.show_error(f"View para módulo '{module_id}' não implementada")
            return
        
        self.current_view.pack(fill=tk.BOTH, expand=True)
        
        # Atualiza o título da janela
        self.parent.title(f"MeuCantinho - {module_info['name']}")
    
    def show_error(self, message: str):
        """Exibe mensagem de erro na área de conteúdo"""
        error_label = ttk.Label(
            self.content_frame,
            text=f"❌ {message}",
            font=("Segoe UI", 14)
        )
        error_label.pack(expand=True)
        
        # Auto-destrói após 3 segundos
        self.content_frame.after(3000, error_label.destroy)
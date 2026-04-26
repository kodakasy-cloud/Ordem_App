"""
Classe principal do aplicativo
Gerencia a janela principal e o ciclo de vida
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import Optional

from app.core.router import Router
from app.services.storage import StorageService
from app.ui.screens.main_screen import MainScreen
from app.ui.screens.loading_screen import LoadingScreen


class Application:
    """Classe principal do aplicativo"""
    
    def __init__(self, storage_service: StorageService, router: Router):
        self.storage_service = storage_service
        self.router = router
        self.root: Optional[tk.Tk] = None
        self.current_screen: Optional[ttk.Frame] = None
        
    def run(self):
        """Inicia o aplicativo"""
        # Cria a janela principal
        self.root = tk.Tk()
        self.root.title("MeuCantinho - Seu Espaço Pessoal")
        self.root.geometry("1280x720")
        self.root.minsize(1024, 600)
        
        # Configura o estilo
        self.setup_styles()
        
        # Mostra tela de loading
        self.show_loading_screen()
        
        # Carrega dados em background
        self.root.after(100, self.initialize_app)
        
        # Inicia o loop principal
        self.root.mainloop()
    
    def setup_styles(self):
        """Configura os estilos do ttk"""
        style = ttk.Style()
        
        # Cores principais
        style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"))
        style.configure("Heading.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Normal.TLabel", font=("Segoe UI", 10))
        
        # Configuração do sidebar
        style.configure("Sidebar.TFrame", background="#2c3e50")
        style.configure("Sidebar.TButton", 
                       font=("Segoe UI", 11),
                       padding=10,
                       background="#34495e")
        
        # Cores para diferentes módulos
        self.colors = {
            "calendar": "#3498db",
            "notes": "#2ecc71",
            "daily": "#e74c3c",
            "finance": "#f39c12",
            "setting": "#9b59b6"
        }
    
    def show_loading_screen(self):
        """Exibe a tela de carregamento"""
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = LoadingScreen(self.root, self.colors)
        self.current_screen.pack(fill=tk.BOTH, expand=True)
    
    def initialize_app(self):
        """Inicializa o aplicativo carregando os dados"""
        try:
            # Carrega configurações
            self.config = self.storage_service.load_config()
            
            # Registra os módulos no router
            self.register_modules()
            
            # Carrega o módulo ativo
            active_module = self.config.get("active_module", "calendar")
            
            # Mostra a tela principal
            self.show_main_screen(active_module)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inicializar aplicativo: {e}")
            self.root.quit()
    
    def register_modules(self):
        """Registra todos os módulos disponíveis no router"""
        # Importa os controladores dos módulos
        from app.modules.calendar.controller.calendar_controller import CalendarController
        from app.modules.notes.controller import NotesController
        from app.modules.daily.controller import DailyController
        from app.modules.finance.controller import FinanceController
        from app.modules.setting.controller import SettingController
        
        # Registra cada módulo com seu controlador
        self.router.register_module("calendar", {
            "name": "Calendário",
            "icon": "📅",
            "color": self.colors["calendar"],
            "controller": CalendarController(self.storage_service)
        })
        
        self.router.register_module("notes", {
            "name": "Notas",
            "icon": "📝",
            "color": self.colors["notes"],
            "controller": NotesController(self.storage_service)
        })
        
        self.router.register_module("daily", {
            "name": "Diário",
            "icon": "📖",
            "color": self.colors["daily"],
            "controller": DailyController(self.storage_service)
        })
        
        self.router.register_module("finance", {
            "name": "Finanças",
            "icon": "💰",
            "color": self.colors["finance"],
            "controller": FinanceController(self.storage_service)
        })
        
        self.router.register_module("setting", {
            "name": "Configurações",
            "icon": "⚙️",
            "color": self.colors["setting"],
            "controller": SettingController(self.storage_service)
        })
    
    def show_main_screen(self, active_module: str):
        """Exibe a tela principal do aplicativo"""
        if self.current_screen:
            self.current_screen.destroy()
        
        # Cria e exibe a tela principal
        self.current_screen = MainScreen(
            self.root,
            self.router,
            self.storage_service,
            active_module,
            self.colors
        )
        self.current_screen.pack(fill=tk.BOTH, expand=True)
        
        # Atualiza o título da janela
        module_name = self.router.get_module_info(active_module)["name"]
        self.root.title(f"MeuCantinho - {module_name}")
    
    def shutdown(self):
        """Finaliza o aplicativo"""
        try:
            # Salva configurações
            if hasattr(self, 'config'):
                self.storage_service.save_config(self.config)
            
            # Fecha a janela
            if self.root:
                self.root.quit()
                
        except Exception as e:
            print(f"Erro ao finalizar aplicativo: {e}")
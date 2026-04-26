"""
Tela principal do módulo de calendário
"""

import tkinter as tk
from tkinter import ttk
from app.modules.calendar.controller.calendar_controller import CalendarController
from app.modules.calendar.view.calendar_views import MonthView, WeekView, ListView
from app.modules.calendar.view.event_dialog import EventDialog


class CalendarView(ttk.Frame):
    """Tela principal do calendário"""
    
    def __init__(self, parent, controller: CalendarController, on_module_change=None):
        super().__init__(parent)
        self.controller = controller
        self.on_module_change = on_module_change
        
        self.current_view_frame = None
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        """Configura a interface do calendário"""
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra de ferramentas
        toolbar = self.create_toolbar(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para o conteúdo da visualização
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_toolbar(self, parent):
        """Cria a barra de ferramentas"""
        toolbar = ttk.Frame(parent)
        
        # Botões de navegação
        ttk.Button(toolbar, text="◀", width=3, 
                  command=self.previous).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Hoje", width=8,
                  command=self.today).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="▶", width=3,
                  command=self.next).pack(side=tk.LEFT, padx=2)
        
        # Label do período atual
        self.period_label = ttk.Label(toolbar, font=("Segoe UI", 14, "bold"))
        self.period_label.pack(side=tk.LEFT, padx=20)
        
        # Separador
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        # Botões de visualização
        self.view_var = tk.StringVar(value="month")
        views = [("📅 Mês", "month"), ("📆 Semana", "week"), ("📋 Lista", "list")]
        
        for text, value in views:
            ttk.Radiobutton(toolbar, text=text, value=value,
                           variable=self.view_var,
                           command=self.change_view).pack(side=tk.LEFT, padx=5)
        
        # Separador
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        # Botão Novo Evento
        ttk.Button(toolbar, text="+ Novo Evento", 
                  command=self.new_event).pack(side=tk.LEFT, padx=5)
        
        # Botão de voltar (se houver callback de módulo)
        if self.on_module_change:
            ttk.Button(toolbar, text="← Voltar", 
                      command=lambda: self.on_module_change("menu")).pack(side=tk.RIGHT, padx=5)
        
        return toolbar
    
    def change_view(self):
        """Muda a visualização atual"""
        view = self.view_var.get()
        self.controller.set_view(view)
        self.refresh()
    
    def previous(self):
        """Volta período anterior"""
        self.controller.previous_period()
        self.refresh()
    
    def next(self):
        """Avança período"""
        self.controller.next_period()
        self.refresh()
    
    def today(self):
        """Volta para hoje"""
        self.controller.go_to_today()
        self.refresh()
    
    def new_event(self):
        """Abre diálogo para criar novo evento"""
        dialog = EventDialog(self.winfo_toplevel(), self.controller)
        self.wait_window(dialog)
        self.refresh()
    
    def edit_event(self, event):
        """Abre diálogo para editar evento"""
        dialog = EventDialog(self.winfo_toplevel(), self.controller, event)
        self.wait_window(dialog)
        self.refresh()
    
    def refresh(self):
        """Atualiza a visualização atual"""
        # Limpa o frame de conteúdo
        if self.current_view_frame:
            self.current_view_frame.destroy()
        
        # Atualiza label do período
        if self.controller.current_view == "month":
            self.period_label.config(text=self.controller.get_month_name())
        elif self.controller.current_view == "week":
            self.period_label.config(text=self.controller.get_week_range())
        else:
            self.period_label.config(text="Próximos Eventos")
        
        # Cria a visualização apropriada
        if self.controller.current_view == "month":
            self.current_view_frame = MonthView(self.content_frame, self.controller, self)
        elif self.controller.current_view == "week":
            self.current_view_frame = WeekView(self.content_frame, self.controller, self)
        else:
            self.current_view_frame = ListView(self.content_frame, self.controller, self)
        
        self.current_view_frame.pack(fill=tk.BOTH, expand=True)
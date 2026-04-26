"""
Componentes de UI para eventos: Cards e Células de dia
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class DayCell(ttk.Frame):
    """Célula de dia na visualização mensal"""
    
    def __init__(self, parent, date, events, is_current_month, app):
        super().__init__(parent, relief="solid", borderwidth=1)
        self.date = date
        self.events = events
        self.is_current_month = is_current_month
        self.app = app
        
        self.setup_ui()
        self.display_events()
    
    def setup_ui(self):
        """Configura a célula do dia"""
        # Configurar cor de fundo
        if not self.is_current_month:
            self.configure(style="OtherMonth.TFrame")
        
        # Frame para o cabeçalho
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=3, pady=2)
        
        # Dia do mês
        day_number = self.date.day
        
        # Destacar dia atual
        is_today = self.date == datetime.now().date()
        if is_today:
            day_label = tk.Label(header_frame, text=str(day_number), 
                                font=("Segoe UI", 10, "bold"),
                                bg="#3498db", fg="white", width=3)
            day_label.pack(side=tk.LEFT)
        else:
            day_label = ttk.Label(header_frame, text=str(day_number), 
                                 font=("Segoe UI", 10, "bold"))
            day_label.pack(side=tk.LEFT)
        
        # Frame para eventos
        self.events_frame = ttk.Frame(self)
        self.events_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Bind para adicionar evento ao clicar
        self.bind("<Double-Button-1>", lambda e: self.open_new_event_dialog())
        header_frame.bind("<Double-Button-1>", lambda e: self.open_new_event_dialog())
        day_label.bind("<Double-Button-1>", lambda e: self.open_new_event_dialog())
    
    def display_events(self):
        """Exibe os eventos do dia"""
        # Limpar eventos existentes
        for widget in self.events_frame.winfo_children():
            widget.destroy()
        
        # Mostrar apenas os 3 primeiros eventos
        for event in self.events[:3]:
            event_card = EventCard(self.events_frame, event, self.app, compact=True)
            event_card.pack(fill=tk.X, pady=1)
        
        # Indicador de mais eventos
        if len(self.events) > 3:
            more_label = ttk.Label(self.events_frame, 
                                  text=f"+{len(self.events)-3} mais...",
                                  font=("Segoe UI", 8),
                                  foreground="#7f8c8d")
            more_label.pack()
            more_label.bind("<Button-1>", lambda e: self.open_new_event_dialog())
    
    def open_new_event_dialog(self):
        """Abre diálogo para criar evento nesta data"""
        from app.modules.calendar.view.event_dialog import EventDialog
        dialog = EventDialog(self.winfo_toplevel(), self.app.controller, date=self.date)
        self.winfo_toplevel().wait_window(dialog)
        self.app.refresh()


class EventCard(ttk.Frame):
    """Card de evento para exibição"""
    
    def __init__(self, parent, event, app, compact=False):
        super().__init__(parent)
        self.event = event
        self.app = app
        self.compact = compact
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura o card do evento"""
        if not self.compact:
            # Card detalhado
            # Criar estilo com a cor do evento
            style = ttk.Style()
            style_name = f"Event{self.event.id.replace('-', '')}.TFrame"
            style.configure(style_name, background=self.event.color)
            self.configure(style=style_name)
            
            # Frame interno
            inner_frame = ttk.Frame(self)
            inner_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Título
            title_label = ttk.Label(inner_frame, text=self.event.title, 
                                   font=("Segoe UI", 10, "bold"),
                                   background=self.event.color,
                                   foreground="white")
            title_label.pack(anchor=tk.W)
            
            # Horário
            time_label = ttk.Label(inner_frame, text=self.event.time_display,
                                  font=("Segoe UI", 8),
                                  background=self.event.color,
                                  foreground="white")
            time_label.pack(anchor=tk.W)
            
            # Descrição (se houver)
            if self.event.description:
                desc = self.event.description[:50] + "..." if len(self.event.description) > 50 else self.event.description
                desc_label = ttk.Label(inner_frame, text=desc,
                                      font=("Segoe UI", 8),
                                      background=self.event.color,
                                      foreground="#ecf0f1")
                desc_label.pack(anchor=tk.W, pady=(2, 0))
            
            # Botão de editar
            edit_btn = tk.Button(self, text="✎", width=2, height=1,
                                bg=self.event.color, fg="white",
                                relief="flat", cursor="hand2",
                                command=lambda: self.app.edit_event(self.event))
            edit_btn.place(x=self.winfo_width() - 30, y=5)
            
            # Bind para redesenhar quando redimensionar
            def on_resize(event):
                edit_btn.place(x=event.width - 30, y=5)
            
            self.bind("<Configure>", on_resize)
            
            # Bind para editar ao clicar (exceto no botão)
            self.bind("<Button-1>", lambda e: self.app.edit_event(self.event))
            title_label.bind("<Button-1>", lambda e: self.app.edit_event(self.event))
            time_label.bind("<Button-1>", lambda e: self.app.edit_event(self.event))
            
        else:
            # Card compacto (para visualização mês)
            # Criar estilo com a cor do evento
            style = ttk.Style()
            style_name = f"EventCompact{self.event.id.replace('-', '')}.TFrame"
            style.configure(style_name, background=self.event.color)
            self.configure(style=style_name)
            
            # Título resumido
            title = self.event.title[:12] + "..." if len(self.event.title) > 12 else self.event.title
            title_label = ttk.Label(self, text=title,
                                   font=("Segoe UI", 8),
                                   background=self.event.color,
                                   foreground="white")
            title_label.pack(fill=tk.BOTH, expand=True, padx=3, pady=2)
            
            # Bind para editar ao clicar
            title_label.bind("<Button-1>", lambda e: self.app.edit_event(self.event))
            self.bind("<Button-1>", lambda e: self.app.edit_event(self.event))
"""
Visualizações do calendário: Mês, Semana e Lista
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from app.modules.calendar.view.event_ui import DayCell, EventCard


class MonthView(ttk.Frame):
    """Visualização de mês"""
    
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.controller = controller
        self.app = app
        self.setup_ui()
        self.display_month()
    
    def setup_ui(self):
        """Configura estrutura da visualização mês"""
        # Dias da semana
        weekdays = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        for col, day in enumerate(weekdays):
            label = ttk.Label(self, text=day, font=("Segoe UI", 10, "bold"))
            label.grid(row=0, column=col, padx=2, pady=5, sticky="nsew")
        
        # Configurar grid
        for i in range(7):
            self.columnconfigure(i, weight=1)
        
        self.cells = []
    
    def display_month(self):
        """Exibe os dias do mês"""
        month_days = self.controller.get_month_days()
        current_month = self.controller.current_date.month
        
        for i, day_date in enumerate(month_days):
            row = (i // 7) + 1
            col = i % 7
            
            # Determinar se é do mês atual
            is_current_month = (day_date.month == current_month)
            
            # Obter eventos do dia
            events = self.controller.get_events_for_date(day_date)
            
            # Criar célula do dia
            cell = DayCell(self, day_date, events, is_current_month, self.app)
            cell.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            # Configurar peso da linha
            self.rowconfigure(row, weight=1)
            
            self.cells.append(cell)


class WeekView(ttk.Frame):
    """Visualização de semana"""
    
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.controller = controller
        self.app = app
        self.setup_ui()
        self.display_week()
    
    def setup_ui(self):
        """Configura estrutura da visualização semana"""
        # Criar canvas com scroll para dias muito cheios
        self.canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_width())
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Atualizar largura quando a janela redimensionar
        def configure_canvas(event):
            self.canvas.itemconfig(1, width=event.width)
        
        self.canvas.bind('<Configure>', configure_canvas)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.days_frame = ttk.Frame(self.scrollable_frame)
        self.days_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def display_week(self):
        """Exibe os dias da semana"""
        week_days = self.controller.get_week_days()
        
        # Configurar grid
        for col in range(7):
            self.days_frame.columnconfigure(col, weight=1)
        
        for col, day_date in enumerate(week_days):
            # Frame para o dia
            day_frame = ttk.Frame(self.days_frame, relief="solid", borderwidth=1)
            day_frame.grid(row=0, column=col, padx=3, pady=3, sticky="nsew")
            
            # Cabeçalho do dia
            is_today = day_date == datetime.now().date()
            bg_color = "#e3f2fd" if is_today else ""
            
            header_frame = ttk.Frame(day_frame)
            header_frame.pack(fill=tk.X, pady=5)
            
            weekday_label = ttk.Label(header_frame, 
                                      text=day_date.strftime("%A"),
                                      font=("Segoe UI", 10, "bold"))
            weekday_label.pack()
            
            day_label = ttk.Label(header_frame,
                                 text=day_date.strftime("%d/%m"),
                                 font=("Segoe UI", 9))
            day_label.pack()
            
            ttk.Separator(day_frame, orient="horizontal").pack(fill=tk.X, padx=5, pady=5)
            
            # Frame para eventos (com scroll interno)
            events_canvas = tk.Canvas(day_frame, height=400, highlightthickness=0)
            events_scrollbar = ttk.Scrollbar(day_frame, orient="vertical", command=events_canvas.yview)
            events_frame = ttk.Frame(events_canvas)
            
            events_frame.bind(
                "<Configure>",
                lambda e, c=events_canvas: c.configure(scrollregion=c.bbox("all"))
            )
            
            events_canvas.create_window((0, 0), window=events_frame, anchor="nw", width=events_canvas.winfo_width())
            events_canvas.configure(yscrollcommand=events_scrollbar.set)
            
            # Eventos do dia
            events = self.controller.get_events_for_date(day_date)
            for event in events:
                event_card = EventCard(events_frame, event, self.app)
                event_card.pack(pady=2, padx=5, fill=tk.X)
            
            # Botão adicionar evento
            ttk.Button(day_frame, text="+ Adicionar", 
                      command=lambda d=day_date: self.open_new_event_dialog(d)).pack(pady=5)
            
            events_canvas.pack(side="left", fill="both", expand=True, padx=5)
            events_scrollbar.pack(side="right", fill="y")
    
    def open_new_event_dialog(self, date):
        """Abre diálogo para criar evento na data específica"""
        from app.modules.calendar.view.event_dialog import EventDialog
        dialog = EventDialog(self.winfo_toplevel(), self.controller, date=date)
        self.winfo_toplevel().wait_window(dialog)
        self.app.refresh()


class ListView(ttk.Frame):
    """Visualização de lista"""
    
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.controller = controller
        self.app = app
        self.setup_ui()
        self.display_list()
    
    def setup_ui(self):
        """Configura estrutura da visualização lista"""
        # Treeview para lista de eventos
        columns = ("Data", "Horário", "Título", "Descrição")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)
        
        # Configurar colunas
        self.tree.heading("Data", text="Data")
        self.tree.heading("Horário", text="Horário")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Descrição", text="Descrição")
        
        self.tree.column("Data", width=100)
        self.tree.column("Horário", width=100)
        self.tree.column("Título", width=200)
        self.tree.column("Descrição", width=400)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind duplo clique para editar
        self.tree.bind("<Double-Button-1>", self.on_double_click)
        
        # Bind para seleção
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Frame de botões
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="✎ Editar", command=self.edit_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑 Excluir", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="+ Novo Evento", command=self.app.new_event).pack(side=tk.RIGHT, padx=5)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.selected_event_id = None
    
    def display_list(self):
        """Exibe lista de eventos"""
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ordenar eventos por data
        events = sorted(self.controller.get_all_events(), key=lambda e: e.date)
        
        # Filtrar apenas eventos futuros ou recentes (últimos 30 dias)
        hoje = datetime.now().date()
        events = [e for e in events if e.date.date() >= hoje - timedelta(days=30)]
        
        for event in events:
            # Formatar data e hora
            date_str = event.date.strftime("%d/%m/%Y")
            time_str = event.time_display
            
            self.tree.insert("", "end", values=(
                date_str, time_str, event.title, event.description[:50]
            ), tags=(event.id,))
            
            # Colorir linha baseada na data
            if event.date.date() < hoje:
                self.tree.tag_configure(event.id, background='#ffe6e6')
            elif event.date.date() == hoje:
                self.tree.tag_configure(event.id, background='#e6f3ff')
    
    def on_select(self, event):
        """Quando um item é selecionado"""
        selection = self.tree.selection()
        if selection:
            tags = self.tree.item(selection[0], "tags")
            if tags:
                self.selected_event_id = tags[0]
    
    def on_double_click(self, event):
        """Abre evento para edição ao dar duplo clique"""
        self.edit_selected()
    
    def edit_selected(self):
        """Edita o evento selecionado"""
        if self.selected_event_id:
            event = self.controller.get_event_by_id(self.selected_event_id)
            if event:
                self.app.edit_event(event)
    
    def delete_selected(self):
        """Exclui o evento selecionado"""
        if self.selected_event_id:
            from tkinter import messagebox
            if messagebox.askyesno("Confirmar", "Deseja excluir este evento?"):
                self.controller.delete_event(self.selected_event_id)
                self.display_list()
                self.selected_event_id = None
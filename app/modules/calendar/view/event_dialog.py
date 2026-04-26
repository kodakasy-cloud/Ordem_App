"""
Diálogo para criar e editar eventos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class EventDialog(tk.Toplevel):
    """Diálogo para criação/edição de eventos"""
    
    def __init__(self, parent, controller, event=None, date=None):
        super().__init__(parent)
        self.controller = controller
        self.event = event
        self.default_date = date
        
        self.title("Editar Evento" if event else "Novo Evento")
        self.geometry("550x500")
        self.resizable(False, False)
        
        # Tornar modal
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        
        if event:
            self.load_event_data()
        elif date:
            self.set_default_date(date)
        
        # Centralizar na tela
        self.center_window()
    
    def setup_ui(self):
        """Configura os campos do formulário"""
        # Frame principal com scroll
        main_canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=main_canvas.yview)
        main_frame = ttk.Frame(main_canvas)
        
        main_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar grid do main_frame
        main_frame.columnconfigure(1, weight=1)
        
        # Padding interno
        padding_frame = ttk.Frame(main_frame, padding="20")
        padding_frame.pack(fill="both", expand=True)
        
        # Título
        ttk.Label(padding_frame, text="Título:", font=("Segoe UI", 10, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 5))
        self.title_entry = ttk.Entry(padding_frame, width=40, font=("Segoe UI", 10))
        self.title_entry.grid(row=0, column=1, sticky="ew", pady=(0, 15))
        
        # Data
        ttk.Label(padding_frame, text="Data:", font=("Segoe UI", 10, "bold")).grid(
            row=1, column=0, sticky="w", pady=(0, 5))
        
        # Frame para widgets de data
        date_frame = ttk.Frame(padding_frame)
        date_frame.grid(row=1, column=1, sticky="w", pady=(0, 15))
        
        self.day_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        
        # Valores padrão
        now = datetime.now()
        self.day_var.set(str(now.day))
        self.month_var.set(str(now.month))
        self.year_var.set(str(now.year))
        
        ttk.Spinbox(date_frame, from_=1, to=31, width=5, textvariable=self.day_var,
                   font=("Segoe UI", 10)).pack(side="left", padx=2)
        ttk.Label(date_frame, text="/", font=("Segoe UI", 10)).pack(side="left")
        ttk.Spinbox(date_frame, from_=1, to=12, width=5, textvariable=self.month_var,
                   font=("Segoe UI", 10)).pack(side="left", padx=2)
        ttk.Label(date_frame, text="/", font=("Segoe UI", 10)).pack(side="left")
        ttk.Spinbox(date_frame, from_=2000, to=2030, width=7, textvariable=self.year_var,
                   font=("Segoe UI", 10)).pack(side="left", padx=2)
        
        # Horário
        ttk.Label(padding_frame, text="Horário:", font=("Segoe UI", 10, "bold")).grid(
            row=2, column=0, sticky="nw", pady=(0, 5))
        
        time_frame = ttk.Frame(padding_frame)
        time_frame.grid(row=2, column=1, sticky="w", pady=(0, 15))
        
        self.has_time = tk.BooleanVar(value=True)
        ttk.Checkbutton(time_frame, text="Definir horário", 
                       variable=self.has_time,
                       command=self.toggle_time).pack(anchor="w")
        
        # Horário de início
        self.start_frame = ttk.Frame(time_frame)
        self.start_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Label(self.start_frame, text="Início:", font=("Segoe UI", 10)).pack(side="left", padx=(20, 5))
        self.start_hour = ttk.Spinbox(self.start_frame, from_=0, to=23, width=3, 
                                      format="%02.0f", font=("Segoe UI", 10))
        self.start_hour.pack(side="left")
        ttk.Label(self.start_frame, text=":", font=("Segoe UI", 10)).pack(side="left")
        self.start_minute = ttk.Spinbox(self.start_frame, from_=0, to=59, width=3,
                                        format="%02.0f", font=("Segoe UI", 10))
        self.start_minute.pack(side="left")
        
        # Horário de fim
        self.end_frame = ttk.Frame(time_frame)
        self.end_frame.pack(fill="x", pady=(5, 0))
        
        ttk.Label(self.end_frame, text="Término:", font=("Segoe UI", 10)).pack(side="left", padx=(20, 5))
        self.end_hour = ttk.Spinbox(self.end_frame, from_=0, to=23, width=3,
                                    format="%02.0f", font=("Segoe UI", 10))
        self.end_hour.pack(side="left")
        ttk.Label(self.end_frame, text=":", font=("Segoe UI", 10)).pack(side="left")
        self.end_minute = ttk.Spinbox(self.end_frame, from_=0, to=59, width=3,
                                      format="%02.0f", font=("Segoe UI", 10))
        self.end_minute.pack(side="left")
        
        # Descrição
        ttk.Label(padding_frame, text="Descrição:", font=("Segoe UI", 10, "bold")).grid(
            row=3, column=0, sticky="nw", pady=(0, 5))
        
        self.description_text = tk.Text(padding_frame, height=5, width=40,
                                       font=("Segoe UI", 10), wrap=tk.WORD)
        self.description_text.grid(row=3, column=1, sticky="ew", pady=(0, 15))
        
        # Scrollbar para descrição
        scrollbar_text = ttk.Scrollbar(padding_frame, orient="vertical", 
                                      command=self.description_text.yview)
        scrollbar_text.grid(row=3, column=2, sticky="nsew", pady=(0, 15))
        self.description_text.configure(yscrollcommand=scrollbar_text.set)
        
        # Cor
        ttk.Label(padding_frame, text="Cor:", font=("Segoe UI", 10, "bold")).grid(
            row=4, column=0, sticky="w", pady=(0, 5))
        
        self.color_var = tk.StringVar(value="#3498db")
        colors = [
            ("#3498db", "Azul"), ("#e74c3c", "Vermelho"), 
            ("#2ecc71", "Verde"), ("#f39c12", "Laranja"),
            ("#9b59b6", "Roxo"), ("#1abc9c", "Turquesa"),
            ("#e67e22", "Laranja escuro"), ("#95a5a6", "Cinza")
        ]
        
        color_frame = ttk.Frame(padding_frame)
        color_frame.grid(row=4, column=1, sticky="w", pady=(0, 20))
        
        for i, (color, name) in enumerate(colors):
            col = i % 4
            row = i // 4
            
            rb = ttk.Radiobutton(color_frame, text="", value=color,
                                variable=self.color_var)
            rb.grid(row=row, column=col*2, padx=2, pady=2)
            
            # Criar label colorida
            color_label = tk.Label(color_frame, bg=color, width=4, height=1,
                                  relief="ridge", borderwidth=1)
            color_label.grid(row=row, column=col*2+1, padx=(0, 10))
            
            # Tooltip com nome da cor
            self.create_tooltip(color_label, name)
        
        # Botões
        button_frame = ttk.Frame(padding_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Salvar", command=self.save_event,
                  width=15).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.destroy,
                  width=15).pack(side="left", padx=5)
        
        if self.event:
            ttk.Button(button_frame, text="Excluir", command=self.delete_event,
                      width=15).pack(side="right", padx=5)
    
    def create_tooltip(self, widget, text):
        """Cria um tooltip simples"""
        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, background="#ffffe0", 
                             relief="solid", borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind("<Leave>", lambda e: hide_tooltip())
        
        widget.bind("<Enter>", show_tooltip)
    
    def toggle_time(self):
        """Habilita/desabilita campos de horário"""
        state = "normal" if self.has_time.get() else "disabled"
        for widget in [self.start_hour, self.start_minute, self.end_hour, self.end_minute]:
            widget.config(state=state)
    
    def set_default_date(self, date):
        """Define a data padrão no diálogo"""
        if date:
            if isinstance(date, datetime):
                self.day_var.set(str(date.day))
                self.month_var.set(str(date.month))
                self.year_var.set(str(date.year))
            elif isinstance(date, date):
                self.day_var.set(str(date.day))
                self.month_var.set(str(date.month))
                self.year_var.set(str(date.year))
    
    def load_event_data(self):
        """Carrega dados do evento para edição"""
        self.title_entry.insert(0, self.event.title)
        
        # Carregar data
        self.day_var.set(str(self.event.date.day))
        self.month_var.set(str(self.event.date.month))
        self.year_var.set(str(self.event.date.year))
        
        # Carregar horário
        if self.event.start_time:
            self.has_time.set(True)
            self.start_hour.set(self.event.start_time.strftime("%H"))
            self.start_minute.set(self.event.start_time.strftime("%M"))
            
            if self.event.end_time:
                self.end_hour.set(self.event.end_time.strftime("%H"))
                self.end_minute.set(self.event.end_time.strftime("%M"))
        else:
            self.has_time.set(False)
            self.toggle_time()
        
        # Carregar descrição
        self.description_text.insert("1.0", self.event.description)
        
        # Carregar cor
        self.color_var.set(self.event.color)
    
    def save_event(self):
        """Salva o evento (cria ou atualiza)"""
        # Validar título
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Erro", "O título é obrigatório!")
            return
        
        # Validar data
        try:
            event_date = datetime(int(self.year_var.get()), 
                                 int(self.month_var.get()),
                                 int(self.day_var.get()))
        except ValueError:
            messagebox.showerror("Erro", "Data inválida!")
            return
        
        # Validar horário
        start_time = None
        end_time = None
        
        if self.has_time.get():
            try:
                start_hour = int(self.start_hour.get())
                start_minute = int(self.start_minute.get())
                start_time = f"{start_hour:02d}:{start_minute:02d}:00"
                start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
                
                end_hour = int(self.end_hour.get())
                end_minute = int(self.end_minute.get())
                end_time = f"{end_hour:02d}:{end_minute:02d}:00"
                end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()
                
                if start_time_obj >= end_time_obj:
                    messagebox.showerror("Erro", "Horário de término deve ser após o início!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Horário inválido!")
                return
        
        description = self.description_text.get("1.0", "end-1c").strip()
        color = self.color_var.get()
        
        # Verificar conflito
        if self.controller.has_conflict(event_date, start_time, end_time, 
                                        exclude_id=self.event.id if self.event else None):
            messagebox.showerror("Erro", "Conflito de horário! Já existe um evento neste horário.")
            return
        
        # Salvar evento
        if self.event:
            # Editar evento existente
            success = self.controller.edit_event(
                self.event.id, title, event_date,
                start_time, end_time, description, color
            )
        else:
            # Criar novo evento
            event = self.controller.add_event(
                title, event_date, start_time, end_time, description, color
            )
            success = event is not None
        
        if success:
            self.destroy()
        else:
            messagebox.showerror("Erro", "Erro ao salvar evento!")
    
    def delete_event(self):
        """Exclui o evento"""
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este evento?"):
            if self.controller.delete_event(self.event.id):
                self.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao excluir evento!")
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

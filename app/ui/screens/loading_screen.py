"""
Tela de carregamento do aplicativo
"""

import tkinter as tk
from tkinter import ttk


class LoadingScreen(ttk.Frame):
    """Tela de carregamento com animação"""
    
    def __init__(self, parent, colors: dict):
        super().__init__(parent)
        self.parent = parent
        self.colors = colors
        self.progress = 0
        
        self.setup_ui()
        self.animate_loading()
    
    def setup_ui(self):
        """Configura a interface da tela de loading"""
        # Frame central
        center_frame = ttk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        title_label = ttk.Label(
            center_frame,
            text="MeuCantinho",
            font=("Segoe UI", 36, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = ttk.Label(
            center_frame,
            text="Seu Espaço Pessoal",
            font=("Segoe UI", 14),
            foreground="#7f8c8d"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Progressbar
        self.progress_bar = ttk.Progressbar(
            center_frame,
            mode="determinate",
            length=400,
            style="Loading.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=20)
        
        # Label de status
        self.status_label = ttk.Label(
            center_frame,
            text="Inicializando...",
            font=("Segoe UI", 10),
            foreground="#95a5a6"
        )
        self.status_label.pack()
        
        # Frame de módulos (animação dos ícones)
        modules_frame = ttk.Frame(center_frame)
        modules_frame.pack(pady=30)
        
        modules = [
            ("📅", "Calendário", self.colors["calendar"]),
            ("📝", "Notas", self.colors["notes"]),
            ("📖", "Diário", self.colors["daily"]),
            ("💰", "Finanças", self.colors["finance"]),
            ("⚙️", "Configurações", self.colors["setting"])
        ]
        
        self.module_labels = []
        for icon, name, color in modules:
            module_frame = ttk.Frame(modules_frame)
            module_frame.pack(side=tk.LEFT, padx=15)
            
            icon_label = ttk.Label(
                module_frame,
                text=icon,
                font=("Segoe UI", 24)
            )
            icon_label.pack()
            
            name_label = ttk.Label(
                module_frame,
                text=name,
                font=("Segoe UI", 10),
                foreground=color
            )
            name_label.pack()
            
            self.module_labels.append((icon_label, name))
    
    def animate_loading(self):
        """Anima a barra de progresso e atualiza o status"""
        self.progress += 2
        
        if self.progress <= 100:
            self.progress_bar["value"] = self.progress
            
            # Atualiza status baseado no progresso
            if self.progress < 20:
                status = "Carregando módulos..."
            elif self.progress < 40:
                status = "Inicializando banco de dados..."
            elif self.progress < 60:
                status = "Verificando configurações..."
            elif self.progress < 80:
                status = "Preparando interface..."
            else:
                status = "Quase lá..."
            
            self.status_label.config(text=status)
            
            # Anima ícones dos módulos
            for idx, (label, name) in enumerate(self.module_labels):
                if self.progress > (idx + 1) * 20:
                    label.config(text=["📅", "📝", "📖", "💰", "⚙️"][idx])
            
            # Continua animação
            self.after(30, self.animate_loading)
        else:
            # Loading completo
            self.status_label.config(text="Pronto!")
            self.progress_bar["value"] = 100
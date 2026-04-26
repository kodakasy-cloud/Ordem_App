"""
Componente de barra lateral do aplicativo
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class Sidebar(ttk.Frame):
    """Barra lateral com navegação entre módulos"""
    
    def __init__(self, parent, router, on_select: Callable, colors: dict):
        super().__init__(parent, style="Sidebar.TFrame")
        self.router = router
        self.on_select = on_select
        self.colors = colors
        self.buttons = {}
        
        self.setup_ui()
        self.load_modules()
    
    def setup_ui(self):
        """Configura a interface do sidebar"""
        # Logo
        logo_frame = ttk.Frame(self, style="Sidebar.TFrame")
        logo_frame.pack(fill=tk.X, pady=20)
        
        logo_label = ttk.Label(
            logo_frame,
            text="🏠 MeuCantinho",
            font=("Segoe UI", 16, "bold"),
            foreground="white",
            background="#2c3e50"
        )
        logo_label.pack(pady=10)
        
        ttk.Separator(self, orient="horizontal").pack(fill=tk.X, padx=10, pady=10)
        
        # Scrollable frame para botões
        self.canvas = tk.Canvas(self, bg="#2c3e50", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Sidebar.TFrame")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame dos botões
        self.buttons_frame = ttk.Frame(self.scrollable_frame, style="Sidebar.TFrame")
        self.buttons_frame.pack(fill=tk.X, padx=5, pady=10)
    
    def load_modules(self):
        """Carrega os botões para cada módulo"""
        modules = self.router.get_modules_list()
        
        for module in modules:
            self.add_module_button(
                module["id"],
                f"{module['icon']} {module['name']}",
                module["color"]
            )
        
        # Espaçador
        ttk.Frame(self.buttons_frame, height=20, style="Sidebar.TFrame").pack()
        
        # Botão de sair
        self.add_exit_button()
    
    def add_module_button(self, module_id: str, label: str, color: str):
        """Adiciona um botão de módulo"""
        # Frame para o botão
        btn_frame = ttk.Frame(self.buttons_frame, style="Sidebar.TFrame")
        btn_frame.pack(fill=tk.X, pady=2)
        
        # Botão estilizado
        btn = tk.Button(
            btn_frame,
            text=label,
            font=("Segoe UI", 11),
            bg="#34495e",
            fg="white",
            activebackground="#3d566e",
            activeforeground="white",
            relief="flat",
            anchor="w",
            padx=15,
            pady=10,
            cursor="hand2",
            command=lambda m=module_id: self.on_select(m)
        )
        btn.pack(fill=tk.X)
        
        # Efeito hover
        def on_enter(e):
            btn.config(bg="#3d566e")
        
        def on_leave(e):
            if self.router.get_current_module() != module_id:
                btn.config(bg="#34495e")
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        self.buttons[module_id] = btn
        
        # Barra de indicador
        indicator = tk.Frame(
            btn_frame,
            width=3,
            bg=color
        )
        indicator.place(x=0, rely=0, relheight=1)
    
    def add_exit_button(self):
        """Adiciona botão de sair"""
        btn_frame = ttk.Frame(self.buttons_frame, style="Sidebar.TFrame")
        btn_frame.pack(fill=tk.X, pady=2)
        
        exit_btn = tk.Button(
            btn_frame,
            text="🚪 Sair",
            font=("Segoe UI", 11),
            bg="#c0392b",
            fg="white",
            activebackground="#e74c3c",
            activeforeground="white",
            relief="flat",
            anchor="w",
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.exit_app
        )
        exit_btn.pack(fill=tk.X)
    
    def exit_app(self):
        """Sai do aplicativo"""
        if tk.messagebox.askyesno("Sair", "Deseja realmente sair do MeuCantinho?"):
            self.winfo_toplevel().quit()
    
    def highlight_module(self, module_id: str):
        """Destaca o módulo ativo"""
        for mid, btn in self.buttons.items():
            if mid == module_id:
                btn.config(bg="#3d566e")
            else:
                btn.config(bg="#34495e")
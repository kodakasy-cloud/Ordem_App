# One/Two/Quit.py
import tkinter as tk
from tkinter import messagebox

class QuitModule:
    def __init__(self, parent):
        self.parent = parent
    
    def abrir(self):
        """Abre o módulo de saída (confirmação)"""
        self.parent.atualizar_status("Saindo da aplicação...")
        
        # Salvar todos os dados antes de sair
        self.parent.modules['notes'].salvar_notas()
        self.parent.modules['daily'].salvar_diario()
        self.parent.modules['finance'].salvar_financas()
        self.parent.modules['setting'].salvar_config()
        
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair?\n\nTodos os dados serão salvos automaticamente."):
            self.parent.atualizar_status("Aplicação encerrada. Até logo!")
            self.parent.root.after(500, self.parent.root.destroy)
        else:
            self.parent.atualizar_status("Operação cancelada")
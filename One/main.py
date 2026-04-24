# One/main.py
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from datetime import datetime

# Importar os módulos da pasta Two
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from One.Two.Calendar import CalendarModule
from One.Two.Notes import NotesModule
from One.Two.Daily import DailyModule
from One.Two.Finance import FinanceModule
from One.Two.Setting import SettingModule
from One.Two.Quit import QuitModule

class AppDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Meu Dashboard Pessoal")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Inicializar módulos
        self.modules = {
            'calendar': CalendarModule(self),
            'notes': NotesModule(self),
            'daily': DailyModule(self),
            'finance': FinanceModule(self),
            'setting': SettingModule(self),
            'quit': QuitModule(self)
        }
        
        # Centralizar a janela
        self.centralizar_janela()
        
        # Configurar grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Criar frame principal
        self.main_frame = tk.Frame(self.root, bg='#2c3e50')
        self.main_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        
        # Configurar grid do main_frame
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        self.criar_titulo()
        
        # Botões principais
        self.criar_botoes()
        
        # Barra de status
        self.criar_status_bar()
    
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = 800
        height = 600
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def criar_titulo(self):
        """Cria o título do dashboard"""
        titulo_frame = tk.Frame(self.main_frame, bg='#2c3e50')
        titulo_frame.grid(row=0, column=0, pady=(0, 30))
        
        titulo = tk.Label(
            titulo_frame,
            text="📱 MEU DASHBOARD PESSOAL",
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        titulo.pack()
        
        subtitulo = tk.Label(
            titulo_frame,
            text="Organize sua vida com estas ferramentas:",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        subtitulo.pack(pady=(5, 0))
    
    def criar_botoes(self):
        """Cria os 6 botões principais"""
        botoes_frame = tk.Frame(self.main_frame, bg='#2c3e50')
        botoes_frame.grid(row=1, column=0, sticky='nsew')
        
        # Configurar grid (2 colunas x 3 linhas)
        for i in range(3):
            botoes_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            botoes_frame.grid_columnconfigure(i, weight=1)
        
        # Configuração dos botões
        opcoes = [
            {"texto": "📅 CALENDÁRIO\nVer e gerenciar eventos", "cor": "#e74c3c", "modulo": "calendar"},
            {"texto": "📝 ANOTAÇÕES\nSalvar notas rápidas", "cor": "#3498db", "modulo": "notes"},
            {"texto": "📔 DIÁRIO\nRegistrar seu dia", "cor": "#9b59b6", "modulo": "daily"},
            {"texto": "💰 FINANÇAS\nControlar gastos", "cor": "#2ecc71", "modulo": "finance"},
            {"texto": "⚙️ OPÇÕES\nConfigurações do app", "cor": "#f39c12", "modulo": "setting"},
            {"texto": "🚪 SAIR\nFechar aplicação", "cor": "#95a5a6", "modulo": "quit"}
        ]
        
        # Criar botões
        for idx, opcao in enumerate(opcoes):
            linha = idx // 2
            coluna = idx % 2
            
            frame_botao = tk.Frame(botoes_frame, bg='#2c3e50')
            frame_botao.grid(row=linha, column=coluna, padx=15, pady=15, sticky='nsew')
            
            btn = tk.Button(
                frame_botao,
                text=opcao["texto"],
                font=('Arial', 13, 'bold'),
                bg=opcao["cor"],
                fg='white',
                activebackground=self.escurer_cor(opcao["cor"]),
                activeforeground='white',
                relief=tk.RAISED,
                borderwidth=2,
                cursor='hand2',
                command=lambda m=opcao["modulo"]: self.abrir_modulo(m),
                height=3,
                width=22
            )
            btn.pack(fill='both', expand=True)
            
            # Efeito hover
            btn.bind("<Enter>", lambda e, b=btn, cor=opcao["cor"]: self.on_enter(b, cor))
            btn.bind("<Leave>", lambda e, b=btn, cor=opcao["cor"]: self.on_leave(b, cor))
    
    def escurer_cor(self, cor):
        """Escurece uma cor hexadecimal"""
        if cor.startswith('#'):
            r = int(cor[1:3], 16)
            g = int(cor[3:5], 16)
            b = int(cor[5:7], 16)
            r = max(0, r - 40)
            g = max(0, g - 40)
            b = max(0, b - 40)
            return f'#{r:02x}{g:02x}{b:02x}'
        return cor
    
    def on_enter(self, botao, cor_original):
        """Efeito ao passar o mouse"""
        botao.configure(bg=self.escurer_cor(cor_original))
    
    def on_leave(self, botao, cor_original):
        """Efeito ao remover o mouse"""
        botao.configure(bg=cor_original)
    
    def criar_status_bar(self):
        """Cria a barra de status"""
        self.status_frame = tk.Frame(self.main_frame, bg='#34495e', height=40)
        self.status_frame.grid(row=2, column=0, sticky='ew', pady=(20, 0))
        self.status_frame.grid_propagate(False)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="✅ Bem-vindo! Escolha uma opção",
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.status_label.pack(side='left', padx=10, pady=10)
        
        self.clock_label = tk.Label(
            self.status_frame,
            font=('Arial', 10),
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.clock_label.pack(side='right', padx=10, pady=10)
        self.atualizar_relogio()
    
    def atualizar_relogio(self):
        """Atualiza o relógio"""
        agora = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        self.clock_label.config(text=agora)
        self.root.after(1000, self.atualizar_relogio)
    
    def atualizar_status(self, mensagem):
        """Atualiza a mensagem de status"""
        self.status_label.config(text=f"📌 {mensagem}")
    
    def abrir_modulo(self, modulo_nome):
        """Abre o módulo selecionado"""
        if modulo_nome in self.modules:
            self.modules[modulo_nome].abrir()

def main():
    """Função principal"""
    root = tk.Tk()
    app = AppDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
# One/Two/Setting.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import shutil
from pathlib import Path

class SettingModule:
    def __init__(self, parent):
        self.parent = parent
        self.janela = None
        self.dados_dir = Path.home() / "MeuDashboard"
        self.dados_dir.mkdir(exist_ok=True)
        self.config_file = self.dados_dir / "config.json"
        self.carregar_config()
    
    def carregar_config(self):
        """Carrega as configurações"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    "tema": "Claro",
                    "backup_auto": True,
                    "notificacoes": True
                }
        except Exception:
            self.config = {"tema": "Claro", "backup_auto": True, "notificacoes": True}
    
    def salvar_config(self):
        """Salva as configurações"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")
    
    def abrir(self):
        """Abre o módulo de configurações"""
        if self.janela and self.janela.winfo_exists():
            self.janela.lift()
            return
        
        self.parent.atualizar_status("Abrindo Configurações...")
        
        self.janela = tk.Toplevel(self.parent.root)
        self.janela.title("⚙️ Configurações")
        self.janela.geometry("500x500")
        self.janela.configure(bg='#ecf0f1')
        
        frame = tk.Frame(self.janela, bg='#ecf0f1', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="⚙️ Configurações do Sistema", font=('Arial', 16, 'bold'),
                bg='#ecf0f1').pack(pady=10)
        
        # Opções
        opcoes_frame = tk.LabelFrame(frame, text="Preferências", bg='#ecf0f1', font=('Arial', 12, 'bold'))
        opcoes_frame.pack(fill='x', pady=10)
        
        # Tema
        tk.Label(opcoes_frame, text="Tema:", bg='#ecf0f1', font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.tema_var = tk.StringVar(value=self.config.get("tema", "Claro"))
        tema_combo = ttk.Combobox(opcoes_frame, textvariable=self.tema_var, values=["Claro", "Escuro"], width=15)
        tema_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Backup automático
        self.backup_var = tk.BooleanVar(value=self.config.get("backup_auto", True))
        tk.Checkbutton(opcoes_frame, text="Fazer backup automático", variable=self.backup_var,
                      bg='#ecf0f1', font=('Arial', 10)).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='w')
        
        # Notificações
        self.notif_var = tk.BooleanVar(value=self.config.get("notificacoes", True))
        tk.Checkbutton(opcoes_frame, text="Mostrar notificações", variable=self.notif_var,
                      bg='#ecf0f1', font=('Arial', 10)).grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='w')
        
        # Local dos dados
        local_frame = tk.LabelFrame(frame, text="Dados", bg='#ecf0f1', font=('Arial', 12, 'bold'))
        local_frame.pack(fill='x', pady=10)
        
        tk.Label(local_frame, text=f"Local dos dados:\n{self.dados_dir}", 
                bg='#ecf0f1', font=('Arial', 9), justify='left').pack(pady=10, padx=10)
        
        # Botões
        btn_frame = tk.Frame(frame, bg='#ecf0f1')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="💾 Salvar Configurações", command=self.salvar_configuracoes,
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Limpar Todos os Dados", command=self.limpar_dados,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="📦 Fazer Backup", command=self.fazer_backup,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Fechar", command=self.fechar,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    
    def salvar_configuracoes(self):
        """Salva as configurações"""
        self.config['tema'] = self.tema_var.get()
        self.config['backup_auto'] = self.backup_var.get()
        self.config['notificacoes'] = self.notif_var.get()
        self.salvar_config()
        self.parent.atualizar_status("Configurações salvas!")
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        self.fechar()
    
    def limpar_dados(self):
        """Limpa todos os dados do usuário"""
        if messagebox.askyesno("Confirmar", "Tem certeza? Isso apagará TODOS os seus dados!\n\nDeseja continuar?"):
            # Limpar arquivos de dados
            for arquivo in self.dados_dir.glob("*.json"):
                if arquivo.name != "config.json":
                    arquivo.unlink()
            self.parent.modules['notes'].notas = []
            self.parent.modules['daily'].diario = {}
            self.parent.modules['finance'].financas = {"receitas": [], "despesas": []}
            self.parent.atualizar_status("Todos os dados foram limpos!")
            messagebox.showinfo("Sucesso", "Dados limpos com sucesso!")
            self.fechar()
    
    def fazer_backup(self):
        """Faz backup dos dados"""
        backup_dir = self.dados_dir / "backup"
        backup_dir.mkdir(exist_ok=True)
        
        data_backup = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_destino = backup_dir / f"backup_{data_backup}"
        backup_destino.mkdir()
        
        for arquivo in self.dados_dir.glob("*.json"):
            shutil.copy2(arquivo, backup_destino / arquivo.name)
        
        self.parent.atualizar_status(f"Backup criado em {backup_destino}")
        messagebox.showinfo("Backup", f"Backup criado com sucesso!\nLocal: {backup_destino}")
    
    def fechar(self):
        """Fecha a janela"""
        if self.janela:
            self.janela.destroy()
            self.janela = None

from datetime import datetime
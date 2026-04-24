# One/Two/Daily.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
from datetime import datetime
from pathlib import Path

class DailyModule:
    def __init__(self, parent):
        self.parent = parent
        self.janela = None
        self.dados_dir = Path.home() / "MeuDashboard"
        self.dados_dir.mkdir(exist_ok=True)
        self.arquivo_diario = self.dados_dir / "diario.json"
        self.carregar_diario()
    
    def carregar_diario(self):
        """Carrega o diário do arquivo"""
        try:
            if self.arquivo_diario.exists():
                with open(self.arquivo_diario, 'r', encoding='utf-8') as f:
                    self.diario = json.load(f)
            else:
                self.diario = {}
        except Exception:
            self.diario = {}
    
    def salvar_diario(self):
        """Salva o diário no arquivo"""
        try:
            with open(self.arquivo_diario, 'w', encoding='utf-8') as f:
                json.dump(self.diario, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar diário: {e}")
    
    def abrir(self):
        """Abre o módulo do diário"""
        if self.janela and self.janela.winfo_exists():
            self.janela.lift()
            return
        
        self.parent.atualizar_status("Abrindo Diário...")
        
        self.janela = tk.Toplevel(self.parent.root)
        self.janela.title("📔 Meu Diário")
        self.janela.geometry("700x600")
        self.janela.configure(bg='#ecf0f1')
        
        frame = tk.Frame(self.janela, bg='#ecf0f1', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="📔 Meu Diário Pessoal", font=('Arial', 18, 'bold'),
                bg='#ecf0f1').pack(pady=10)
        
        data_atual = datetime.now().strftime("%d/%m/%Y")
        
        # Selecionar data
        data_frame = tk.Frame(frame, bg='#ecf0f1')
        data_frame.pack(pady=10)
        
        tk.Label(data_frame, text="Data:", font=('Arial', 10, 'bold'),
                bg='#ecf0f1').pack(side='left')
        
        self.entry_data = tk.Entry(data_frame, width=12, font=('Arial', 10))
        self.entry_data.insert(0, data_atual)
        self.entry_data.pack(side='left', padx=5)
        
        # Área de texto do diário
        tk.Label(frame, text="Como foi seu dia?", bg='#ecf0f1',
                font=('Arial', 10, 'bold')).pack(anchor='w')
        
        self.txt_diario = scrolledtext.ScrolledText(frame, height=15, font=('Arial', 11))
        self.txt_diario.pack(fill='both', expand=True, pady=10)
        
        # Botões
        btn_frame = tk.Frame(frame, bg='#ecf0f1')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="📖 Carregar", command=self.carregar_entrada,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="💾 Salvar", command=self.salvar_entrada,
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="📚 Histórico", command=self.ver_historico,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Fechar", command=self.fechar,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        self.carregar_entrada()
    
    def carregar_entrada(self):
        """Carrega uma entrada do diário"""
        data = self.entry_data.get().strip()
        if data in self.diario:
            self.txt_diario.delete("1.0", tk.END)
            self.txt_diario.insert("1.0", self.diario[data])
            self.parent.atualizar_status(f"Entrada de {data} carregada")
        else:
            self.txt_diario.delete("1.0", tk.END)
            self.parent.atualizar_status(f"Nenhuma entrada para {data}")
    
    def salvar_entrada(self):
        """Salva uma entrada no diário"""
        data = self.entry_data.get().strip()
        texto = self.txt_diario.get("1.0", tk.END).strip()
        
        if texto:
            self.diario[data] = texto
            self.salvar_diario()
            self.parent.atualizar_status(f"Diário de {data} salvo!")
            messagebox.showinfo("Sucesso", f"Entrada de {data} salva!")
        else:
            messagebox.showwarning("Aviso", "Digite algo no diário!")
    
    def ver_historico(self):
        """Mostra o histórico do diário"""
        if self.diario:
            historico = "\n".join([f"{data}: {texto[:50]}..." for data, texto in self.diario.items()])
            messagebox.showinfo("Histórico", f"Entradas do diário:\n\n{historico}")
        else:
            messagebox.showinfo("Histórico", "Nenhuma entrada ainda!")
    
    def fechar(self):
        """Fecha a janela"""
        if self.janela:
            self.janela.destroy()
            self.janela = None
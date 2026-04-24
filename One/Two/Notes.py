# One/Two/Notes.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
from datetime import datetime
from pathlib import Path

class NotesModule:
    def __init__(self, parent):
        self.parent = parent
        self.janela = None
        self.dados_dir = Path.home() / "MeuDashboard"
        self.dados_dir.mkdir(exist_ok=True)
        self.arquivo_notas = self.dados_dir / "anotacoes.json"
        self.carregar_notas()
    
    def carregar_notas(self):
        """Carrega as notas do arquivo"""
        try:
            if self.arquivo_notas.exists():
                with open(self.arquivo_notas, 'r', encoding='utf-8') as f:
                    self.notas = json.load(f)
            else:
                self.notas = []
        except Exception:
            self.notas = []
    
    def salvar_notas(self):
        """Salva as notas no arquivo"""
        try:
            with open(self.arquivo_notas, 'w', encoding='utf-8') as f:
                json.dump(self.notas, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar notas: {e}")
    
    def abrir(self):
        """Abre o módulo de anotações"""
        if self.janela and self.janela.winfo_exists():
            self.janela.lift()
            return
        
        self.parent.atualizar_status("Abrindo Anotações...")
        
        self.janela = tk.Toplevel(self.parent.root)
        self.janela.title("📝 Minhas Anotações")
        self.janela.geometry("700x500")
        self.janela.configure(bg='#ecf0f1')
        
        frame = tk.Frame(self.janela, bg='#ecf0f1', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="📝 Bloco de Anotações", font=('Arial', 18, 'bold'),
                bg='#ecf0f1').pack(pady=10)
        
        # Lista de anotações
        listbox_frame = tk.Frame(frame, bg='#ecf0f1')
        listbox_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                                  font=('Arial', 10), height=8)
        self.listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Área de texto
        tk.Label(frame, text="Nova anotação:", bg='#ecf0f1',
                font=('Arial', 10, 'bold')).pack(anchor='w')
        
        self.txt_nota = scrolledtext.ScrolledText(frame, height=6, font=('Arial', 10))
        self.txt_nota.pack(fill='x', pady=5)
        
        # Botões
        btn_frame = tk.Frame(frame, bg='#ecf0f1')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ Adicionar", command=self.adicionar_nota,
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="👁️ Ver", command=self.ver_nota,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Excluir", command=self.excluir_nota,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="❌ Fechar", command=self.fechar,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        self.atualizar_lista()
    
    def atualizar_lista(self):
        """Atualiza a lista de notas"""
        self.listbox.delete(0, tk.END)
        for nota in self.notas:
            self.listbox.insert(tk.END, f"{nota['data']} - {nota['titulo'][:50]}")
    
    def adicionar_nota(self):
        """Adiciona uma nova nota"""
        texto = self.txt_nota.get("1.0", tk.END).strip()
        if texto:
            titulo = texto.split('\n')[0][:50]
            self.notas.append({
                'titulo': titulo,
                'texto': texto,
                'data': datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            self.salvar_notas()
            self.atualizar_lista()
            self.txt_nota.delete("1.0", tk.END)
            self.parent.atualizar_status("Anotação adicionada!")
            messagebox.showinfo("Sucesso", "Anotação salva!")
        else:
            messagebox.showwarning("Aviso", "Digite uma anotação!")
    
    def ver_nota(self):
        """Visualiza uma nota"""
        selecao = self.listbox.curselection()
        if selecao:
            nota = self.notas[selecao[0]]
            messagebox.showinfo("Anotação", f"Data: {nota['data']}\n\n{nota['texto']}")
    
    def excluir_nota(self):
        """Exclui uma nota"""
        selecao = self.listbox.curselection()
        if selecao:
            if messagebox.askyesno("Confirmar", "Excluir esta anotação?"):
                del self.notas[selecao[0]]
                self.salvar_notas()
                self.atualizar_lista()
                self.parent.atualizar_status("Anotação excluída!")
    
    def fechar(self):
        """Fecha a janela"""
        if self.janela:
            self.janela.destroy()
            self.janela = None
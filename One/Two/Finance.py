# One/Two/Finance.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from pathlib import Path

class FinanceModule:
    def __init__(self, parent):
        self.parent = parent
        self.janela = None
        self.dados_dir = Path.home() / "MeuDashboard"
        self.dados_dir.mkdir(exist_ok=True)
        self.arquivo_financas = self.dados_dir / "financas.json"
        self.carregar_financas()
    
    def carregar_financas(self):
        """Carrega os dados financeiros"""
        try:
            if self.arquivo_financas.exists():
                with open(self.arquivo_financas, 'r', encoding='utf-8') as f:
                    self.financas = json.load(f)
            else:
                self.financas = {"receitas": [], "despesas": []}
        except Exception:
            self.financas = {"receitas": [], "despesas": []}
    
    def salvar_financas(self):
        """Salva os dados financeiros"""
        try:
            with open(self.arquivo_financas, 'w', encoding='utf-8') as f:
                json.dump(self.financas, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar finanças: {e}")
    
    def abrir(self):
        """Abre o módulo financeiro"""
        if self.janela and self.janela.winfo_exists():
            self.janela.lift()
            return
        
        self.parent.atualizar_status("Abrindo Finanças...")
        
        self.janela = tk.Toplevel(self.parent.root)
        self.janela.title("💰 Controle Financeiro")
        self.janela.geometry("700x600")
        self.janela.configure(bg='#ecf0f1')
        
        # Notebook para abas
        notebook = ttk.Notebook(self.janela)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de despesas
        frame_despesas = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(frame_despesas, text="💸 Despesas")
        self.criar_aba_financas(frame_despesas, "despesa")
        
        # Aba de receitas
        frame_receitas = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(frame_receitas, text="💰 Receitas")
        self.criar_aba_financas(frame_receitas, "receita")
        
        # Aba de resumo
        frame_resumo = tk.Frame(notebook, bg='#ecf0f1')
        notebook.add(frame_resumo, text="📊 Resumo")
        self.criar_resumo(frame_resumo)
    
    def criar_aba_financas(self, frame, tipo):
        """Cria uma aba de finanças"""
        # Lista de itens
        listbox_frame = tk.Frame(frame, bg='#ecf0f1')
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, height=12)
        listbox.pack(fill='both', expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Formulário
        form_frame = tk.LabelFrame(frame, text=f"Adicionar {tipo.title()}", 
                                  bg='#ecf0f1', font=('Arial', 10, 'bold'))
        form_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(form_frame, text="Descrição:", bg='#ecf0f1').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        entry_desc = tk.Entry(form_frame, width=30)
        entry_desc.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Valor (R$):", bg='#ecf0f1').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        entry_valor = tk.Entry(form_frame, width=15)
        entry_valor.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Data:", bg='#ecf0f1').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        entry_data = tk.Entry(form_frame, width=12)
        entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        entry_data.grid(row=2, column=1, padx=5, pady=5)
        
        total_label = tk.Label(frame, text=f"Total {tipo}s: R$ 0.00", 
                              bg='#ecf0f1', font=('Arial', 12, 'bold'))
        total_label.pack()
        
        def atualizar_lista():
            listbox.delete(0, tk.END)
            items = self.financas[f"{tipo}s"]
            total = 0
            for item in items:
                listbox.insert(tk.END, f"{item['data']} - {item['desc']}: R$ {item['valor']:.2f}")
                total += item['valor']
            cor = '#e74c3c' if tipo == 'despesa' else '#2ecc71'
            total_label.config(text=f"Total {tipo}s: R$ {total:.2f}", fg=cor)
        
        def adicionar_item():
            try:
                desc = entry_desc.get().strip()
                valor = float(entry_valor.get().strip())
                data = entry_data.get().strip()
                
                if desc and valor > 0:
                    self.financas[f"{tipo}s"].append({
                        'desc': desc,
                        'valor': valor,
                        'data': data
                    })
                    self.salvar_financas()
                    atualizar_lista()
                    entry_desc.delete(0, tk.END)
                    entry_valor.delete(0, tk.END)
                    self.parent.atualizar_status(f"{tipo.title()} adicionada: R$ {valor:.2f}")
                    messagebox.showinfo("Sucesso", f"{tipo.title()} adicionada!")
                else:
                    messagebox.showwarning("Aviso", "Preencha todos os campos!")
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
        
        def excluir_item():
            selecao = listbox.curselection()
            if selecao:
                if messagebox.askyesno("Confirmar", f"Excluir esta {tipo}?"):
                    del self.financas[f"{tipo}s"][selecao[0]]
                    self.salvar_financas()
                    atualizar_lista()
                    self.parent.atualizar_status(f"{tipo.title()} excluída!")
        
        # Botões
        btn_frame = tk.Frame(form_frame, bg='#ecf0f1')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="➕ Adicionar", command=adicionar_item,
                 bg='#2ecc71', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Excluir", command=excluir_item,
                 bg='#e74c3c', fg='white', font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        
        atualizar_lista()
    
    def criar_resumo(self, frame):
        """Cria o resumo financeiro"""
        total_receitas = sum(item['valor'] for item in self.financas['receitas'])
        total_despesas = sum(item['valor'] for item in self.financas['despesas'])
        saldo = total_receitas - total_despesas
        
        tk.Label(frame, text="📊 Resumo Financeiro", font=('Arial', 16, 'bold'),
                bg='#ecf0f1').pack(pady=20)
        
        resumo_frame = tk.Frame(frame, bg='#ecf0f1', relief=tk.RAISED, borderwidth=2)
        resumo_frame.pack(pady=20, padx=20, fill='x')
        
        tk.Label(resumo_frame, text=f"💰 Total de Receitas: R$ {total_receitas:.2f}",
                font=('Arial', 12), bg='#ecf0f1', fg='#2ecc71').pack(pady=5)
        
        tk.Label(resumo_frame, text=f"💸 Total de Despesas: R$ {total_despesas:.2f}",
                font=('Arial', 12), bg='#ecf0f1', fg='#e74c3c').pack(pady=5)
        
        cor_saldo = '#2ecc71' if saldo >= 0 else '#e74c3c'
        tk.Label(resumo_frame, text=f"💵 Saldo: R$ {saldo:.2f}",
                font=('Arial', 14, 'bold'), bg='#ecf0f1', fg=cor_saldo).pack(pady=10)
        
        # Dicas
        dica_frame = tk.LabelFrame(frame, text="💡 Dica Financeira", bg='#ecf0f1', font=('Arial', 10, 'bold'))
        dica_frame.pack(pady=20, padx=20, fill='x')
        
        if saldo < 0:
            dica = "⚠️ Atenção! Suas despesas estão maiores que as receitas. Reveja seus gastos!"
        elif saldo < 500:
            dica = "📈 Continue economizando! Tente reduzir gastos desnecessários."
        else:
            dica = "🎉 Excelente! Continue mantendo suas finanças organizadas."
        
        tk.Label(dica_frame, text=dica, wraplength=500, bg='#ecf0f1',
                font=('Arial', 10)).pack(pady=10, padx=10)
        
        tk.Button(frame, text="Atualizar", command=lambda: self.criar_resumo(frame),
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
    
    def fechar(self):
        """Fecha a janela"""
        if self.janela:
            self.janela.destroy()
            self.janela = None
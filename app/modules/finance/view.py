"""
Interface do módulo de finanças
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime


class FinanceView(ctk.CTkToplevel):
    """Janela de controle financeiro"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Configurar janela
        self.title("💰 Minhas Finanças")
        self.geometry("1100x750")
        
        # Centralizar
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1100) // 2
        y = (screen_height - 750) // 2
        self.geometry(f"+{x}+{y}")
        
        # Configurar fechamento
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        
        # Mês/ano atual
        self.mes_atual = datetime.now().month
        self.ano_atual = datetime.now().year
        
        # Aplicar tema
        tema = self.controller.app.config.get("tema", "dark")
        ctk.set_appearance_mode(tema)
        
        self._setup_ui()
        self.atualizar_dados()
    
    def _setup_ui(self):
        """Configura a interface"""
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        titulo = ctk.CTkLabel(
            header,
            text="💰 Controle Financeiro",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FF6B8A"
        )
        titulo.pack(side="left")
        
        # Botão nova transação
        self.novo_btn = ctk.CTkButton(
            header,
            text="➕ Nova Transação",
            command=self.nova_transacao,
            width=160,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.novo_btn.pack(side="right", padx=5)
        
        # Navegação de mês
        nav_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(0, 15))
        
        btn_anterior = ctk.CTkButton(
            nav_frame,
            text="◀",
            width=40,
            command=self.mes_anterior
        )
        btn_anterior.pack(side="left", padx=5)
        
        from utils.helpers import obter_nome_mes
        self.mes_label = ctk.CTkLabel(
            nav_frame,
            text=f"{obter_nome_mes(self.mes_atual)} {self.ano_atual}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.mes_label.pack(side="left", expand=True)
        
        btn_proximo = ctk.CTkButton(
            nav_frame,
            text="▶",
            width=40,
            command=self.mes_proximo
        )
        btn_proximo.pack(side="left", padx=5)
        
        # Cards de resumo
        resumo_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        resumo_frame.pack(fill="x", pady=(0, 15))
        
        # Card Receitas
        self.receitas_card = ctk.CTkFrame(resumo_frame, corner_radius=15, fg_color="#2A5F8B")
        self.receitas_card.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkLabel(
            self.receitas_card,
            text="💰 Receitas",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(pady=(10, 5))
        
        self.receitas_label = ctk.CTkLabel(
            self.receitas_card,
            text="R$ 0,00",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#90EE90"
        )
        self.receitas_label.pack(pady=(0, 10))
        
        # Card Despesas
        self.despesas_card = ctk.CTkFrame(resumo_frame, corner_radius=15, fg_color="#8B3A3A")
        self.despesas_card.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkLabel(
            self.despesas_card,
            text="📉 Despesas",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(pady=(10, 5))
        
        self.despesas_label = ctk.CTkLabel(
            self.despesas_card,
            text="R$ 0,00",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FF9090"
        )
        self.despesas_label.pack(pady=(0, 10))
        
        # Card Saldo
        self.saldo_card = ctk.CTkFrame(resumo_frame, corner_radius=15, fg_color="#6A3A8B")
        self.saldo_card.pack(side="left", expand=True, fill="x", padx=5)
        
        ctk.CTkLabel(
            self.saldo_card,
            text="💎 Saldo",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(pady=(10, 5))
        
        self.saldo_label = ctk.CTkLabel(
            self.saldo_card,
            text="R$ 0,00",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#90EE90"
        )
        self.saldo_label.pack(pady=(0, 10))
        
        # Frame principal (2 colunas)
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Lista de transações
        self.transacoes_frame = ctk.CTkFrame(content_frame, corner_radius=15)
        self.transacoes_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(
            self.transacoes_frame,
            text="📋 Últimas Transações",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF6B8A"
        ).pack(pady=(10, 5))
        
        self.transacoes_lista = ctk.CTkScrollableFrame(
            self.transacoes_frame,
            fg_color="transparent"
        )
        self.transacoes_lista.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Gráfico de despesas por categoria
        self.categorias_frame = ctk.CTkFrame(content_frame, corner_radius=15)
        self.categorias_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(
            self.categorias_frame,
            text="📊 Despesas por Categoria",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF6B8A"
        ).pack(pady=(10, 5))
        
        self.categorias_lista = ctk.CTkScrollableFrame(
            self.categorias_frame,
            fg_color="transparent"
        )
        self.categorias_lista.pack(fill="both", expand=True, padx=10, pady=10)
    
    def atualizar_dados(self):
        """Atualiza todos os dados"""
        # Totais
        receitas = self.controller.get_total_receitas(self.mes_atual, self.ano_atual)
        despesas = self.controller.get_total_despesas(self.mes_atual, self.ano_atual)
        saldo = self.controller.get_saldo(self.mes_atual, self.ano_atual)
        
        from utils.helpers import formatar_moeda
        self.receitas_label.configure(text=formatar_moeda(receitas))
        self.despesas_label.configure(text=formatar_moeda(despesas))
        
        cor_saldo = "#90EE90" if saldo >= 0 else "#FF9090"
        self.saldo_label.configure(text=formatar_moeda(saldo), text_color=cor_saldo)
        
        # Lista de transações
        for widget in self.transacoes_lista.winfo_children():
            widget.destroy()
        
        transacoes = self.controller.get_transacoes(self.mes_atual, self.ano_atual)
        
        if not transacoes:
            msg = ctk.CTkLabel(
                self.transacoes_lista,
                text="📭 Nenhuma transação neste mês",
                font=ctk.CTkFont(size=14),
                text_color="#808080"
            )
            msg.pack(pady=20)
        else:
            for transacao in transacoes[:20]:  # Últimas 20
                self.criar_card_transacao(transacao)
        
        # Despesas por categoria
        for widget in self.categorias_lista.winfo_children():
            widget.destroy()
        
        despesas_categoria = self.controller.get_despesas_por_categoria(self.mes_atual, self.ano_atual)
        
        if not despesas_categoria:
            msg = ctk.CTkLabel(
                self.categorias_lista,
                text="📊 Nenhuma despesa registrada",
                font=ctk.CTkFont(size=14),
                text_color="#808080"
            )
            msg.pack(pady=20)
        else:
            # Ordenar por valor (maior primeiro)
            for categoria, valor in sorted(despesas_categoria.items(), key=lambda x: x[1], reverse=True):
                self.criar_item_categoria(categoria, valor, sum(despesas_categoria.values()))
    
    def criar_card_transacao(self, transacao):
        """Cria um card para exibir uma transação"""
        card = ctk.CTkFrame(self.transacoes_lista, corner_radius=10)
        card.pack(fill="x", pady=5)
        
        # Cor baseada no tipo
        cor = "#90EE90" if transacao["tipo"] == "receita" else "#FF9090"
        
        # Frame principal
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=8)
        
        # Descrição e categoria
        desc_label = ctk.CTkLabel(
            info_frame,
            text=transacao["descricao"],
            font=ctk.CTkFont(size=14, weight="bold")
        )
        desc_label.pack(anchor="w")
        
        cat_label = ctk.CTkLabel(
            info_frame,
            text=f"📁 {transacao['categoria']}",
            font=ctk.CTkFont(size=11),
            text_color="#808080"
        )
        cat_label.pack(anchor="w")
        
        # Data
        data_obj = datetime.strptime(transacao["data"], "%Y-%m-%d")
        data_label = ctk.CTkLabel(
            info_frame,
            text=f"📅 {data_obj.strftime('%d/%m/%Y')}",
            font=ctk.CTkFont(size=11),
            text_color="#808080"
        )
        data_label.pack(anchor="w")
        
        # Valor
        from utils.helpers import formatar_moeda
        valor_label = ctk.CTkLabel(
            info_frame,
            text=formatar_moeda(transacao["valor"]),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=cor
        )
        valor_label.pack(anchor="e")
        
        # Botão excluir
        excluir_btn = ctk.CTkButton(
            card,
            text="🗑️",
            width=30,
            height=25,
            fg_color="#8B3A3A",
            hover_color="#B04D4D",
            command=lambda: self.excluir_transacao(transacao["id"])
        )
        excluir_btn.place(relx=0.98, rely=0.5, anchor="e")
    
    def criar_item_categoria(self, categoria, valor, total):
        """Cria um item de categoria com barra de progresso"""
        frame = ctk.CTkFrame(self.categorias_lista, fg_color="transparent")
        frame.pack(fill="x", pady=5)
        
        # Nome e valor
        info_frame = ctk.CTkFrame(frame, fg_color="transparent")
        info_frame.pack(fill="x")
        
        nome_label = ctk.CTkLabel(
            info_frame,
            text=categoria,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        nome_label.pack(side="left")
        
        from utils.helpers import formatar_moeda
        valor_label = ctk.CTkLabel(
            info_frame,
            text=formatar_moeda(valor),
            font=ctk.CTkFont(size=13),
            text_color="#FF9090"
        )
        valor_label.pack(side="right")
        
        # Barra de progresso
        percentual = (valor / total) if total > 0 else 0
        progress = ctk.CTkProgressBar(frame, height=10, corner_radius=5)
        progress.pack(fill="x", pady=(5, 0))
        progress.set(percentual)
        
        # Percentual
        percent_label = ctk.CTkLabel(
            frame,
            text=f"{percentual:.1%}",
            font=ctk.CTkFont(size=10),
            text_color="#808080"
        )
        percent_label.pack(anchor="e")
    
    def nova_transacao(self):
        """Abre diálogo para nova transação"""
        self.abrir_editor()
    
    def abrir_editor(self, transacao=None):
        """Abre o editor de transações"""
        editor = ctk.CTkToplevel(self)
        editor.title("💰 Nova Transação")
        editor.geometry("450x550")
        editor.transient(self)
        editor.grab_set()
        
        tema = self.controller.app.config.get("tema", "dark")
        ctk.set_appearance_mode(tema)
        
        # Centralizar
        screen_width = editor.winfo_screenwidth()
        screen_height = editor.winfo_screenheight()
        x = (screen_width - 450) // 2
        y = (screen_height - 550) // 2
        editor.geometry(f"+{x}+{y}")
        
        main_frame = ctk.CTkFrame(editor, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Tipo
        tipo_label = ctk.CTkLabel(
            main_frame,
            text="Tipo:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        tipo_label.pack(anchor="w", pady=(0, 5))
        
        tipo_var = ctk.StringVar(value="despesa")
        tipo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        tipo_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkRadioButton(
            tipo_frame,
            text="💰 Receita",
            variable=tipo_var,
            value="receita",
            command=lambda: self.atualizar_cor_editor(tipo_var.get(), valor_entry)
        ).pack(side="left", padx=10)
        
        ctk.CTkRadioButton(
            tipo_frame,
            text="📉 Despesa",
            variable=tipo_var,
            value="despesa",
            command=lambda: self.atualizar_cor_editor(tipo_var.get(), valor_entry)
        ).pack(side="left", padx=10)
        
        # Valor
        valor_label = ctk.CTkLabel(
            main_frame,
            text="Valor (R$):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        valor_label.pack(anchor="w", pady=(0, 5))
        
        valor_entry = ctk.CTkEntry(main_frame, placeholder_text="0,00", height=40)
        valor_entry.pack(fill="x", pady=(0, 15))
        
        # Categoria
        cat_label = ctk.CTkLabel(
            main_frame,
            text="Categoria:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        cat_label.pack(anchor="w", pady=(0, 5))
        
        categorias = self.controller.get_categorias()
        cat_combo = ctk.CTkComboBox(
            main_frame,
            values=categorias,
            height=40
        )
        cat_combo.pack(fill="x", pady=(0, 15))
        cat_combo.set(categorias[0])
        
        # Descrição
        desc_label = ctk.CTkLabel(
            main_frame,
            text="Descrição:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        desc_label.pack(anchor="w", pady=(0, 5))
        
        desc_entry = ctk.CTkEntry(main_frame, placeholder_text="Ex: Supermercado", height=40)
        desc_entry.pack(fill="x", pady=(0, 15))
        
        def salvar():
            try:
                tipo = tipo_var.get()
                valor_str = valor_entry.get().strip().replace(",", ".")
                valor = float(valor_str)
                categoria = cat_combo.get()
                descricao = desc_entry.get().strip()
                
                if not descricao:
                    messagebox.showwarning("Aviso", "Digite uma descrição")
                    return
                
                self.controller.adicionar_transacao(tipo, valor, categoria, descricao)
                self.atualizar_dados()
                editor.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido! Use números e vírgula")
        
        ctk.CTkButton(
            main_frame,
            text="💾 Salvar",
            command=salvar,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(fill="x", pady=5)
        
        ctk.CTkButton(
            main_frame,
            text="❌ Cancelar",
            command=editor.destroy,
            height=40
        ).pack(fill="x", pady=5)
        
        def atualizar_cor_editor(tipo, entry):
            if tipo == "receita":
                entry.configure(border_color="#90EE90")
            else:
                entry.configure(border_color="#FF9090")
        
        atualizar_cor_editor(tipo_var.get(), valor_entry)
        valor_entry.bind("<KeyRelease>", lambda e: atualizar_cor_editor(tipo_var.get(), valor_entry))
    
    def atualizar_cor_editor(self, tipo, entry):
        """Atualiza a cor do campo valor no editor"""
        if tipo == "receita":
            entry.configure(border_color="#90EE90")
        else:
            entry.configure(border_color="#FF9090")
    
    def excluir_transacao(self, transacao_id):
        """Exclui uma transação"""
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta transação?"):
            self.controller.excluir_transacao(transacao_id)
            self.atualizar_dados()
    
    def mes_anterior(self):
        """Vai para o mês anterior"""
        if self.mes_atual == 1:
            self.mes_atual = 12
            self.ano_atual -= 1
        else:
            self.mes_atual -= 1
        self.atualizar_mes_label()
        self.atualizar_dados()
    
    def mes_proximo(self):
        """Vai para o próximo mês"""
        if self.mes_atual == 12:
            self.mes_atual = 1
            self.ano_atual += 1
        else:
            self.mes_atual += 1
        self.atualizar_mes_label()
        self.atualizar_dados()
    
    def atualizar_mes_label(self):
        """Atualiza o label do mês"""
        from utils.helpers import obter_nome_mes
        self.mes_label.configure(text=f"{obter_nome_mes(self.mes_atual)} {self.ano_atual}")
    
    def fechar(self):
        """Fecha a janela"""
        self.controller.fechar()
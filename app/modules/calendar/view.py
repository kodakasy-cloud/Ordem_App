"""
Interface do módulo de calendário
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import calendar


class CalendarView(ctk.CTkToplevel):
    """Janela de calendário com eventos"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Configurar janela
        self.title("Meu Calendário")
        self.geometry("1000x700")
        
        # Centralizar
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 700) // 2
        self.geometry(f"+{x}+{y}")
        
        # Configurar fechamento
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        
        # Data atual
        self.ano_atual = datetime.now().year
        self.mes_atual = datetime.now().month
        self.dia_selecionado = None
        
        # Aplicar tema
        tema = self.controller.app.config.get("tema", "dark")
        ctk.set_appearance_mode(tema)
        
        self._setup_ui()
        self.atualizar_calendario()
    
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
            text="Meu Calendario",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FF6B8A"
        )
        titulo.pack(side="left")
        
        # Botão novo evento
        self.novo_btn = ctk.CTkButton(
            header,
            text="Novo Evento",
            command=self.novo_evento,
            width=140,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.novo_btn.pack(side="right", padx=5)
        
        # Frame do calendário (2 colunas)
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Painel do calendário
        self.calendario_frame = ctk.CTkFrame(
            content_frame,
            corner_radius=15,
            fg_color="transparent"
        )
        self.calendario_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Painel de eventos
        self.eventos_frame = ctk.CTkFrame(
            content_frame,
            corner_radius=15
        )
        self.eventos_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Título eventos
        self.eventos_titulo = ctk.CTkLabel(
            self.eventos_frame,
            text="Eventos do Dia",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FF6B8A"
        )
        self.eventos_titulo.pack(pady=(15, 10))
        
        # Lista de eventos
        self.eventos_lista = ctk.CTkScrollableFrame(
            self.eventos_frame,
            fg_color="transparent"
        )
        self.eventos_lista.pack(fill="both", expand=True, padx=10, pady=10)
    
    def atualizar_calendario(self):
        """Atualiza a exibição do calendário"""
        # Limpar frame
        for widget in self.calendario_frame.winfo_children():
            widget.destroy()
        
        # Navegação
        nav_frame = ctk.CTkFrame(self.calendario_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(0, 15))
        
        # Botão mês anterior
        btn_anterior = ctk.CTkButton(
            nav_frame,
            text="<",
            width=40,
            command=self.mes_anterior,
            font=ctk.CTkFont(size=16)
        )
        btn_anterior.pack(side="left", padx=5)
        
        # Título do mês/ano
        from app.utils.helpers import obter_nome_mes
        nome_mes = obter_nome_mes(self.mes_atual)
        self.mes_label = ctk.CTkLabel(
            nav_frame,
            text=f"{nome_mes} {self.ano_atual}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FF6B8A"
        )
        self.mes_label.pack(side="left", expand=True)
        
        # Botão próximo mês
        btn_proximo = ctk.CTkButton(
            nav_frame,
            text=">",
            width=40,
            command=self.mes_proximo,
            font=ctk.CTkFont(size=16)
        )
        btn_proximo.pack(side="right", padx=5)
        
        # Botão hoje
        btn_hoje = ctk.CTkButton(
            nav_frame,
            text="Hoje",
            width=80,
            command=self.ir_hoje,
            font=ctk.CTkFont(size=12)
        )
        btn_hoje.pack(side="right", padx=5)
        
        # Dias da semana
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
        week_frame = ctk.CTkFrame(self.calendario_frame, fg_color="transparent")
        week_frame.pack(fill="x", pady=(0, 10))
        
        for dia in dias_semana:
            label = ctk.CTkLabel(
                week_frame,
                text=dia,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#FF6B8A",
                width=40
            )
            label.pack(side="left", expand=True, fill="x")
        
        # Grade do calendário
        self.cal_grid = ctk.CTkFrame(self.calendario_frame, fg_color="transparent")
        self.cal_grid.pack(fill="both", expand=True)
        
        # Configurar grid (7 colunas)
        for i in range(7):
            self.cal_grid.grid_columnconfigure(i, weight=1)
        
        # Obter dias do mês
        cal = calendar.monthcalendar(self.ano_atual, self.mes_atual)
        
        # Preencher grid
        self.botoes_dias = {}
        hoje = datetime.now().date()
        
        for semana_idx, semana in enumerate(cal):
            for dia_idx, dia in enumerate(semana):
                if dia == 0:
                    # Dia vazio
                    btn = ctk.CTkButton(
                        self.cal_grid,
                        text="",
                        width=50,
                        height=50,
                        state="disabled",
                        fg_color="transparent"
                    )
                    btn.grid(row=semana_idx, column=dia_idx, padx=2, pady=2, sticky="nsew")
                else:
                    # Dia com número
                    data_str = f"{self.ano_atual:04d}-{self.mes_atual:02d}-{dia:02d}"
                    eventos_dia = self.controller.get_eventos_data(data_str)
                    
                    # Definir cor baseada em eventos
                    if eventos_dia:
                        cor = "#FF6B8A" if len(eventos_dia) == 1 else "#FF9AB8"
                    else:
                        cor = "#3D3D3D"
                    
                    # Verificar se é hoje
                    if data_str == hoje.strftime("%Y-%m-%d"):
                        cor = "#FF3B6A"
                    
                    btn = ctk.CTkButton(
                        self.cal_grid,
                        text=str(dia),
                        width=50,
                        height=50,
                        fg_color=cor,
                        hover_color="#FF9AB8",
                        command=lambda d=dia: self.selecionar_dia(d)
                    )
                    btn.grid(row=semana_idx, column=dia_idx, padx=2, pady=2, sticky="nsew")
                    
                    # Indicador de eventos
                    if eventos_dia:
                        btn_text = f"{dia}\n●"
                        btn.configure(text=btn_text, font=ctk.CTkFont(size=12))
                    
                    self.botoes_dias[dia] = btn
    
    def selecionar_dia(self, dia):
        """Seleciona um dia e mostra eventos"""
        self.dia_selecionado = dia
        self.carregar_eventos_dia()
    
    def carregar_eventos_dia(self):
        """Carrega eventos do dia selecionado"""
        if not self.dia_selecionado:
            return
        
        # Limpar lista
        for widget in self.eventos_lista.winfo_children():
            widget.destroy()
        
        data_str = f"{self.ano_atual:04d}-{self.mes_atual:02d}-{self.dia_selecionado:02d}"
        eventos = self.controller.get_eventos_data(data_str)
        
        if not eventos:
            msg = ctk.CTkLabel(
                self.eventos_lista,
                text="Nenhum evento neste dia",
                font=ctk.CTkFont(size=14),
                text_color="#808080"
            )
            msg.pack(pady=20)
            return
        
        for evento in eventos:
            self.criar_card_evento(evento)
    
    def criar_card_evento(self, evento):
        """Cria um card para exibir um evento"""
        card = ctk.CTkFrame(self.eventos_lista, corner_radius=10)
        card.pack(fill="x", pady=5)
        
        # Cor do evento
        cor = evento.get("cor", "#FF6B8A")
        
        # Título
        titulo = ctk.CTkLabel(
            card,
            text=evento.get("titulo", "Sem titulo"),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=cor
        )
        titulo.pack(anchor="w", padx=10, pady=(5, 0))
        
        # Hora
        if evento.get("hora"):
            hora_label = ctk.CTkLabel(
                card,
                text=f"Hora: {evento['hora']}",
                font=ctk.CTkFont(size=11),
                text_color="#808080"
            )
            hora_label.pack(anchor="w", padx=10, pady=(0, 2))
        
        # Descrição
        if evento.get("descricao"):
            desc = evento["descricao"]
            if len(desc) > 100:
                desc = desc[:100] + "..."
            desc_label = ctk.CTkLabel(
                card,
                text=desc,
                font=ctk.CTkFont(size=12),
                wraplength=200,
                justify="left"
            )
            desc_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        # Botões
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        editar_btn = ctk.CTkButton(
            btn_frame,
            text="Editar",
            width=30,
            height=25,
            command=lambda: self.editar_evento(evento)
        )
        editar_btn.pack(side="left", padx=2)
        
        excluir_btn = ctk.CTkButton(
            btn_frame,
            text="Excluir",
            width=30,
            height=25,
            fg_color="#8B3A3A",
            hover_color="#B04D4D",
            command=lambda: self.excluir_evento(evento["id"])
        )
        excluir_btn.pack(side="left", padx=2)
    
    def novo_evento(self):
        """Abre diálogo para criar novo evento"""
        self.abrir_editor()
    
    def editar_evento(self, evento):
        """Abre diálogo para editar evento"""
        self.abrir_editor(evento)
    
    def abrir_editor(self, evento=None):
        """Abre o editor de eventos"""
        editor = ctk.CTkToplevel(self)
        editor.title("Editar Evento" if evento else "Novo Evento")
        editor.geometry("500x500")
        editor.transient(self)
        editor.grab_set()
        
        # Aplicar tema
        tema = self.controller.app.config.get("tema", "dark")
        ctk.set_appearance_mode(tema)
        
        # Centralizar
        screen_width = editor.winfo_screenwidth()
        screen_height = editor.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 500) // 2
        editor.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(editor, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo_label = ctk.CTkLabel(
            main_frame,
            text="Titulo do Evento:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo_label.pack(anchor="w", pady=(0, 5))
        
        titulo_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Digite o titulo...",
            height=40
        )
        titulo_entry.pack(fill="x", pady=(0, 15))
        
        # Data
        data_label = ctk.CTkLabel(
            main_frame,
            text="Data:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        data_label.pack(anchor="w", pady=(0, 5))
        
        data_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="DD/MM/AAAA",
            height=40
        )
        data_entry.pack(fill="x", pady=(0, 15))
        
        # Hora
        hora_label = ctk.CTkLabel(
            main_frame,
            text="Hora (opcional):",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        hora_label.pack(anchor="w", pady=(0, 5))
        
        hora_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="HH:MM",
            height=40
        )
        hora_entry.pack(fill="x", pady=(0, 15))
        
        # Descrição
        desc_label = ctk.CTkLabel(
            main_frame,
            text="Descricao:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        desc_label.pack(anchor="w", pady=(0, 5))
        
        desc_text = ctk.CTkTextbox(main_frame, height=150)
        desc_text.pack(fill="both", expand=True, pady=(0, 20))
        
        # Preencher dados se for edição
        if evento:
            titulo_entry.insert(0, evento.get("titulo", ""))
            data_entry.insert(0, evento.get("data", ""))
            hora_entry.insert(0, evento.get("hora", ""))
            desc_text.insert("1.0", evento.get("descricao", ""))
        elif self.dia_selecionado:
            data_padrao = f"{self.dia_selecionado:02d}/{self.mes_atual:02d}/{self.ano_atual}"
            data_entry.insert(0, data_padrao)
        
        def salvar():
            titulo = titulo_entry.get().strip()
            data = data_entry.get().strip()
            hora = hora_entry.get().strip()
            descricao = desc_text.get("1.0", "end-1c").strip()
            
            if not titulo:
                messagebox.showwarning("Aviso", "Digite um titulo para o evento.")
                return
            
            if not data:
                messagebox.showwarning("Aviso", "Digite uma data para o evento.")
                return
            
            # Validar data
            try:
                from datetime import datetime
                data_obj = datetime.strptime(data, "%d/%m/%Y")
                data_formatada = data_obj.strftime("%Y-%m-%d")
            except:
                messagebox.showerror("Erro", "Data invalida! Use o formato DD/MM/AAAA")
                return
            
            if evento:
                self.controller.editar_evento(
                    evento["id"],
                    titulo=titulo,
                    data=data_formatada,
                    hora=hora,
                    descricao=descricao
                )
            else:
                self.controller.adicionar_evento(titulo, data_formatada, hora, descricao)
            
            self.atualizar_calendario()
            if self.dia_selecionado:
                self.carregar_eventos_dia()
            editor.destroy()
        
        ctk.CTkButton(
            main_frame,
            text="Salvar",
            command=salvar,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(fill="x", pady=5)
        
        ctk.CTkButton(
            main_frame,
            text="Cancelar",
            command=editor.destroy,
            height=40
        ).pack(fill="x", pady=5)
    
    def excluir_evento(self, evento_id):
        """Exclui um evento após confirmação"""
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este evento?"):
            self.controller.excluir_evento(evento_id)
            self.atualizar_calendario()
            if self.dia_selecionado:
                self.carregar_eventos_dia()
    
    def mes_anterior(self):
        """Vai para o mês anterior"""
        if self.mes_atual == 1:
            self.mes_atual = 12
            self.ano_atual -= 1
        else:
            self.mes_atual -= 1
        self.atualizar_calendario()
    
    def mes_proximo(self):
        """Vai para o próximo mês"""
        if self.mes_atual == 12:
            self.mes_atual = 1
            self.ano_atual += 1
        else:
            self.mes_atual += 1
        self.atualizar_calendario()
    
    def ir_hoje(self):
        """Vai para o mês atual"""
        hoje = datetime.now()
        self.ano_atual = hoje.year
        self.mes_atual = hoje.month
        self.dia_selecionado = hoje.day
        self.atualizar_calendario()
        self.carregar_eventos_dia()
    
    def fechar(self):
        """Fecha a janela"""
        self.controller.fechar()
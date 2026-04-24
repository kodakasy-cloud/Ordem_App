"""
Interface do módulo de diário
"""
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime


class DailyView(ctk.CTkToplevel):
    """Janela do diário pessoal"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Configurar janela
        self.title("💖 Meu Diário")
        self.geometry("950x700")
        
        # Centralizar
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 950) // 2
        y = (screen_height - 700) // 2
        self.geometry(f"+{x}+{y}")
        
        # Configurar fechamento
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        
        # Data atual
        self.data_atual = datetime.now().strftime("%Y-%m-%d")
        
        # Aplicar tema
        tema = self.controller.app.config.get("tema", "dark")
        ctk.set_appearance_mode(tema)
        
        self._setup_ui()
        self.carregar_entrada_hoje()
    
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
            text="💖 Meu Diário",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FF6B8A"
        )
        titulo.pack(side="left")
        
        # Seletor de data
        data_frame = ctk.CTkFrame(header, fg_color="transparent")
        data_frame.pack(side="right")
        
        self.data_entry = ctk.CTkEntry(
            data_frame,
            placeholder_text="DD/MM/AAAA",
            width=120,
            height=35
        )
        self.data_entry.pack(side="left", padx=5)
        self.data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        ctk.CTkButton(
            data_frame,
            text="📅 Ir",
            width=50,
            height=35,
            command=self.ir_para_data
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            data_frame,
            text="📖 Ver Todas",
            width=100,
            height=35,
            command=self.ver_todas_entradas,
            fg_color="#6A3A8B",
            hover_color="#8A4DB0"
        ).pack(side="left", padx=5)
        
        # Frame principal (2 colunas)
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Painel de humor e tags (esquerda)
        self.painel_humor = ctk.CTkFrame(content_frame, corner_radius=15)
        self.painel_humor.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Título humor
        ctk.CTkLabel(
            self.painel_humor,
            text="😊 Como você está se sentindo?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF6B8A"
        ).pack(pady=(15, 10))
        
        # Botões de humor
        self.humor_var = ctk.StringVar(value="😊")
        humores = [
            ("😊", "Feliz"), ("🥰", "Amor"), ("😢", "Triste"),
            ("😤", "Ansiosa"), ("😴", "Cansada"), ("🤗", "Grata")
        ]
        
        humor_frame = ctk.CTkFrame(self.painel_humor, fg_color="transparent")
        humor_frame.pack(pady=10)
        
        for i, (emoji, texto) in enumerate(humores):
            btn = ctk.CTkButton(
                humor_frame,
                text=f"{emoji} {texto}",
                width=100,
                height=40,
                command=lambda e=emoji: self.humor_var.set(e)
            )
            btn.pack(pady=5)
        
        # Tags
        ctk.CTkLabel(
            self.painel_humor,
            text="🏷️ Tags",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FF6B8A"
        ).pack(pady=(15, 5))
        
        self.tags_entry = ctk.CTkEntry(
            self.painel_humor,
            placeholder_text="Separe por vírgulas",
            height=35
        )
        self.tags_entry.pack(fill="x", padx=15, pady=5)
        
        # Sugestões de tags
        tags_sugeridas = ["#amor", "#gratidão", "#aprendizado", "#metas"]
        tags_frame = ctk.CTkFrame(self.painel_humor, fg_color="transparent")
        tags_frame.pack(pady=5)
        
        for tag in tags_sugeridas:
            ctk.CTkLabel(
                tags_frame,
                text=tag,
                font=ctk.CTkFont(size=11),
                text_color="#808080"
            ).pack(side="left", padx=5)
        
        # Editor (direita)
        self.editor_frame = ctk.CTkFrame(content_frame, corner_radius=15)
        self.editor_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Título da entrada
        ctk.CTkLabel(
            self.editor_frame,
            text="📝 Título do Dia",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FF6B8A"
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.titulo_entry = ctk.CTkEntry(
            self.editor_frame,
            placeholder_text="Como foi seu dia?",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.titulo_entry.pack(fill="x", padx=15, pady=(0, 15))
        
        # Conteúdo
        ctk.CTkLabel(
            self.editor_frame,
            text="✍️ Escreva aqui...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FF6B8A"
        ).pack(anchor="w", padx=15, pady=(0, 5))
        
        self.conteudo_text = ctk.CTkTextbox(
            self.editor_frame,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.conteudo_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Botões
        btn_frame = ctk.CTkFrame(self.editor_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar",
            command=self.salvar_entrada,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=5, expand=True, fill="x")
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Excluir",
            command=self.excluir_entrada,
            height=40,
            fg_color="#8B3A3A",
            hover_color="#B04D4D"
        ).pack(side="left", padx=5, expand=True, fill="x")
    
    def carregar_entrada_hoje(self):
        """Carrega a entrada do dia atual"""
        entrada = self.controller.get_entrada(self.data_atual)
        if entrada:
            self.titulo_entry.delete(0, "end")
            self.titulo_entry.insert(0, entrada.get("titulo", ""))
            
            self.conteudo_text.delete("1.0", "end")
            self.conteudo_text.insert("1.0", entrada.get("conteudo", ""))
            
            self.humor_var.set(entrada.get("humor", "😊"))
            
            tags = entrada.get("tags", [])
            if tags:
                self.tags_entry.delete(0, "end")
                self.tags_entry.insert(0, ", ".join(tags))
    
    def ir_para_data(self):
        """Vai para uma data específica"""
        data_str = self.data_entry.get().strip()
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y")
            self.data_atual = data_obj.strftime("%Y-%m-%d")
            self.carregar_entrada_data(self.data_atual)
        except:
            messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA")
    
    def carregar_entrada_data(self, data):
        """Carrega entrada de uma data específica"""
        entrada = self.controller.get_entrada(data)
        if entrada:
            self.titulo_entry.delete(0, "end")
            self.titulo_entry.insert(0, entrada.get("titulo", ""))
            
            self.conteudo_text.delete("1.0", "end")
            self.conteudo_text.insert("1.0", entrada.get("conteudo", ""))
            
            self.humor_var.set(entrada.get("humor", "😊"))
            
            tags = entrada.get("tags", [])
            if tags:
                self.tags_entry.delete(0, "end")
                self.tags_entry.insert(0, ", ".join(tags))
        else:
            # Limpar para nova entrada
            self.titulo_entry.delete(0, "end")
            self.conteudo_text.delete("1.0", "end")
            self.humor_var.set("😊")
            self.tags_entry.delete(0, "end")
    
    def salvar_entrada(self):
        """Salva a entrada atual"""
        titulo = self.titulo_entry.get().strip()
        conteudo = self.conteudo_text.get("1.0", "end-1c").strip()
        humor = self.humor_var.get()
        
        tags_str = self.tags_entry.get().strip()
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
        
        if not titulo:
            messagebox.showwarning("Aviso", "Digite um título para a entrada")
            return
        
        if not conteudo:
            if not messagebox.askyesno("Confirmar", "Deseja salvar uma entrada vazia?"):
                return
        
        self.controller.salvar_entrada(self.data_atual, titulo, conteudo, humor, tags)
        messagebox.showinfo("Sucesso", "Entrada salva no diário!")
    
    def excluir_entrada(self):
        """Exclui a entrada atual"""
        entrada = self.controller.get_entrada(self.data_atual)
        if not entrada:
            messagebox.showwarning("Aviso", "Não há entrada para excluir")
            return
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta entrada?"):
            self.controller.excluir_entrada(self.data_atual)
            self.titulo_entry.delete(0, "end")
            self.conteudo_text.delete("1.0", "end")
            self.humor_var.set("😊")
            self.tags_entry.delete(0, "end")
            messagebox.showinfo("Sucesso", "Entrada excluída!")
    
    def ver_todas_entradas(self):
        """Abre a janela com todas as entradas"""
        todas_window = ctk.CTkToplevel(self)
        todas_window.title("📖 Todas as Entradas")
        todas_window.geometry("800x600")
        
        # Centralizar
        screen_width = todas_window.winfo_screenwidth()
        screen_height = todas_window.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        todas_window.geometry(f"+{x}+{y}")
        
        # Aplicar tema
        tema = self.controller.app.config.get("tema", "dark")
        ctk.set_appearance_mode(tema)
        
        # Frame principal
        main_frame = ctk.CTkFrame(todas_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            main_frame,
            text="📖 Todas as Entradas do Diário",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FF6B8A"
        )
        titulo.pack(pady=(0, 15))
        
        # Busca
        busca_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        busca_frame.pack(fill="x", pady=(0, 15))
        
        busca_entry = ctk.CTkEntry(
            busca_frame,
            placeholder_text="🔍 Buscar entradas...",
            height=35
        )
        busca_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        def buscar():
            termo = busca_entry.get().strip()
            if termo:
                entradas = self.controller.buscar_entradas(termo)
            else:
                entradas = self.controller.get_todas_entradas()
            atualizar_lista(entradas)
        
        ctk.CTkButton(
            busca_frame,
            text="Buscar",
            width=80,
            command=buscar
        ).pack(side="left")
        
        # Lista de entradas
        lista_frame = ctk.CTkScrollableFrame(main_frame)
        lista_frame.pack(fill="both", expand=True)
        
        def atualizar_lista(entradas):
            """Atualiza a lista de entradas"""
            for widget in lista_frame.winfo_children():
                widget.destroy()
            
            if not entradas:
                msg = ctk.CTkLabel(
                    lista_frame,
                    text="📭 Nenhuma entrada encontrada",
                    font=ctk.CTkFont(size=14),
                    text_color="#808080"
                )
                msg.pack(pady=50)
                return
            
            for entrada in entradas:
                card = ctk.CTkFrame(lista_frame, corner_radius=10)
                card.pack(fill="x", pady=5)
                
                # Cabeçalho
                header_frame = ctk.CTkFrame(card, fg_color="transparent")
                header_frame.pack(fill="x", padx=10, pady=10)
                
                # Data e humor
                data_obj = datetime.strptime(entrada["data"], "%Y-%m-%d")
                data_label = ctk.CTkLabel(
                    header_frame,
                    text=f"📅 {data_obj.strftime('%d/%m/%Y')} {entrada.get('humor', '😊')}",
                    font=ctk.CTkFont(size=12),
                    text_color="#808080"
                )
                data_label.pack(side="left")
                
                # Título
                titulo_label = ctk.CTkLabel(
                    card,
                    text=entrada.get("titulo", "Sem título"),
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#FF6B8A"
                )
                titulo_label.pack(anchor="w", padx=10, pady=(0, 5))
                
                # Conteúdo resumido
                conteudo = entrada.get("conteudo", "")
                if len(conteudo) > 100:
                    conteudo = conteudo[:100] + "..."
                conteudo_label = ctk.CTkLabel(
                    card,
                    text=conteudo,
                    font=ctk.CTkFont(size=12),
                    justify="left",
                    wraplength=700
                )
                conteudo_label.pack(anchor="w", padx=10, pady=(0, 10))
                
                # Tags
                tags = entrada.get("tags", [])
                if tags:
                    tags_text = " ".join(tags)
                    tags_label = ctk.CTkLabel(
                        card,
                        text=tags_text,
                        font=ctk.CTkFont(size=10),
                        text_color="#808080"
                    )
                    tags_label.pack(anchor="w", padx=10, pady=(0, 10))
                
                # Botão abrir
                ctk.CTkButton(
                    card,
                    text="📖 Abrir",
                    width=80,
                    command=lambda d=entrada["data"]: self.abrir_entrada(d, todas_window)
                ).pack(anchor="e", padx=10, pady=(0, 10))
        
        # Carregar todas entradas
        entradas = self.controller.get_todas_entradas()
        atualizar_lista(entradas)
        
        # Evento de busca
        busca_entry.bind("<KeyRelease>", lambda e: buscar())
    
    def abrir_entrada(self, data, janela_atual):
        """Abre uma entrada específica"""
        self.data_atual = data
        self.carregar_entrada_data(data)
        janela_atual.destroy()
    
    def fechar(self):
        """Fecha a janela"""
        self.controller.fechar()
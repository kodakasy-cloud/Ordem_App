"""
Interface do módulo de notas
"""
import customtkinter as ctk
from tkinter import messagebox


class NotesView(ctk.CTkToplevel):
    """Janela de gerenciamento de notas"""
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Configurar janela
        self.title("📝 Minhas Anotações")
        self.geometry("900x650")
        
        # Centralizar
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 650) // 2
        self.geometry(f"+{x}+{y}")
        
        # Configurar fechamento
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        
        # Aplicar tema
        tema = self.controller.app.config.get("tema", "dark")
        ctk.set_appearance_mode(tema)
        
        self._setup_ui()
        self.carregar_notas()
    
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
            text="💭 Minhas Anotações",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FF6B8A"
        )
        titulo.pack(side="left")
        
        # Barra de ferramentas
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 15))
        
        # Botão nova nota
        self.nova_btn = ctk.CTkButton(
            toolbar,
            text="✏️ Nova Nota",
            command=self.nova_nota,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.nova_btn.pack(side="left", padx=5)
        
        # Campo de busca
        self.busca_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="🔍 Buscar notas...",
            width=350,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.busca_entry.pack(side="left", padx=10)
        self.busca_entry.bind('<KeyRelease>', self.buscar_notas)
        
        # Botão limpar busca
        self.limpar_btn = ctk.CTkButton(
            toolbar,
            text="✖️",
            width=40,
            height=40,
            command=self.limpar_busca,
            fg_color="#3D3D3D",
            hover_color="#5D5D5D"
        )
        self.limpar_btn.pack(side="left", padx=5)
        
        # Contador de notas
        self.contador_label = ctk.CTkLabel(
            toolbar,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#808080"
        )
        self.contador_label.pack(side="right", padx=10)
        
        # Frame da lista de notas (scrollable)
        self.lista_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.lista_frame.pack(fill="both", expand=True)
    
    def carregar_notas(self):
        """Carrega e exibe as notas"""
        # Limpar lista
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        
        # Carregar notas do controlador
        notas = self.controller.get_notas()
        
        # Atualizar contador
        self.contador_label.configure(text=f"📊 {len(notas)} notas")
        
        if not notas:
            # Mensagem quando não há notas
            self.mostrar_mensagem_vazio()
            return
        
        # Ordenar por data (mais recente primeiro)
        notas_ordenadas = sorted(
            notas, 
            key=lambda x: x.get("atualizado_em", ""), 
            reverse=True
        )
        
        # Criar card para cada nota
        for nota in notas_ordenadas:
            self.criar_card_nota(nota)
    
    def mostrar_mensagem_vazio(self):
        """Mostra mensagem quando não há notas"""
        frame_vazio = ctk.CTkFrame(self.lista_frame, fg_color="transparent")
        frame_vazio.pack(expand=True, fill="both")
        
        icon = ctk.CTkLabel(
            frame_vazio,
            text="📭",
            font=ctk.CTkFont(size=64)
        )
        icon.pack(pady=30)
        
        msg = ctk.CTkLabel(
            frame_vazio,
            text="Nenhuma anotação ainda\nClique em 'Nova Nota' para começar!",
            font=ctk.CTkFont(size=16),
            justify="center",
            text_color="#808080"
        )
        msg.pack(pady=10)
    
    def criar_card_nota(self, nota):
        """Cria um card para exibir uma nota"""
        card = ctk.CTkFrame(
            self.lista_frame,
            corner_radius=15,
            border_width=1,
            border_color="#3D3D3D"
        )
        card.pack(fill="x", padx=10, pady=8)
        
        # Frame do cabeçalho do card
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        # Título
        titulo = ctk.CTkLabel(
            header_frame,
            text=nota.get("titulo", "Sem título"),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FF6B8A"
        )
        titulo.pack(side="left")
        
        # Data
        data_str = nota.get("atualizado_em", "")
        if data_str:
            from datetime import datetime
            try:
                data_obj = datetime.fromisoformat(data_str)
                data_formatada = data_obj.strftime("%d/%m/%Y %H:%M")
            except:
                data_formatada = data_str[:16]
        else:
            data_formatada = "Data desconhecida"
        
        data_label = ctk.CTkLabel(
            header_frame,
            text=f"🕒 {data_formatada}",
            font=ctk.CTkFont(size=11),
            text_color="#808080"
        )
        data_label.pack(side="right")
        
        # Conteúdo (resumido)
        conteudo = nota.get("conteudo", "")
        if len(conteudo) > 150:
            conteudo = conteudo[:150] + "..."
        
        conteudo_label = ctk.CTkLabel(
            card,
            text=conteudo,
            font=ctk.CTkFont(size=13),
            justify="left",
            wraplength=750
        )
        conteudo_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Botões
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        editar_btn = ctk.CTkButton(
            btn_frame,
            text="✏️ Editar",
            width=90,
            height=32,
            font=ctk.CTkFont(size=12),
            command=lambda: self.editar_nota(nota)
        )
        editar_btn.pack(side="left", padx=5)
        
        excluir_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Excluir",
            width=90,
            height=32,
            fg_color="#8B3A3A",
            hover_color="#B04D4D",
            font=ctk.CTkFont(size=12),
            command=lambda: self.excluir_nota(nota.get("id"))
        )
        excluir_btn.pack(side="left", padx=5)
    
    def nova_nota(self):
        """Abre diálogo para criar nova nota"""
        self.abrir_editor()
    
    def editar_nota(self, nota):
        """Abre diálogo para editar nota"""
        self.abrir_editor(nota)
    
    def abrir_editor(self, nota=None):
        """Abre o editor de notas"""
        editor = ctk.CTkToplevel(self)
        editor.title("✏️ Editor de Nota" if nota else "📝 Nova Nota")
        editor.geometry("600x500")
        editor.transient(self)
        editor.grab_set()
        
        # Aplicar tema
        tema = self.controller.app.config.get("tema", "dark")
        ctk.set_appearance_mode(tema)
        
        # Centralizar
        screen_width = editor.winfo_screenwidth()
        screen_height = editor.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 500) // 2
        editor.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(editor, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo_label = ctk.CTkLabel(
            main_frame,
            text="Título da Nota:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        titulo_label.pack(anchor="w", pady=(0, 5))
        
        titulo_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Digite o título...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        titulo_entry.pack(fill="x", pady=(0, 15))
        
        # Conteúdo
        conteudo_label = ctk.CTkLabel(
            main_frame,
            text="Conteúdo:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        conteudo_label.pack(anchor="w", pady=(0, 5))
        
        conteudo_text = ctk.CTkTextbox(
            main_frame,
            height=250,
            font=ctk.CTkFont(size=13)
        )
        conteudo_text.pack(fill="both", expand=True, pady=(0, 20))
        
        # Preencher dados se for edição
        if nota:
            titulo_entry.insert(0, nota.get("titulo", ""))
            conteudo_text.insert("1.0", nota.get("conteudo", ""))
        
        # Botões
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        def salvar():
            titulo = titulo_entry.get().strip()
            conteudo = conteudo_text.get("1.0", "end-1c").strip()
            
            if not titulo:
                messagebox.showwarning("Aviso", "Por favor, digite um título para a nota.")
                return
            
            if nota:
                self.controller.editar_nota(nota.get("id"), titulo, conteudo)
            else:
                self.controller.nova_nota(titulo, conteudo)
            
            self.carregar_notas()
            editor.destroy()
        
        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar",
            command=salvar,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=editor.destroy,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=5)
        
        # Foco no título
        titulo_entry.focus()
    
    def excluir_nota(self, nota_id):
        """Exclui uma nota após confirmação"""
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta nota?"):
            self.controller.excluir_nota(nota_id)
            self.carregar_notas()
    
    def buscar_notas(self, event=None):
        """Busca notas pelo termo digitado"""
        termo = self.busca_entry.get().strip()
        
        if not termo:
            self.carregar_notas()
            return
        
        # Limpar lista
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        
        # Buscar notas
        notas = self.controller.buscar_notas(termo)
        
        if not notas:
            frame_vazio = ctk.CTkFrame(self.lista_frame, fg_color="transparent")
            frame_vazio.pack(expand=True, fill="both")
            
            msg = ctk.CTkLabel(
                frame_vazio,
                text=f"🔍 Nenhuma nota encontrada para '{termo}'",
                font=ctk.CTkFont(size=14),
                text_color="#808080"
            )
            msg.pack(expand=True)
            return
        
        # Criar cards
        for nota in notas:
            self.criar_card_nota(nota)
        
        # Atualizar contador
        self.contador_label.configure(text=f"📊 {len(notas)} resultados")
    
    def limpar_busca(self):
        """Limpa o campo de busca"""
        self.busca_entry.delete(0, "end")
        self.carregar_notas()
    
    def fechar(self):
        """Fecha a janela"""
        self.controller.fechar()
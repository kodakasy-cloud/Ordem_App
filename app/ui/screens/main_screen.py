"""
Tela principal do aplicativo - Dashboard
"""
import customtkinter as ctk
from datetime import datetime
from pathlib import Path
import json
import random
from tkinter import messagebox


class MainScreen(ctk.CTkFrame):
    """Tela principal com dashboard estilo journal/app feminino"""
    
    def __init__(self, app, **kwargs):
        super().__init__(app.root, fg_color="transparent")
        self.app = app
        
        # Configurar cores
        self.cores = self._get_cores()
        
        # Configurar layout
        self._setup_ui()
        
        # Iniciar atualizações
        self.atualizacao_ativa = True
        self.atualizar_relogio()
    
    def _get_cores(self):
        """Retorna cores baseadas no tema atual"""
        tema = self.app.config.get("tema", "dark")
        
        if tema == "dark":
            return {
                "fundo_root": "#0F0F0F",
                "fundo_painel": "#1E1E1E",
                "card_bg": "#2D2D2D",
                "texto_principal": "#FFFFFF",
                "texto_secundario": "#B0B0B0",
                "texto_terciario": "#808080",
                "borda": "#3D3D3D",
                "card_pink": "#2D1A1A",
                "card_blue": "#1A2A3D",
                "card_purple": "#2A1A3D",
                "card_green": "#1A2D1A",
                "card_orange": "#2D2A1A",
                "card_red": "#2D1A1A",
                "btn_pink": "#8B3A5A",
                "btn_blue": "#2A5F8B",
                "btn_purple": "#6A3A8B",
                "btn_green": "#2A8B5A",
                "btn_orange": "#8B6A3A",
                "btn_red": "#8B3A3A",
                "btn_pink_hover": "#B04D73",
                "btn_blue_hover": "#3A7AB0",
                "btn_purple_hover": "#8A4DB0",
                "btn_green_hover": "#3AB073",
                "btn_orange_hover": "#B08A4D",
                "btn_red_hover": "#B04D4D",
                "text_pink": "#FF9AB8",
                "accent": "#FF6B8A",
                "accent_purple": "#9B59B6"
            }
        else:
            return {
                "fundo_root": "#FFF9F9",
                "fundo_painel": "#FFFFFF",
                "card_bg": "#F5F0F0",
                "texto_principal": "#333333",
                "texto_secundario": "#666666",
                "texto_terciario": "#999999",
                "borda": "#FFE0E0",
                "card_pink": "#FFF5F5",
                "card_blue": "#F0F5FF",
                "card_purple": "#F5F0FF",
                "card_green": "#F0FFF5",
                "card_orange": "#FFF5F0",
                "card_red": "#FFF0F0",
                "btn_pink": "#FFB8D0",
                "btn_blue": "#C5E0FF",
                "btn_purple": "#E0C5FF",
                "btn_green": "#C5FFD0",
                "btn_orange": "#FFE0C5",
                "btn_red": "#FFC5C5",
                "btn_pink_hover": "#FF9AB8",
                "btn_blue_hover": "#A8D1FF",
                "btn_purple_hover": "#D0A8FF",
                "btn_green_hover": "#A8FFB8",
                "btn_orange_hover": "#FFD0A8",
                "btn_red_hover": "#FFA8A8",
                "text_pink": "#FF6B8A",
                "accent": "#FF6B8A",
                "accent_purple": "#9B59B6"
            }
    
    def _setup_ui(self):
        """Configura a interface da tela principal"""
        # Frame principal com grid de 3 colunas
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configurar grid
        self.main_frame.grid_columnconfigure(0, weight=1)  # Esquerda
        self.main_frame.grid_columnconfigure(1, weight=4)  # Centro
        self.main_frame.grid_columnconfigure(2, weight=1)  # Direita
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Criar painéis
        self._criar_painel_esquerdo()
        self._criar_painel_central()
        self._criar_painel_direito()
    
    def _criar_painel_esquerdo(self):
        """Painel esquerdo com menus principais"""
        esquerdo_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.cores["fundo_painel"],
            corner_radius=25
        )
        esquerdo_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)
        
        inner_frame = ctk.CTkFrame(esquerdo_frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Título
        titulo = ctk.CTkLabel(
            inner_frame,
            text="✨ MENU ✨",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.cores["text_pink"]
        )
        titulo.pack(pady=(10, 25))
        
        # Botões principais
        botoes = [
            {"icone": "📅", "texto": "Calendário", "desc": "Seus compromissos", "cor": "btn_pink", "modulo": "calendar"},
            {"icone": "💭", "texto": "Anotações", "desc": "Ideias e lembretes", "cor": "btn_blue", "modulo": "notes"},
            {"icone": "💖", "texto": "Diário", "desc": "Seus sentimentos", "cor": "btn_purple", "modulo": "daily"}
        ]
        
        for btn_info in botoes:
            card = ctk.CTkFrame(inner_frame, fg_color=self.cores["card_bg"], corner_radius=15)
            card.pack(fill="x", pady=10)
            
            btn = ctk.CTkButton(
                card,
                text=f"{btn_info['icone']}  {btn_info['texto']}",
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color=self.cores[btn_info["cor"]],
                hover_color=self.cores[f"{btn_info['cor']}_hover"],
                text_color=self.cores["texto_principal"],
                corner_radius=12,
                height=55,
                anchor="w",
                command=lambda m=btn_info["modulo"]: self._abrir_modulo(m)
            )
            btn.pack(fill="both", expand=True, padx=3, pady=3)
            
            desc_label = ctk.CTkLabel(
                card,
                text=btn_info["desc"],
                font=ctk.CTkFont(size=11),
                text_color=self.cores["texto_terciario"]
            )
            desc_label.pack(pady=(0, 8))
    
    def _criar_painel_central(self):
        """Painel central com conteúdo principal"""
        self.central_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.cores["fundo_painel"],
            corner_radius=25
        )
        self.central_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=0)
        
        self._conteudo_inicial()
    
    def _conteudo_inicial(self):
        """Conteúdo inicial do painel central"""
        # Limpar frame
        for widget in self.central_frame.winfo_children():
            widget.destroy()
        
        content = ctk.CTkFrame(self.central_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Ícone
        self.icon_label = ctk.CTkLabel(
            content,
            text="🌸",
            font=ctk.CTkFont(size=64),
            text_color=self.cores["accent"]
        )
        self.icon_label.pack(pady=(30, 10))
        
        # Boas-vindas
        boas_vindas = ctk.CTkLabel(
            content,
            text="Bem-vinda ao seu Cantinho!",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.cores["accent"]
        )
        boas_vindas.pack(pady=10)
        
        # Mensagem
        mensagem = ctk.CTkLabel(
            content,
            text="Organize sua vida com carinho e amor ♡\nAqui você encontra tudo que precisa para\nter dias mais leves e produtivos.",
            font=ctk.CTkFont(size=15),
            text_color=self.cores["texto_secundario"],
            justify="center"
        )
        mensagem.pack(pady=20)
        
        # Dicas do dia
        dicas = [
            ("💡", "Pequenas ações diárias trazem grandes resultados!"),
            ("🌟", "A gratidão transforma o ordinário em extraordinário."),
            ("🌱", "Respire fundo e confie no seu processo."),
            ("💪", "Você é mais forte do que imagina."),
            ("🌞", "Hoje é um novo começo, aproveite!"),
            ("💕", "Seja gentil consigo mesma hoje."),
            ("✨", "Acredite no poder dos seus sonhos."),
            ("🌻", "Cada dia é uma nova oportunidade.")
        ]
        
        dica_escolhida = random.choice(dicas)
        
        dica_frame = ctk.CTkFrame(
            content,
            fg_color=self.cores["card_pink"],
            corner_radius=15
        )
        dica_frame.pack(pady=30, padx=20, fill="x")
        
        dica_titulo = ctk.CTkLabel(
            dica_frame,
            text=f"{dica_escolhida[0]} Dica do Dia {dica_escolhida[0]}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.cores["accent"]
        )
        dica_titulo.pack(pady=(15, 5))
        
        dica_texto = ctk.CTkLabel(
            dica_frame,
            text=dica_escolhida[1],
            font=ctk.CTkFont(size=13),
            text_color=self.cores["texto_secundario"],
            justify="center"
        )
        dica_texto.pack(pady=(0, 15))
        
        # Frase motivacional
        frases = [
            "✨ \"Acredite no poder dos seus sonhos\" ✨",
            "🌟 \"Você é capaz de coisas incríveis\" 🌟",
            "💪 \"Acredite em si mesma\" 💪",
            "🌻 \"Seja a mudança que você quer ver\" 🌻",
            "❤️ \"O amor próprio é o melhor amor\" ❤️",
            "🦋 \"Transforme seus sonhos em realidade\" 🦋"
        ]
        
        frase = ctk.CTkLabel(
            content,
            text=random.choice(frases),
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color=self.cores["texto_terciario"]
        )
        frase.pack(pady=(20, 10))
    
    def _criar_painel_direito(self):
        """Painel direito com opções e status"""
        direito_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.cores["fundo_painel"],
            corner_radius=25
        )
        direito_frame.grid(row=0, column=2, sticky="nsew", padx=(15, 0), pady=0)
        
        inner_frame = ctk.CTkFrame(direito_frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Título
        titulo = ctk.CTkLabel(
            inner_frame,
            text="⚙️ OPÇÕES",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.cores["text_pink"]
        )
        titulo.pack(pady=(10, 25))
        
        # Botões de opções
        botoes = [
            {"icone": "💰", "texto": "Finanças", "desc": "Gastos e metas", "cor": "btn_green", "modulo": "finance"},
            {"icone": "🎨", "texto": "Aparência", "desc": "Personalizar tema", "cor": "btn_orange", "modulo": "theme"},
            {"icone": "⚙️", "texto": "Ajustes", "desc": "Configurações", "cor": "btn_blue", "modulo": "setting"},
            {"icone": "👋", "texto": "Sair", "desc": "Até mais!", "cor": "btn_red", "modulo": "sair"}
        ]
        
        for btn_info in botoes:
            card = ctk.CTkFrame(inner_frame, fg_color=self.cores["card_bg"], corner_radius=15)
            card.pack(fill="x", pady=10)
            
            btn = ctk.CTkButton(
                card,
                text=f"{btn_info['icone']}  {btn_info['texto']}",
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color=self.cores[btn_info["cor"]],
                hover_color=self.cores[f"{btn_info['cor']}_hover"],
                text_color=self.cores["texto_principal"],
                corner_radius=12,
                height=55,
                anchor="w",
                command=lambda m=btn_info["modulo"]: self._abrir_modulo(m)
            )
            btn.pack(fill="both", expand=True, padx=3, pady=3)
            
            desc_label = ctk.CTkLabel(
                card,
                text=btn_info["desc"],
                font=ctk.CTkFont(size=11),
                text_color=self.cores["texto_terciario"]
            )
            desc_label.pack(pady=(0, 8))
        
        # Separador
        separador = ctk.CTkFrame(inner_frame, height=2, fg_color=self.cores["borda"], corner_radius=1)
        separador.pack(fill="x", pady=20)
        
        # Status
        status_label = ctk.CTkLabel(
            inner_frame,
            text="💕 STATUS",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.cores["accent_purple"]
        )
        status_label.pack(pady=(5, 10))
        
        self.status_label = ctk.CTkLabel(
            inner_frame,
            text="Conectada 💚",
            font=ctk.CTkFont(size=13),
            text_color=self.cores["texto_secundario"]
        )
        self.status_label.pack()
        
        # Relógio estilizado
        clock_card = ctk.CTkFrame(inner_frame, fg_color=self.cores["card_bg"], corner_radius=15)
        clock_card.pack(fill="x", pady=15)
        
        self.clock_label = ctk.CTkLabel(
            clock_card,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.cores["accent"]
        )
        self.clock_label.pack(pady=15)
        
        # Decoração
        coracao = ctk.CTkLabel(inner_frame, text="❤️", font=ctk.CTkFont(size=28), text_color=self.cores["accent"])
        coracao.pack(pady=(10, 5))
        
        # Botão tema rápido
        tema_btn = ctk.CTkButton(
            inner_frame,
            text="🌓 Alternar Tema",
            font=ctk.CTkFont(size=12),
            fg_color=self.cores["btn_purple"],
            hover_color=self.cores["btn_purple_hover"],
            height=35,
            command=self.app.alternar_tema
        )
        tema_btn.pack(pady=10)
    
    def _abrir_modulo(self, modulo_nome):
        """Abre um módulo específico"""
        if modulo_nome == "sair":
            if messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
                self.app.fechar()
        elif modulo_nome == "theme":
            self.app.alternar_tema()
        else:
            module = self.app.get_module(modulo_nome)
            if module:
                module.abrir()
                self.app.atualizar_status(f"Abrindo {modulo_nome}")
    
    def atualizar_relogio(self):
        """Atualiza o relógio"""
        if self.atualizacao_ativa and self.winfo_exists():
            try:
                agora = datetime.now().strftime("%H:%M")
                data = datetime.now().strftime("%d/%m")
                dias = {
                    "Monday": "Segunda", "Tuesday": "Terça", "Wednesday": "Quarta",
                    "Thursday": "Quinta", "Friday": "Sexta", "Saturday": "Sábado", "Sunday": "Domingo"
                }
                dia_semana_pt = dias.get(datetime.now().strftime("%A"), "")
                
                self.clock_label.configure(text=f"{agora}\n{data}\n{dia_semana_pt}")
                self.after(1000, self.atualizar_relogio)
            except:
                pass
    
    def atualizar_status(self, mensagem):
        """Atualiza a mensagem de status"""
        if self.winfo_exists():
            self.status_label.configure(text=f"{mensagem} 💕")
            # Reset após 3 segundos
            self.after(3000, lambda: self.status_label.configure(text="Conectada 💚") if self.winfo_exists() else None)
    
    def atualizar_cores(self, tema):
        """Atualiza as cores da interface quando o tema muda"""
        self.cores = self._get_cores()
        # Recarregar toda a interface
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self._setup_ui()
    
    def destroy(self):
        """Destroi a tela e para atualizações"""
        self.atualizacao_ativa = False
        super().destroy()
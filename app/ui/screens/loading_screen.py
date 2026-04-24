"""
Tela de loading - Splash screen
"""
import customtkinter as ctk


class LoadingScreen(ctk.CTkFrame):
    """Tela de carregamento inicial"""
    
    def __init__(self, app, **kwargs):
        super().__init__(app.root, fg_color="transparent")
        self.app = app
        
        self._setup_ui()
        self.carregar()
    
    def _setup_ui(self):
        """Configura a interface de loading"""
        # Frame central
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.pack(expand=True)
        
        # Ícone animado
        self.icon_label = ctk.CTkLabel(
            center_frame,
            text="🌸",
            font=ctk.CTkFont(size=72)
        )
        self.icon_label.pack(pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            center_frame,
            text="Meu Cantinho",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#FF6B8A"
        )
        titulo.pack(pady=10)
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            center_frame,
            text="Seu espaço pessoal de organização",
            font=ctk.CTkFont(size=14),
            text_color="#808080"
        )
        subtitulo.pack(pady=(0, 20))
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(center_frame, width=300, height=10, corner_radius=5)
        self.progress.pack(pady=20)
        self.progress.set(0)
        
        # Status
        self.status_label = ctk.CTkLabel(
            center_frame,
            text="Iniciando...",
            font=ctk.CTkFont(size=12),
            text_color="#999999"
        )
        self.status_label.pack()
        
        # Animar ícone
        self._animar_icone()
    
    def _animar_icone(self, passo=0):
        """Anima o ícone durante o loading"""
        if self.winfo_exists():
            icones = ["🌸", "🌺", "🌸", "🌷"]
            self.icon_label.configure(text=icones[passo % len(icones)])
            self.after(500, lambda: self._animar_icone(passo + 1))
    
    def carregar(self, progresso=0):
        """Simula carregamento com diferentes etapas"""
        etapas = [
            (0.2, "Carregando módulos..."),
            (0.4, "Configurando interface..."),
            (0.6, "Preparando dados..."),
            (0.8, "Quase lá..."),
            (1.0, "Concluído!")
        ]
        
        if progresso <= 1:
            self.progress.set(progresso)
            
            # Atualizar status baseado no progresso
            for p, texto in etapas:
                if progresso <= p:
                    self.status_label.configure(text=texto)
                    break
            
            self.after(20, lambda: self.carregar(progresso + 0.02))
        else:
            # Carregamento completo, ir para tela principal
            self.after(500, lambda: self.app.router.navegar("main"))
    
    def destroy(self):
        """Destroi a tela"""
        super().destroy()
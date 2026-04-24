"""
Componente de sidebar reutilizável para navegação
"""
import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    """
    Sidebar com menu de navegação
    Pode ser usado em diferentes telas
    """
    
    def __init__(self, parent, app, width=250, **kwargs):
        """
        Inicializa a sidebar
        
        Args:
            parent: Widget pai
            app: Instância da aplicação
            width: Largura da sidebar
        """
        super().__init__(parent, width=width, corner_radius=0, **kwargs)
        self.app = app
        
        # Configurar largura mínima/máxima
        self.grid_propagate(False)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface da sidebar"""
        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="🌸 Meu Cantinho",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FF6B8A"
        )
        self.titulo.pack(pady=(30, 20))
        
        # Separador
        separador = ctk.CTkFrame(self, height=2, fg_color="#3D3D3D")
        separador.pack(fill="x", padx=15, pady=10)
        
        # Menu
        self.menu_items = {}
        self._criar_menu()
        
        # Versão
        self.version_label = ctk.CTkLabel(
            self,
            text="Versão 1.0.0",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        )
        self.version_label.pack(side="bottom", pady=10)
    
    def _criar_menu(self):
        """Cria os itens do menu"""
        itens = [
            ("🏠", "Início", "main"),
            ("📅", "Calendário", "calendar"),
            ("💭", "Anotações", "notes"),
            ("💖", "Diário", "daily"),
            ("💰", "Finanças", "finance"),
            ("⚙️", "Configurações", "settings")
        ]
        
        for icon, text, route in itens:
            btn = ctk.CTkButton(
                self,
                text=f"{icon}  {text}",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                hover_color="#3D3D3D",
                anchor="w",
                height=45,
                corner_radius=10,
                command=lambda r=route: self._navegar(r)
            )
            btn.pack(fill="x", padx=15, pady=5)
            self.menu_items[route] = btn
        
        # Separador antes do botão sair
        separador = ctk.CTkFrame(self, height=2, fg_color="#3D3D3D")
        separador.pack(fill="x", padx=15, pady=20)
        
        # Botão sair
        self.sair_btn = ctk.CTkButton(
            self,
            text="🚪  Sair",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#8B3A3A",
            hover_color="#B04D4D",
            height=45,
            corner_radius=10,
            command=self.app.fechar
        )
        self.sair_btn.pack(fill="x", padx=15, pady=10)
    
    def _navegar(self, route):
        """Navega para a rota especificada"""
        self.app.router.navegar(route)
        self._destacar_item(route)
    
    def _destacar_item(self, route_ativo):
        """Destaca o item do menu ativo"""
        for route, btn in self.menu_items.items():
            if route == route_ativo:
                btn.configure(fg_color="#3D3D3D")
            else:
                btn.configure(fg_color="transparent")
    
    def set_ativo(self, route):
        """Define qual item do menu está ativo"""
        self._destacar_item(route)
    
    def collapse(self):
        """Recolhe a sidebar (para uso futuro)"""
        # Implementar animação de colapso se necessário
        pass
    
    def expand(self):
        """Expande a sidebar (para uso futuro)"""
        pass
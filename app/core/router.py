"""
Roteador - Gerencia navegação entre telas
"""
from typing import Optional
import customtkinter as ctk


class Router:
    """Gerencia a navegação entre diferentes telas da aplicação"""
    
    def __init__(self, app):
        self.app = app
        self.screens = {}
        self.current_screen = None
        self.main_container = None
        self.history = []  # Histórico de navegação
        
        # Configurar container principal
        self._setup_container()
        
        # Registrar telas
        self._register_screens()
    
    def _setup_container(self):
        """Configura o container principal para as telas"""
        # Criar frame principal que ocupará toda a janela
        self.main_container = ctk.CTkFrame(self.app.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
    
    def _register_screens(self):
        """Registra todas as telas disponíveis"""
        from app.ui.screens.main_screen import MainScreen
        from app.ui.screens.loading_screen import LoadingScreen
        
        self.screens = {
            'main': MainScreen,
            'loading': LoadingScreen
        }
    
    def navegar(self, screen_name: str, **kwargs):
        """
        Navega para uma tela específica
        
        Args:
            screen_name: Nome da tela ('main', 'loading', etc)
            **kwargs: Argumentos adicionais para a tela
        """
        if screen_name not in self.screens:
            print(f"⚠️ Tela '{screen_name}' não encontrada")
            return
        
        # Salvar no histórico (evitar duplicatas consecutivas)
        if not self.history or self.history[-1] != screen_name:
            self.history.append(screen_name)
        
        # Limitar tamanho do histórico
        if len(self.history) > 10:
            self.history.pop(0)
        
        # Limpar tela atual
        if self.current_screen:
            try:
                self.current_screen.destroy()
            except:
                pass
        
        # Criar nova tela
        screen_class = self.screens[screen_name]
        self.current_screen = screen_class(self.app, **kwargs)
        
        # Exibir tela no container
        self.current_screen.pack(fill="both", expand=True)
        
        # Atualizar título da janela se necessário
        self._atualizar_titulo(screen_name)
    
    def _atualizar_titulo(self, screen_name: str):
        """Atualiza o título da janela baseado na tela"""
        titulos = {
            'main': "🌸 Meu Cantinho",
            'loading': "🔄 Carregando..."
        }
        titulo = titulos.get(screen_name, "🌸 Meu Cantinho")
        self.app.root.title(titulo)
    
    def voltar(self):
        """Volta para a tela anterior"""
        if len(self.history) >= 2:
            # Remove tela atual
            self.history.pop()
            # Volta para a anterior
            tela_anterior = self.history[-1]
            self.navegar(tela_anterior)
        else:
            print("⚠️ Não há tela anterior no histórico")
    
    def limpar_historico(self):
        """Limpa o histórico de navegação"""
        self.history = []
    
    def recarregar_tela_atual(self):
        """Recarrega a tela atual"""
        if self.current_screen:
            screen_name = self.history[-1] if self.history else 'main'
            self.navegar(screen_name)
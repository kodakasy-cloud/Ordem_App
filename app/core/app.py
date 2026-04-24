"""
Nucleo da aplicacao - Gerencia o ciclo de vida
"""
import customtkinter as ctk
from pathlib import Path
import json
from datetime import datetime

from app.core.router import Router
from app.services.storage import StorageService


class App:
    """Classe principal da aplicacao"""
    
    def __init__(self, root):
        """
        Inicializa a aplicacao
        
        Args:
            root: Janela root do CustomTkinter
        """
        self.root = root
        self.root.title("Meu Cantinho")
        
        # Configurar tamanho da janela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.window_width = 1200
        self.window_height = 750
        
        # Centralizar janela
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        
        # Configurar minimo da janela
        self.root.minsize(900, 600)
        
        # Icone da janela (se tiver)
        icon_path = Path(__file__).parent.parent / "assets" / "icon.ico"
        if icon_path.exists():
            try:
                self.root.iconbitmap(str(icon_path))
            except:
                pass
        
        # Inicializar servicos
        self.storage = StorageService()
        
        # Carregar configuracoes
        self.config = self.storage.carregar_config()
        
        # Aplicar tema salvo
        tema = self.config.get("tema", "dark")
        ctk.set_appearance_mode(tema)
        
        # Inicializar roteador
        self.router = Router(self)
        
        # Controladores dos modulos
        self.modules = {}
        
        # Estado da aplicacao
        self.running = True
        self.atualizacao_ativa = True
        
        # Configurar evento de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)
        
        # Inicializar modulos
        self._inicializar_modulos()
        
        # Carregar tela principal
        self.router.navegar("main")
    
    def _inicializar_modulos(self):
        """Inicializa todos os modulos da aplicacao"""
        from app.modules.calendar.controller import CalendarController
        from app.modules.notes.controller import NotesController
        from app.modules.daily.controller import DailyController
        from app.modules.finance.controller import FinanceController
        from app.modules.setting.controller import SettingController
        
        self.modules = {
            'calendar': CalendarController(self),
            'notes': NotesController(self),
            'daily': DailyController(self),
            'finance': FinanceController(self),
            'setting': SettingController(self)
        }
    
    def get_module(self, name):
        """Retorna um modulo pelo nome"""
        return self.modules.get(name)
    
    def run(self):
        """Inicia o loop principal da aplicacao"""
        try:
            print("Aplicacao iniciada com sucesso!")
            self.root.mainloop()
        except Exception as e:
            print(f"Erro no loop principal: {e}")
    
    def fechar(self):
        """Fecha a aplicacao de forma segura"""
        print("Salvando dados e encerrando...")
        self.running = False
        self.atualizacao_ativa = False
        
        # Salvar dados de todos os modulos
        for module in self.modules.values():
            try:
                if hasattr(module, 'salvar_dados'):
                    module.salvar_dados()
            except Exception as e:
                print(f"Erro ao salvar dados do modulo: {e}")
        
        # Salvar configuracoes
        self.storage.salvar_config(self.config)
        
        # Fechar janelas secundarias
        for module in self.modules.values():
            try:
                if hasattr(module, 'fechar'):
                    module.fechar()
            except Exception as e:
                print(f"Erro ao fechar modulo: {e}")
        
        # Destruir janela principal
        try:
            self.root.destroy()
        except:
            pass
        
        print("Aplicacao encerrada com sucesso! Ate mais!")
    
    def atualizar_status(self, mensagem):
        """Atualiza mensagem de status na interface"""
        # Verifica se o router e a tela atual existem
        if hasattr(self.router, 'current_screen') and self.router.current_screen:
            # Verifica se a tela atual tem o metodo atualizar_status
            if hasattr(self.router.current_screen, 'atualizar_status'):
                self.router.current_screen.atualizar_status(mensagem)
    
    def alternar_tema(self):
        """Alterna entre tema claro e escuro"""
        novo_tema = "light" if ctk.get_appearance_mode() == "Dark" else "dark"
        ctk.set_appearance_mode(novo_tema)
        self.config["tema"] = novo_tema
        self.storage.salvar_config(self.config)
        
        # Recarregar tela para aplicar novas cores
        if hasattr(self.router, 'current_screen') and self.router.current_screen:
            if hasattr(self.router.current_screen, 'atualizar_cores'):
                self.router.current_screen.atualizar_cores(novo_tema)
        
        self.atualizar_status(f"Tema {novo_tema} ativado")
"""
Controlador do módulo de configurações
"""
from .model import SettingModel
from .view import SettingsView


class SettingController:
    """Controla as ações do módulo de configurações"""
    
    def __init__(self, app):
        self.app = app
        self.model = SettingModel(app)
        self.view = None
        self.janela = None
    
    def abrir(self):
        """Abre a janela do módulo"""
        if self.janela and self.janela.winfo_exists():
            self.janela.lift()
            return
        
        self.janela = self.view = SettingsView(self)
        self.app.atualizar_status("Configurações abertas")
    
    def fechar(self):
        """Fecha a janela do módulo"""
        if self.janela and self.janela.winfo_exists():
            self.janela.destroy()
        self.janela = None
        self.view = None
    
    def salvar_dados(self):
        """Salva dados do módulo"""
        self.model.salvar_dados()
    
    def get_config(self, key: str, default=None):
        """Retorna uma configuração"""
        return self.model.get_config(key, default)
    
    def set_config(self, key: str, value):
        """Define uma configuração"""
        self.model.set_config(key, value)
    
    def alternar_tema(self):
        """Alterna o tema"""
        novo_tema = self.model.alternar_tema()
        self.app.alternar_tema()
        return novo_tema
    
    def fazer_backup(self):
        """Faz backup"""
        return self.model.fazer_backup()
    
    def limpar_dados(self):
        """Limpa dados"""
        return self.model.limpar_dados()
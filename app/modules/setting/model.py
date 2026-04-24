"""
Modelo de dados para o módulo de configurações
"""
from typing import Dict


class SettingModel:
    """Gerencia as configurações do aplicativo"""
    
    def __init__(self, app):
        self.app = app
        self.config = {}
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega configurações"""
        self.config = self.app.storage.carregar_config()
        
        # Garantir valores padrão
        if "tema" not in self.config:
            self.config["tema"] = "dark"
        if "notificacoes" not in self.config:
            self.config["notificacoes"] = True
        if "backup_automatico" not in self.config:
            self.config["backup_automatico"] = False
        if "idioma" not in self.config:
            self.config["idioma"] = "pt-BR"
        if "primeira_vez" not in self.config:
            self.config["primeira_vez"] = True
    
    def salvar_dados(self):
        """Salva configurações"""
        self.app.storage.salvar_config(self.config)
        # Aplicar tema imediatamente
        import customtkinter as ctk
        ctk.set_appearance_mode(self.config.get("tema", "dark"))
    
    def get_config(self, key: str, default=None):
        """Retorna uma configuração específica"""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value):
        """Define uma configuração"""
        self.config[key] = value
        self.salvar_dados()
    
    def alternar_tema(self):
        """Alterna entre tema claro e escuro"""
        novo_tema = "light" if self.config.get("tema") == "dark" else "dark"
        self.set_config("tema", novo_tema)
        return novo_tema
    
    def fazer_backup(self):
        """Faz backup dos dados"""
        return self.app.storage.backup()
    
    def limpar_dados(self):
        """Limpa todos os dados (exceto configurações)"""
        return self.app.storage.limpar_dados(confirmar=True)
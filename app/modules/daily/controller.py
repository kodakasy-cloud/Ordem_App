"""
Controlador do módulo de diário
"""
from typing import List, Optional
from .model import DailyModel
from .view import DailyView


class DailyController:
    """Controla as ações do módulo de diário"""
    
    def __init__(self, app):
        self.app = app
        self.model = DailyModel(app)
        self.view = None
        self.janela = None
    
    def abrir(self):
        """Abre a janela do módulo"""
        if self.janela and self.janela.winfo_exists():
            self.janela.lift()
            return
        
        self.janela = self.view = DailyView(self)
        self.app.atualizar_status("Diário aberto")
    
    def fechar(self):
        """Fecha a janela do módulo"""
        if self.janela and self.janela.winfo_exists():
            self.janela.destroy()
        self.janela = None
        self.view = None
    
    def salvar_dados(self):
        """Salva dados do módulo"""
        self.model.salvar_dados()
    
    def get_entrada_hoje(self):
        """Retorna entrada de hoje"""
        from datetime import datetime
        hoje = datetime.now().strftime("%Y-%m-%d")
        return self.model.get_entrada(hoje)
    
    def get_entrada(self, data: str) -> Optional[dict]:
        """Retorna entrada de uma data"""
        return self.model.get_entrada(data)
    
    def get_todas_entradas(self) -> List[dict]:
        """Retorna todas as entradas"""
        return self.model.get_todas_entradas()
    
    def salvar_entrada(self, data: str, titulo: str, conteudo: str, 
                      humor: str = "😊", tags: List[str] = None):
        """Salva uma entrada"""
        if tags is None:
            tags = []
            
        if self.model.get_entrada(data):
            self.model.atualizar_entrada(data, titulo=titulo, conteudo=conteudo, 
                                        humor=humor, tags=tags)
            self.app.atualizar_status("Entrada atualizada!")
        else:
            self.model.adicionar_entrada(data, titulo, conteudo, humor, tags)
            self.app.atualizar_status("Entrada salva no diário!")
    
    def excluir_entrada(self, data: str):
        """Exclui uma entrada"""
        self.model.excluir_entrada(data)
        self.app.atualizar_status("Entrada excluída")
    
    def buscar_entradas(self, termo: str) -> List[dict]:
        """Busca entradas"""
        return self.model.buscar_entradas(termo)
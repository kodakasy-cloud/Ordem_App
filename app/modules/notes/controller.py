"""
Controlador do módulo de notas
"""
from .model import NotesModel
from .view import NotesView


class NotesController:
    """Controla as ações do módulo de notas"""
    
    def __init__(self, app):
        self.app = app
        self.model = NotesModel(app)
        self.view = None
        self.janela = None
    
    def abrir(self):
        """Abre a janela do módulo"""
        if self.janela and self.janela.winfo_exists():
            self.janela.lift()
            return
        
        self.janela = self.view = NotesView(self)
        self.app.atualizar_status("Anotações abertas")
    
    def fechar(self):
        """Fecha a janela do módulo"""
        if self.janela and self.janela.winfo_exists():
            self.janela.destroy()
        self.janela = None
        self.view = None
    
    def salvar_dados(self):
        """Salva dados do módulo"""
        self.model.salvar_dados()
    
    def get_notas(self):
        """Retorna todas as notas"""
        return self.model.get_todas_notas()
    
    def nova_nota(self, titulo: str, conteudo: str):
        """Cria uma nova nota"""
        nota_id = self.model.adicionar_nota(titulo, conteudo)
        self.app.atualizar_status("Nota criada com sucesso!")
        return nota_id
    
    def editar_nota(self, nota_id: str, titulo: str, conteudo: str):
        """Edita uma nota existente"""
        self.model.atualizar_nota(nota_id, titulo, conteudo)
        self.app.atualizar_status("Nota atualizada!")
    
    def excluir_nota(self, nota_id: str):
        """Exclui uma nota"""
        self.model.excluir_nota(nota_id)
        self.app.atualizar_status("Nota excluída")
    
    def buscar_notas(self, termo: str):
        """Busca notas"""
        return self.model.buscar_notas(termo)
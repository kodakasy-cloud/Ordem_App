"""
Controlador do módulo de calendário
"""
from .model import CalendarModel
from .view import CalendarView


class CalendarController:
    """Controla as ações do módulo de calendário"""
    
    def __init__(self, app):
        self.app = app
        self.model = CalendarModel(app)
        self.view = None
        self.janela = None
    
    def abrir(self):
        """Abre a janela do módulo"""
        if self.janela and self.janela.winfo_exists():
            self.janela.lift()
            return
        
        self.janela = self.view = CalendarView(self)
        self.app.atualizar_status("Calendário aberto")
    
    def fechar(self):
        """Fecha a janela do módulo"""
        if self.janela and self.janela.winfo_exists():
            self.janela.destroy()
        self.janela = None
        self.view = None
    
    def salvar_dados(self):
        """Salva dados do módulo"""
        self.model.salvar_dados()
    
    def get_eventos_data(self, data: str):
        """Retorna eventos de uma data"""
        return self.model.get_eventos_data(data)
    
    def get_eventos_mes(self, ano: int, mes: int):
        """Retorna eventos de um mês"""
        return self.model.get_eventos_mes(ano, mes)
    
    def adicionar_evento(self, titulo: str, data: str, hora: str = "", 
                        descricao: str = "", cor: str = "#FF6B8A"):
        """Adiciona um novo evento"""
        evento_id = self.model.adicionar_evento(titulo, data, hora, descricao, cor)
        self.app.atualizar_status(f"Evento '{titulo}' criado!")
        return evento_id
    
    def editar_evento(self, evento_id: str, **kwargs):
        """Edita um evento"""
        if self.model.atualizar_evento(evento_id, **kwargs):
            self.app.atualizar_status("Evento atualizado!")
            return True
        return False
    
    def excluir_evento(self, evento_id: str):
        """Exclui um evento"""
        self.model.excluir_evento(evento_id)
        self.app.atualizar_status("Evento excluído")
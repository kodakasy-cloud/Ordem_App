"""
Controlador do módulo de finanças
"""
from .model import FinanceModel
from .view import FinanceView


class FinanceController:
    """Controla as ações do módulo de finanças"""
    
    def __init__(self, app):
        self.app = app
        self.model = FinanceModel(app)
        self.view = None
        self.janela = None
    
    def abrir(self):
        """Abre a janela do módulo"""
        if self.janela and self.janela.winfo_exists():
            self.janela.lift()
            return
        
        self.janela = self.view = FinanceView(self)
        self.app.atualizar_status("Finanças abertas")
    
    def fechar(self):
        """Fecha a janela do módulo"""
        if self.janela and self.janela.winfo_exists():
            self.janela.destroy()
        self.janela = None
        self.view = None
    
    def salvar_dados(self):
        """Salva dados do módulo"""
        self.model.salvar_dados()
    
    def adicionar_transacao(self, tipo: str, valor: float, categoria: str, descricao: str):
        """Adiciona transação"""
        transacao_id = self.model.adicionar_transacao(tipo, valor, categoria, descricao)
        self.app.atualizar_status(f"{'Receita' if tipo == 'receita' else 'Despesa'} adicionada!")
        return transacao_id
    
    def excluir_transacao(self, transacao_id: str):
        """Exclui transação"""
        self.model.excluir_transacao(transacao_id)
        self.app.atualizar_status("Transação excluída")
    
    def get_transacoes(self, mes: int = None, ano: int = None):
        """Retorna transações"""
        return self.model.get_transacoes(mes, ano)
    
    def get_saldo(self, mes: int = None, ano: int = None):
        """Retorna saldo"""
        return self.model.get_saldo(mes, ano)
    
    def get_total_receitas(self, mes: int = None, ano: int = None):
        """Retorna total de receitas"""
        return self.model.get_total_receitas(mes, ano)
    
    def get_total_despesas(self, mes: int = None, ano: int = None):
        """Retorna total de despesas"""
        return self.model.get_total_despesas(mes, ano)
    
    def get_despesas_por_categoria(self, mes: int = None, ano: int = None):
        """Retorna despesas por categoria"""
        return self.model.get_despesas_por_categoria(mes, ano)
    
    def get_categorias(self):
        """Retorna categorias"""
        return self.model.get_categorias()
    
    def adicionar_categoria(self, categoria: str):
        """Adiciona categoria"""
        self.model.adicionar_categoria(categoria)
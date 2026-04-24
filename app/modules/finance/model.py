"""
Modelo de dados para o módulo de finanças
"""
from datetime import datetime
from typing import Dict, List, Optional


class FinanceModel:
    """Gerencia os dados financeiros"""
    
    def __init__(self, app):
        self.app = app
        self.transacoes: List[Dict] = []
        self.categorias = ["Alimentação", "Transporte", "Moradia", "Saúde", 
                          "Educação", "Lazer", "Roupas", "Outros"]
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega dados financeiros"""
        dados = self.app.storage.carregar_financas()
        self.transacoes = dados.get("transacoes", [])
        self.categorias = dados.get("categorias", self.categorias)
    
    def salvar_dados(self):
        """Salva dados financeiros"""
        dados = {
            "transacoes": self.transacoes,
            "categorias": self.categorias
        }
        self.app.storage.salvar_financas(dados)
    
    def adicionar_transacao(self, tipo: str, valor: float, categoria: str, 
                           descricao: str, data: str = None) -> str:
        """Adiciona uma transação (receita/despesa)"""
        from utils.helpers import gerar_id
        
        if not data:
            data = datetime.now().strftime("%Y-%m-%d")
        
        transacao = {
            "id": gerar_id(),
            "tipo": tipo,  # "receita" ou "despesa"
            "valor": valor,
            "categoria": categoria,
            "descricao": descricao,
            "data": data,
            "criado_em": datetime.now().isoformat()
        }
        self.transacoes.append(transacao)
        self.salvar_dados()
        return transacao["id"]
    
    def excluir_transacao(self, transacao_id: str):
        """Exclui uma transação"""
        self.transacoes = [t for t in self.transacoes if t["id"] != transacao_id]
        self.salvar_dados()
    
    def get_transacoes(self, mes: int = None, ano: int = None) -> List[Dict]:
        """Retorna transações filtradas por mês/ano"""
        if not mes and not ano:
            return sorted(self.transacoes, key=lambda x: x["data"], reverse=True)
        
        resultado = []
        for t in self.transacoes:
            data_obj = datetime.strptime(t["data"], "%Y-%m-%d")
            if mes and data_obj.month != mes:
                continue
            if ano and data_obj.year != ano:
                continue
            resultado.append(t)
        
        return sorted(resultado, key=lambda x: x["data"], reverse=True)
    
    def get_saldo(self, mes: int = None, ano: int = None) -> float:
        """Calcula o saldo"""
        transacoes = self.get_transacoes(mes, ano)
        receitas = sum(t["valor"] for t in transacoes if t["tipo"] == "receita")
        despesas = sum(t["valor"] for t in transacoes if t["tipo"] == "despesa")
        return receitas - despesas
    
    def get_total_receitas(self, mes: int = None, ano: int = None) -> float:
        """Total de receitas"""
        transacoes = self.get_transacoes(mes, ano)
        return sum(t["valor"] for t in transacoes if t["tipo"] == "receita")
    
    def get_total_despesas(self, mes: int = None, ano: int = None) -> float:
        """Total de despesas"""
        transacoes = self.get_transacoes(mes, ano)
        return sum(t["valor"] for t in transacoes if t["tipo"] == "despesa")
    
    def get_despesas_por_categoria(self, mes: int = None, ano: int = None) -> Dict:
        """Despesas agrupadas por categoria"""
        transacoes = self.get_transacoes(mes, ano)
        despesas_por_categoria = {}
        
        for t in transacoes:
            if t["tipo"] == "despesa":
                categoria = t["categoria"]
                despesas_por_categoria[categoria] = despesas_por_categoria.get(categoria, 0) + t["valor"]
        
        return despesas_por_categoria
    
    def adicionar_categoria(self, categoria: str):
        """Adiciona uma nova categoria"""
        if categoria not in self.categorias:
            self.categorias.append(categoria)
            self.salvar_dados()
    
    def get_categorias(self) -> List[str]:
        """Retorna lista de categorias"""
        return self.categorias
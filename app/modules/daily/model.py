"""
Modelo de dados para o módulo de diário
"""
from datetime import datetime
from typing import Dict, List, Optional


class DailyModel:
    """Gerencia as entradas do diário"""
    
    def __init__(self, app):
        self.app = app
        self.entradas: Dict[str, Dict] = {}
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega entradas do diário"""
        dados = self.app.storage.carregar_diario()
        self.entradas = dados if isinstance(dados, dict) else {}
    
    def salvar_dados(self):
        """Salva entradas do diário"""
        self.app.storage.salvar_diario(self.entradas)
    
    def adicionar_entrada(self, data: str, titulo: str, conteudo: str, 
                         humor: str = "😊", tags: List[str] = None) -> str:
        """Adiciona uma entrada no diário"""
        if not tags:
            tags = []
        
        entrada = {
            "data": data,
            "titulo": titulo,
            "conteudo": conteudo,
            "humor": humor,
            "tags": tags,
            "criado_em": datetime.now().isoformat()
        }
        self.entradas[data] = entrada
        self.salvar_dados()
        return data
    
    def atualizar_entrada(self, data: str, **kwargs):
        """Atualiza uma entrada existente"""
        if data in self.entradas:
            self.entradas[data].update(kwargs)
            self.entradas[data]["atualizado_em"] = datetime.now().isoformat()
            self.salvar_dados()
            return True
        return False
    
    def excluir_entrada(self, data: str):
        """Exclui uma entrada"""
        if data in self.entradas:
            del self.entradas[data]
            self.salvar_dados()
    
    def get_entrada(self, data: str) -> Optional[Dict]:
        """Retorna uma entrada específica"""
        return self.entradas.get(data)
    
    def get_todas_entradas(self) -> List[Dict]:
        """Retorna todas as entradas ordenadas por data"""
        entradas_lista = list(self.entradas.values())
        return sorted(entradas_lista, key=lambda x: x["data"], reverse=True)
    
    def get_entradas_mes(self, ano: int, mes: int) -> List[Dict]:
        """Retorna entradas de um mês específico"""
        mes_str = f"{ano:04d}-{mes:02d}"
        resultado = []
        for data, entrada in self.entradas.items():
            if data.startswith(mes_str):
                resultado.append(entrada)
        return sorted(resultado, key=lambda x: x["data"], reverse=True)
    
    def buscar_entradas(self, termo: str) -> List[Dict]:
        """Busca entradas por termo"""
        termo = termo.lower()
        resultado = []
        for entrada in self.entradas.values():
            if (termo in entrada["titulo"].lower() or 
                termo in entrada["conteudo"].lower()):
                resultado.append(entrada)
        return sorted(resultado, key=lambda x: x["data"], reverse=True)
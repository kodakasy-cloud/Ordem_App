"""
Modelo de dados para o módulo de notas
"""
from datetime import datetime
from typing import Dict, List
import json


class NotesModel:
    """Gerencia os dados das notas"""
    
    def __init__(self, app):
        self.app = app
        self.notas: Dict[str, Dict] = {}
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega notas do armazenamento"""
        dados = self.app.storage.carregar_notas()
        self.notas = dados if isinstance(dados, dict) else {}
    
    def salvar_dados(self):
        """Salva notas no armazenamento"""
        self.app.storage.salvar_notas(self.notas)
    
    def adicionar_nota(self, titulo: str, conteudo: str) -> str:
        """Adiciona uma nova nota"""
        from utils.helpers import gerar_id
        nota_id = gerar_id()
        
        self.notas[nota_id] = {
            "id": nota_id,
            "titulo": titulo,
            "conteudo": conteudo,
            "criado_em": datetime.now().isoformat(),
            "atualizado_em": datetime.now().isoformat()
        }
        self.salvar_dados()
        return nota_id
    
    def atualizar_nota(self, nota_id: str, titulo: str, conteudo: str):
        """Atualiza uma nota existente"""
        if nota_id in self.notas:
            self.notas[nota_id]["titulo"] = titulo
            self.notas[nota_id]["conteudo"] = conteudo
            self.notas[nota_id]["atualizado_em"] = datetime.now().isoformat()
            self.salvar_dados()
    
    def excluir_nota(self, nota_id: str):
        """Exclui uma nota"""
        if nota_id in self.notas:
            del self.notas[nota_id]
            self.salvar_dados()
    
    def get_todas_notas(self) -> List[Dict]:
        """Retorna todas as notas"""
        return list(self.notas.values())
    
    def get_nota(self, nota_id: str) -> Dict:
        """Retorna uma nota específica"""
        return self.notas.get(nota_id, {})
    
    def buscar_notas(self, termo: str) -> List[Dict]:
        """Busca notas por termo"""
        termo = termo.lower()
        resultado = []
        for nota in self.notas.values():
            if termo in nota["titulo"].lower() or termo in nota["conteudo"].lower():
                resultado.append(nota)
        return resultado
"""
Modelo de dados para o módulo de calendário
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json


class CalendarModel:
    """Gerencia os eventos do calendário"""
    
    def __init__(self, app):
        self.app = app
        self.eventos: List[Dict] = []
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega eventos do armazenamento"""
        dados = self.app.storage.carregar_calendario()
        self.eventos = dados.get("eventos", [])
    
    def salvar_dados(self):
        """Salva eventos no armazenamento"""
        dados = {"eventos": self.eventos}
        self.app.storage.salvar_calendario(dados)
    
    def adicionar_evento(self, titulo: str, data: str, hora: str = "", 
                        descricao: str = "", cor: str = "#FF6B8A") -> str:
        """Adiciona um novo evento"""
        from utils.helpers import gerar_id
        evento_id = gerar_id()
        
        evento = {
            "id": evento_id,
            "titulo": titulo,
            "data": data,
            "hora": hora,
            "descricao": descricao,
            "cor": cor,
            "criado_em": datetime.now().isoformat()
        }
        self.eventos.append(evento)
        self.salvar_dados()
        return evento_id
    
    def atualizar_evento(self, evento_id: str, **kwargs):
        """Atualiza um evento existente"""
        for evento in self.eventos:
            if evento["id"] == evento_id:
                evento.update(kwargs)
                evento["atualizado_em"] = datetime.now().isoformat()
                self.salvar_dados()
                return True
        return False
    
    def excluir_evento(self, evento_id: str):
        """Exclui um evento"""
        self.eventos = [e for e in self.eventos if e["id"] != evento_id]
        self.salvar_dados()
    
    def get_eventos_data(self, data: str) -> List[Dict]:
        """Retorna eventos de uma data específica"""
        return [e for e in self.eventos if e["data"] == data]
    
    def get_eventos_mes(self, ano: int, mes: int) -> List[Dict]:
        """Retorna eventos de um mês específico"""
        mes_str = f"{ano:04d}-{mes:02d}"
        return [e for e in self.eventos if e["data"].startswith(mes_str)]
    
    def get_todos_eventos(self) -> List[Dict]:
        """Retorna todos os eventos"""
        return sorted(self.eventos, key=lambda x: x["data"])
    
    def get_evento(self, evento_id: str) -> Optional[Dict]:
        """Retorna um evento específico"""
        for evento in self.eventos:
            if evento["id"] == evento_id:
                return evento
        return None
"""
Sistema de roteamento entre módulos
Gerencia a navegação e comunicação entre os diferentes módulos
"""

from typing import Dict, Any, Optional
from pathlib import Path


class Router:
    """Gerencia a navegação entre módulos"""
    
    def __init__(self):
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.current_module: Optional[str] = None
        self.history: list = []
    
    def register_module(self, module_id: str, module_info: Dict[str, Any]):
        """
        Registra um módulo no router
        
        Args:
            module_id: Identificador único do módulo
            module_info: Dicionário com informações do módulo
        """
        if module_id in self.modules:
            raise ValueError(f"Módulo '{module_id}' já está registrado")
        
        self.modules[module_id] = module_info
    
    def unregister_module(self, module_id: str):
        """Remove um módulo do router"""
        if module_id in self.modules:
            del self.modules[module_id]
    
    def get_module(self, module_id: str) -> Optional[Dict[str, Any]]:
        """Retorna as informações de um módulo"""
        return self.modules.get(module_id)
    
    def get_module_controller(self, module_id: str) -> Optional[Any]:
        """Retorna o controlador de um módulo"""
        module = self.get_module(module_id)
        if module:
            return module.get("controller")
        return None
    
    def get_module_info(self, module_id: str) -> Dict[str, Any]:
        """Retorna informações básicas do módulo"""
        module = self.get_module(module_id)
        if module:
            return {
                "name": module.get("name", module_id),
                "icon": module.get("icon", "📦"),
                "color": module.get("color", "#95a5a6")
            }
        return {
            "name": module_id,
            "icon": "❓",
            "color": "#95a5a6"
        }
    
    def get_all_modules(self) -> Dict[str, Dict[str, Any]]:
        """Retorna todos os módulos registrados"""
        return self.modules.copy()
    
    def navigate_to(self, module_id: str) -> bool:
        """
        Navega para um módulo específico
        
        Args:
            module_id: ID do módulo de destino
            
        Returns:
            bool: True se navegação foi bem sucedida
        """
        if module_id not in self.modules:
            return False
        
        # Adiciona ao histórico
        if self.current_module:
            self.history.append(self.current_module)
        
        self.current_module = module_id
        return True
    
    def go_back(self) -> Optional[str]:
        """Volta para o módulo anterior no histórico"""
        if self.history:
            self.current_module = self.history.pop()
            return self.current_module
        return None
    
    def get_current_module(self) -> Optional[str]:
        """Retorna o módulo atual"""
        return self.current_module
    
    def clear_history(self):
        """Limpa o histórico de navegação"""
        self.history.clear()
    
    def module_exists(self, module_id: str) -> bool:
        """Verifica se um módulo existe"""
        return module_id in self.modules
    
    def get_modules_list(self) -> list:
        """Retorna lista de módulos disponíveis"""
        return [
            {
                "id": module_id,
                "name": info.get("name", module_id),
                "icon": info.get("icon", "📦"),
                "color": info.get("color", "#95a5a6")
            }
            for module_id, info in self.modules.items()
        ]
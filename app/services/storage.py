"""
Serviço de armazenamento de dados
Gerencia a persistência dos dados JSON
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, List
from datetime import datetime


class StorageService:
    """Serviço para gerenciar o armazenamento de dados"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        
        # Arquivos de dados
        self.files = {
            "config": self.data_dir / "config.json",
            "calendar": self.data_dir / "calendario.json",
            "notes": self.data_dir / "notas.json",
            "daily": self.data_dir / "diario.json",
            "finance": self.data_dir / "financas.json"
        }
        
        # Inicializa arquivos se não existirem
        self.initialize_files()
    
    def initialize_files(self):
        """Inicializa os arquivos de dados com estruturas padrão"""
        default_data = {
            "config": {
                "active_module": "calendar",
                "theme": "light",
                "last_accessed": datetime.now().isoformat()
            },
            "calendar": {"events": []},
            "notes": {"notes": [], "categories": []},
            "daily": {"entries": []},
            "finance": {
                "transactions": [],
                "categories": ["Alimentação", "Transporte", "Lazer", "Saúde", "Educação"]
            }
        }
        
        for file_key, file_path in self.files.items():
            if not file_path.exists():
                self._save_json(file_path, default_data.get(file_key, {}))
    
    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Carrega dados de um arquivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_json(self, file_path: Path, data: Dict[str, Any]) -> bool:
        """Salva dados em um arquivo JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar {file_path}: {e}")
            return False
    
    # Métodos específicos para cada módulo
    
    def load_config(self) -> Dict[str, Any]:
        """Carrega configurações do aplicativo"""
        config = self._load_json(self.files["config"])
        if not config:
            config = {
                "active_module": "calendar",
                "theme": "light"
            }
        return config
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Salva configurações do aplicativo"""
        return self._save_json(self.files["config"], config)
    
    def load_calendar_events(self) -> List[Dict[str, Any]]:
        """Carrega eventos do calendário"""
        data = self._load_json(self.files["calendar"])
        return data.get("events", [])
    
    def save_calendar_events(self, events: List[Dict[str, Any]]) -> bool:
        """Salva eventos do calendário"""
        return self._save_json(self.files["calendar"], {"events": events})
    
    def load_notes(self) -> Dict[str, Any]:
        """Carrega notas"""
        return self._load_json(self.files["notes"])
    
    def save_notes(self, notes_data: Dict[str, Any]) -> bool:
        """Salva notas"""
        return self._save_json(self.files["notes"], notes_data)
    
    def load_daily_entries(self) -> List[Dict[str, Any]]:
        """Carrega entradas do diário"""
        data = self._load_json(self.files["daily"])
        return data.get("entries", [])
    
    def save_daily_entries(self, entries: List[Dict[str, Any]]) -> bool:
        """Salva entradas do diário"""
        return self._save_json(self.files["daily"], {"entries": entries})
    
    def load_finance_data(self) -> Dict[str, Any]:
        """Carrega dados financeiros"""
        return self._load_json(self.files["finance"])
    
    def save_finance_data(self, finance_data: Dict[str, Any]) -> bool:
        """Salva dados financeiros"""
        return self._save_json(self.files["finance"], finance_data)
    
    def backup(self) -> Path:
        """Cria um backup dos dados"""
        backup_dir = self.data_dir / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"backup_{timestamp}"
        backup_path.mkdir()
        
        for file_path in self.files.values():
            if file_path.exists():
                backup_file = backup_path / file_path.name
                with open(file_path, 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
        
        return backup_path
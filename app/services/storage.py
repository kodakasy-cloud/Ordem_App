"""
Serviço de armazenamento de dados - Gerencia persistência
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


class StorageService:
    """
    Gerencia persistência de dados em arquivos JSON
    Centraliza todas as operações de leitura/escrita
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Inicializa o serviço de armazenamento
        
        Args:
            data_dir: Diretório onde os dados serão salvos
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Arquivos de dados
        self.config_file = self.data_dir / "config.json"
        self.notas_file = self.data_dir / "notas.json"
        self.diario_file = self.data_dir / "diario.json"
        self.financas_file = self.data_dir / "financas.json"
        self.calendario_file = self.data_dir / "calendario.json"
        
        # Criar arquivos padrão se não existirem
        self._criar_arquivos_padrao()
    
    def _criar_arquivos_padrao(self):
        """Cria arquivos padrão com estrutura básica se não existirem"""
        arquivos_padrao = {
            self.config_file: {"tema": "dark", "primeira_vez": True, "versao": "1.0.0"},
            self.notas_file: {"notas": {}, "ultima_atualizacao": datetime.now().isoformat()},
            self.diario_file: {"entradas": {}, "ultima_atualizacao": datetime.now().isoformat()},
            self.financas_file: {"transacoes": [], "categorias": [], "ultima_atualizacao": datetime.now().isoformat()},
            self.calendario_file: {"eventos": [], "ultima_atualizacao": datetime.now().isoformat()}
        }
        
        for arquivo, dados_padrao in arquivos_padrao.items():
            if not arquivo.exists():
                try:
                    with open(arquivo, 'w', encoding='utf-8') as f:
                        json.dump(dados_padrao, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"Erro ao criar arquivo padrão {arquivo}: {e}")
    
    # Métodos genéricos
    def carregar_arquivo(self, file_path: Path) -> Dict:
        """
        Carrega dados de um arquivo JSON
        
        Args:
            file_path: Caminho do arquivo
        
        Returns:
            Dicionário com os dados carregados
        """
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Erro de decodificação JSON no arquivo {file_path}")
                return {}
            except Exception as e:
                print(f"Erro ao carregar {file_path}: {e}")
                return {}
        return {}
    
    def salvar_arquivo(self, file_path: Path, dados: Dict) -> bool:
        """
        Salva dados em um arquivo JSON
        
        Args:
            file_path: Caminho do arquivo
            dados: Dados a serem salvos
        
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            # Adicionar timestamp de atualização
            if isinstance(dados, dict):
                dados["ultima_atualizacao"] = datetime.now().isoformat()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2, sort_keys=True)
            return True
        except Exception as e:
            print(f"Erro ao salvar {file_path}: {e}")
            return False
    
    # Métodos específicos para configurações
    def carregar_config(self) -> Dict:
        """
        Carrega configurações salvas
        
        Returns:
            Dicionário com as configurações
        """
        return self.carregar_arquivo(self.config_file)
    
    def salvar_config(self, config: Dict) -> bool:
        """
        Salva configurações
        
        Args:
            config: Configurações a serem salvas
        
        Returns:
            True se salvou com sucesso
        """
        return self.salvar_arquivo(self.config_file, config)
    
    # Métodos específicos para notas
    def carregar_notas(self) -> Dict:
        """Carrega notas salvas"""
        dados = self.carregar_arquivo(self.notas_file)
        return dados.get("notas", {})
    
    def salvar_notas(self, notas: Dict) -> bool:
        """Salva notas"""
        dados = {"notas": notas}
        return self.salvar_arquivo(self.notas_file, dados)
    
    def adicionar_nota(self, nota: Dict) -> bool:
        """Adiciona uma nova nota"""
        notas = self.carregar_notas()
        nota_id = nota.get("id", str(len(notas) + 1))
        notas[nota_id] = nota
        return self.salvar_notas(notas)
    
    # Métodos específicos para diário
    def carregar_diario(self) -> Dict:
        """Carrega entradas do diário"""
        dados = self.carregar_arquivo(self.diario_file)
        return dados.get("entradas", {})
    
    def salvar_diario(self, entradas: Dict) -> bool:
        """Salva entradas do diário"""
        dados = {"entradas": entradas}
        return self.salvar_arquivo(self.diario_file, dados)
    
    def adicionar_entrada_diario(self, data: str, entrada: Dict) -> bool:
        """Adiciona uma entrada no diário"""
        entradas = self.carregar_diario()
        entradas[data] = entrada
        return self.salvar_diario(entradas)
    
    # Métodos específicos para finanças
    def carregar_financas(self) -> Dict:
        """Carrega dados financeiros"""
        return self.carregar_arquivo(self.financas_file)
    
    def salvar_financas(self, dados: Dict) -> bool:
        """Salva dados financeiros"""
        return self.salvar_arquivo(self.financas_file, dados)
    
    def adicionar_transacao(self, transacao: Dict) -> bool:
        """Adiciona uma transação financeira"""
        dados = self.carregar_financas()
        if "transacoes" not in dados:
            dados["transacoes"] = []
        dados["transacoes"].append(transacao)
        return self.salvar_financas(dados)
    
    # Métodos específicos para calendário
    def carregar_calendario(self) -> Dict:
        """Carrega eventos do calendário"""
        return self.carregar_arquivo(self.calendario_file)
    
    def salvar_calendario(self, dados: Dict) -> bool:
        """Salva eventos do calendário"""
        return self.salvar_arquivo(self.calendario_file, dados)
    
    def adicionar_evento(self, evento: Dict) -> bool:
        """Adiciona um evento no calendário"""
        dados = self.carregar_calendario()
        if "eventos" not in dados:
            dados["eventos"] = []
        dados["eventos"].append(evento)
        return self.salvar_calendario(dados)
    
    # Métodos utilitários
    def backup(self, nome_backup: str = None) -> bool:
        """
        Cria um backup dos dados
        
        Args:
            nome_backup: Nome do backup (opcional)
        
        Returns:
            True se o backup foi criado com sucesso
        """
        try:
            backup_dir = self.data_dir / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            if not nome_backup:
                nome_backup = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            backup_path = backup_dir / nome_backup
            backup_path.mkdir(exist_ok=True)
            
            # Copiar todos os arquivos JSON
            import shutil
            for arquivo in self.data_dir.glob("*.json"):
                shutil.copy2(arquivo, backup_path / arquivo.name)
            
            print(f"✅ Backup criado em: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return False
    
    def limpar_dados(self, confirmar: bool = False) -> bool:
        """
        Limpa todos os dados (cuidado!)
        
        Args:
            confirmar: Deve ser True para confirmar a limpeza
        
        Returns:
            True se limpou com sucesso
        """
        if not confirmar:
            print("⚠️ Limpeza não confirmada. Use confirmar=True para prosseguir.")
            return False
        
        try:
            for arquivo in self.data_dir.glob("*.json"):
                if arquivo != self.config_file:  # Manter configurações
                    arquivo.unlink()
            self._criar_arquivos_padrao()
            print("✅ Dados limpos com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao limpar dados: {e}")
            return False
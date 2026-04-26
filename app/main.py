"""
Arquivo principal do aplicativo
Inicializa e gerencia o ciclo de vida do app
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório base ao path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.core.app import Application
from app.core.router import Router
from app.ui.screens.loading_screen import LoadingScreen
from app.services.storage import StorageService


def main():
    """Função principal do aplicativo"""
    try:
        # Inicializa serviços
        storage_service = StorageService(BASE_DIR / "data")
        
        # Cria o router
        router = Router()
        
        # Cria e executa a aplicação
        app = Application(storage_service, router)
        app.run()
        
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
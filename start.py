from pathlib import Path
import sys

# Garantir que o diretório raiz esteja no sys.path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from app import main


if __name__ == "__main__":
    main.iniciar_aplicacao()

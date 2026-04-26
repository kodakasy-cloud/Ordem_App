import sys
import os

# Adiciona o diretório atual ao path para permitir imports relativos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import main

if __name__ == "__main__":
    main()
import os
import shutil
from pathlib import Path

def limpar_pycache(diretorio="."):
    """Remove todas as pastas __pycache__ e arquivos .pyc"""
    base = Path(diretorio)
    removidos = 0
    
    for item in base.rglob("*"):
        if item.is_dir() and item.name == "__pycache__":
            shutil.rmtree(item)
            removidos += 1
            print(f"Removido: {item}")
        elif item.is_file() and item.suffix == ".pyc":
            item.unlink()
            removidos += 1
            print(f"Removido: {item}")
    
    print(f"\nTotal removido: {removidos} itens")

if __name__ == "__main__":
    limpar_pycache()
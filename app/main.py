import sys
import os
from pathlib import Path

# Nota: configuração de encoding é feita de forma segura em `app.__init__`
# para evitar problemas com buffers fechados no ambiente do VS Code.

# Configurar caminhos
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Importar CustomTkinter
try:
    import customtkinter as ctk
except ImportError:
    print("CustomTkinter nao encontrado. Instale com: pip install customtkinter")
    sys.exit(1)

from app.core.app import App


def verificar_dependencias():
    """Verifica se todas as dependencias estao instaladas"""
    dependencias = {
        'customtkinter': 'customtkinter',
    }
    
    faltando = []
    for nome, pacote in dependencias.items():
        try:
            __import__(pacote)
        except ImportError:
            faltando.append(nome)
    
    if faltando:
        print(f"Dependencias faltando: {', '.join(faltando)}")
        print("Instale com: pip install " + " ".join(faltando))
        return False
    
    return True


def configurar_ambiente():
    """Configura o ambiente da aplicacao"""
    # Criar diretorio de dados
    data_dir = ROOT_DIR / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Configurar CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    return True


def iniciar_aplicacao():
    """Funcao principal que inicia a aplicacao"""
    print("Verificando dependencias...")
    if not verificar_dependencias():
        return
    
    print("Configurando ambiente...")
    if not configurar_ambiente():
        return
    
    print("Inicializando aplicacao...")
    try:
        # Criar e executar app
        root = ctk.CTk()
        app = App(root)
        app.run()
    except Exception as e:
        print(f"Erro durante execucao: {e}")
        import traceback
        traceback.print_exc()


# Se executado diretamente (para testes)
if __name__ == "__main__":
    iniciar_aplicacao()
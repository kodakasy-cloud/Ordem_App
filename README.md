# Ordem_App

Instruções rápidas para configurar e executar o projeto localmente (venv + run).

## Pré-requisitos

- Python 3.10+ instalado
- Conexão com internet para instalar dependências

## Passos (Windows)

1. Abra um terminal na raiz do repositório (`C:\Projetos\Ordem_App`).

2. Crie um ambiente virtual e ative (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se estiver no CMD use:

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

3. Atualize o pip e instale dependências:

```powershell
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
```

4. Inicie o aplicativo (duas opções):

- Usando o script `start.py` (recomendado):

```powershell
.venv\Scripts\python start.py
```

- Ou direto pelo módulo principal:

```powershell
.venv\Scripts\python -m app.main
```

## Observações

- O projeto usa `customtkinter` para a interface. Se ocorrer erro de GUI, verifique se a instalação foi concluída sem erros.
- Se o PowerShell bloquear a execução do script de ativação, execute temporariamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Resolução de problemas

- Dependência faltando: execute manualmente `pip install customtkinter`.
- Erros de caminho: certifique-se de executar a partir da pasta raiz do repositório.

## Arquivos úteis

- Iniciador: `start.py`
- Ponto de entrada: `app/main.py`
- Dependências: `requirements.txt`

---

Arquivo gerado automaticamente pelo assistente para instruções de setup.

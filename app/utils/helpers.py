"""
Funções utilitárias auxiliares para toda a aplicação
"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
import re
import uuid
import unicodedata


# ============== FORMATADORES ==============



def formatar_data(data: datetime, formato: str = "%d/%m/%Y") -> str:
    """
    Formata uma data para string
    
    Args:
        data: Objeto datetime
        formato: Formato desejado (padrão: DD/MM/AAAA)
    
    Returns:
        String formatada
    """
    if not data:
        return ""
    return data.strftime(formato)


def formatar_hora(data: datetime, formato: str = "%H:%M") -> str:
    """
    Formata uma hora para string
    
    Args:
        data: Objeto datetime
        formato: Formato desejado (padrão: HH:MM)
    
    Returns:
        String formatada
    """
    if not data:
        return ""
    return data.strftime(formato)


def formatar_moeda(valor: float, simbolo: str = "R$") -> str:
    """
    Formata um valor para moeda brasileira
    
    Args:
        valor: Valor numérico
        simbolo: Símbolo da moeda (padrão: R$)
    
    Returns:
        String formatada ex: "R$ 1.234,56"
    """
    if valor is None:
        valor = 0
    return f"{simbolo} {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_numero(valor: float, casas_decimais: int = 2) -> str:
    """
    Formata um número com separadores de milhar
    
    Args:
        valor: Valor numérico
        casas_decimais: Número de casas decimais
    
    Returns:
        String formatada ex: "1.234,56"
    """
    if valor is None:
        valor = 0
    formato = f"{{:,.{casas_decimais}f}}"
    return formato.format(valor).replace(",", "X").replace(".", ",").replace("X", ".")


# ============== VALIDADORES ==============

def validar_email(email: str) -> bool:
    """
    Valida formato de email
    
    Args:
        email: String do email
    
    Returns:
        True se válido, False caso contrário
    """
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def validar_telefone(telefone: str) -> bool:
    """
    Valida formato de telefone brasileiro
    
    Args:
        telefone: String do telefone
    
    Returns:
        True se válido, False caso contrário
    """
    if not telefone:
        return False
    # Remove caracteres não numéricos
    numeros = re.sub(r'\D', '', telefone)
    # Aceita celular (11 dígitos) ou fixo (10 dígitos)
    return len(numeros) in [10, 11]


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF
    
    Args:
        cpf: String do CPF
    
    Returns:
        True se válido, False caso contrário
    """
    cpf = re.sub(r'\D', '', cpf)
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    if digito1 >= 10:
        digito1 = 0
    
    # Calcula segundo dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    if digito2 >= 10:
        digito2 = 0
    
    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])


# ============== GERADORES ==============

def gerar_id(tamanho: int = 8) -> str:
    """
    Gera um ID único
    
    Args:
        tamanho: Tamanho do ID (padrão: 8)
    
    Returns:
        String com ID único
    """
    return str(uuid.uuid4())[:tamanho]


def gerar_uuid() -> str:
    """
    Gera um UUID completo
    
    Returns:
        String com UUID
    """
    return str(uuid.uuid4())


# ============== MANIPULAÇÃO DE TEXTO ==============

def truncar_texto(texto: str, tamanho: int = 50, sufixo: str = "...") -> str:
    """
    Trunca um texto para o tamanho especificado
    
    Args:
        texto: Texto original
        tamanho: Tamanho máximo
        sufixo: Sufixo para indicar truncamento
    
    Returns:
        Texto truncado
    """
    if not texto:
        return ""
    if len(texto) <= tamanho:
        return texto
    return texto[:tamanho] + sufixo


def capitalizar(texto: str) -> str:
    """
    Capitaliza um texto (primeira letra maiúscula, resto minúsculo)
    
    Args:
        texto: Texto original
    
    Returns:
        Texto capitalizado
    """
    if not texto:
        return ""
    return texto[0].upper() + texto[1:].lower()


def remover_acentos(texto: str) -> str:
    """
    Remove acentos de um texto
    
    Args:
        texto: Texto original
    
    Returns:
        Texto sem acentos
    """
    if not texto:
        return ""
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto


def slugify(texto: str) -> str:
    """
    Converte um texto para slug (URL amigável)
    
    Args:
        texto: Texto original
    
    Returns:
        Slug gerado
    """
    if not texto:
        return ""
    texto = remover_acentos(texto.lower())
    texto = re.sub(r'[^a-z0-9]+', '-', texto)
    texto = texto.strip('-')
    return texto


# ============== DATAS ==============

def obter_mes_atual() -> int:
    """Retorna o número do mês atual (1-12)"""
    return datetime.now().month


def obter_ano_atual() -> int:
    """Retorna o ano atual"""
    return datetime.now().year


def dias_entre_datas(data1: datetime, data2: datetime) -> int:
    """
    Calcula dias entre duas datas
    
    Args:
        data1: Primeira data
        data2: Segunda data
    
    Returns:
        Número de dias entre as datas
    """
    if not data1 or not data2:
        return 0
    return abs((data2 - data1).days)


def eh_hoje(data: datetime) -> bool:
    """
    Verifica se a data é hoje
    
    Args:
        data: Data a verificar
    
    Returns:
        True se for hoje
    """
    if not data:
        return False
    return data.date() == datetime.now().date()


def eh_mesmo_dia(data1: datetime, data2: datetime) -> bool:
    """
    Verifica se duas datas são do mesmo dia
    
    Args:
        data1: Primeira data
        data2: Segunda data
    
    Returns:
        True se forem do mesmo dia
    """
    if not data1 or not data2:
        return False
    return data1.date() == data2.date()


def obter_dias_do_mes(ano: int, mes: int) -> int:
    """
    Retorna o número de dias em um mês
    
    Args:
        ano: Ano
        mes: Mês (1-12)
    
    Returns:
        Número de dias
    """
    from calendar import monthrange
    return monthrange(ano, mes)[1]


def obter_nome_mes(mes: int, curto: bool = False) -> str:
    """
    Retorna o nome do mês
    
    Args:
        mes: Número do mês (1-12)
        curto: Se True, retorna nome curto (3 letras)
    
    Returns:
        Nome do mês
    """
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    meses_curtos = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    
    if 1 <= mes <= 12:
        return meses_curtos[mes - 1] if curto else meses[mes - 1]
    return ""


def obter_nome_dia_semana(dia: int, curto: bool = False) -> str:
    """
    Retorna o nome do dia da semana
    
    Args:
        dia: Número do dia (0-6, onde 0 é segunda)
        curto: Se True, retorna nome curto
    
    Returns:
        Nome do dia da semana
    """
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    dias_curtos = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    
    if 0 <= dia <= 6:
        return dias_curtos[dia] if curto else dias[dia]
    return ""


# ============== LISTAS E DICIONÁRIOS ==============

def agrupar_por(lista: List[Dict], chave: str) -> Dict:
    """
    Agrupa uma lista de dicionários por uma chave
    
    Args:
        lista: Lista de dicionários
        chave: Chave para agrupamento
    
    Returns:
        Dicionário agrupado
    """
    resultado = {}
    for item in lista:
        valor_chave = item.get(chave)
        if valor_chave not in resultado:
            resultado[valor_chave] = []
        resultado[valor_chave].append(item)
    return resultado


def ordenar_por(lista: List[Dict], chave: str, reverso: bool = False) -> List[Dict]:
    """
    Ordena uma lista de dicionários por uma chave
    
    Args:
        lista: Lista de dicionários
        chave: Chave para ordenação
        reverso: Ordem reversa
    
    Returns:
        Lista ordenada
    """
    return sorted(lista, key=lambda x: x.get(chave, ""), reverse=reverso)


def filtrar_por(lista: List[Dict], filtros: Dict) -> List[Dict]:
    """
    Filtra uma lista de dicionários com base em filtros
    
    Args:
        lista: Lista de dicionários
        filtros: Dicionário com chave: valor para filtrar
    
    Returns:
        Lista filtrada
    """
    resultado = lista
    for chave, valor in filtros.items():
        resultado = [item for item in resultado if item.get(chave) == valor]
    return resultado


# ============== ARQUIVOS ==============

def ler_arquivo_texto(caminho: str) -> Optional[str]:
    """
    Lê um arquivo de texto
    
    Args:
        caminho: Caminho do arquivo
    
    Returns:
        Conteúdo do arquivo ou None se erro
    """
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo {caminho}: {e}")
        return None


def escrever_arquivo_texto(caminho: str, conteudo: str) -> bool:
    """
    Escreve em um arquivo de texto
    
    Args:
        caminho: Caminho do arquivo
        conteudo: Conteúdo a escrever
    
    Returns:
        True se sucesso
    """
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        return True
    except Exception as e:
        print(f"Erro ao escrever arquivo {caminho}: {e}")
        return False
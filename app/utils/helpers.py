"""
Funções auxiliares para o aplicativo
"""

import hashlib
from datetime import datetime
from typing import Optional


def generate_id(*args) -> str:
    """
    Gera um ID único baseado em timestamp e conteúdo
    
    Args:
        *args: Valores para gerar o hash
        
    Returns:
        str: ID único
    """
    content = f"{datetime.now().timestamp()}_{'_'.join(str(arg) for arg in args)}"
    return hashlib.md5(content.encode()).hexdigest()[:16]


def format_date(date: datetime, format_type: str = "short") -> str:
    """
    Formata uma data para exibição
    
    Args:
        date: Objeto datetime
        format_type: Tipo de formato ('short', 'long', 'full')
        
    Returns:
        str: Data formatada
    """
    formats = {
        "short": "%d/%m/%Y",
        "long": "%d de %B de %Y",
        "full": "%A, %d de %B de %Y",
        "time": "%H:%M",
        "datetime": "%d/%m/%Y %H:%M"
    }
    
    return date.strftime(formats.get(format_type, "%d/%m/%Y"))


def format_currency(value: float, currency: str = "BRL") -> str:
    """
    Formata valor monetário
    
    Args:
        value: Valor a ser formatado
        currency: Código da moeda
        
    Returns:
        str: Valor formatado
    """
    symbols = {
        "BRL": "R$",
        "USD": "$",
        "EUR": "€"
    }
    
    symbol = symbols.get(currency, "R$")
    return f"{symbol} {value:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Trunca um texto para um tamanho máximo
    
    Args:
        text: Texto a ser truncado
        max_length: Tamanho máximo
        suffix: Sufixo para texto truncado
        
    Returns:
        str: Texto truncado
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def parse_date(date_string: str) -> Optional[datetime]:
    """
    Tenta parsear uma string para datetime
    
    Args:
        date_string: String com data
        
    Returns:
        datetime ou None se falhar
    """
    formats = [
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    return None


def get_month_name(month: int, short: bool = False) -> str:
    """
    Retorna o nome do mês
    
    Args:
        month: Número do mês (1-12)
        short: Se deve retornar nome curto
        
    Returns:
        str: Nome do mês
    """
    months_full = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    months_short = [
        "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
        "Jul", "Ago", "Set", "Out", "Nov", "Dez"
    ]
    
    if 1 <= month <= 12:
        return months_short[month - 1] if short else months_full[month - 1]
    
    return ""


def get_weekday_name(weekday: int, short: bool = False) -> str:
    """
    Retorna o nome do dia da semana
    
    Args:
        weekday: Número do dia (0-6, onde 0 é segunda)
        short: Se deve retornar nome curto
        
    Returns:
        str: Nome do dia da semana
    """
    weekdays_full = [
        "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
        "Sexta-feira", "Sábado", "Domingo"
    ]
    
    weekdays_short = [
        "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"
    ]
    
    if 0 <= weekday <= 6:
        return weekdays_short[weekday] if short else weekdays_full[weekday]
    
    return ""
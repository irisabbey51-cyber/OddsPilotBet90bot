import re
from datetime import datetime
from typing import List, Dict

def format_odds(odds: float) -> str:
    """Format odds for display"""
    if odds > 0:
        return f"+{odds:.0f}"
    return f"{odds:.0f}"

def validate_bet_amount(amount: str) -> bool:
    """Validate bet amount"""
    try:
        value = float(amount)
        return value > 0
    except ValueError:
        return False

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency for display"""
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }
    symbol = symbols.get(currency, "$")
    return f"{symbol}{amount:.2f}"

def is_valid_sport(sport: str) -> bool:
    """Check if sport is supported"""
    from config import Config
    return sport.lower() in Config.SUPPORTED_SPORTS

def parse_game_query(query: str) -> Dict:
    """Parse game query from user input"""
    # Simple parsing - can be enhanced
    teams = query.split(' vs ')
    if len(teams) == 2:
        return {
            'home': teams[0].strip(),
            'away': teams[1].strip()
        }
    return None

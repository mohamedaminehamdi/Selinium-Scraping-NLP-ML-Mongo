import re
from typing import Optional

def extract_format_from_title(title: str) -> Optional[str]:
    """
    Extrait le format du titre du produit (ex: "500g", "1L", etc.)
    """
    match = re.search(r"\b\d+(?:[\.,]\d+)?\s?(g|kg|ml|cl|l|L)\b", title, re.IGNORECASE)
    return match.group(0).replace(',', '.').strip() if match else None

def extract_weight(format_str: Optional[str]) -> Optional[float]:
    """
    Convertit un format type "500g" ou "1.5L" en poids en grammes ou millilitres
    """
    if not format_str:
        return None

    number_match = re.search(r"\d+(?:\.\d+)?", format_str)
    unit_match = re.search(r"[a-zA-Z]+", format_str)
    
    if not number_match or not unit_match:
        return None

    number = float(number_match.group(0))
    unit = unit_match.group(0).lower()

    if unit == "kg":
        return number * 1000
    elif unit == "g":
        return number
    elif unit == "l":
        return number * 1000
    elif unit == "cl":
        return number * 10
    elif unit == "ml":
        return number
    return None

def calculate_price_per_unit(price: Optional[float], weight: Optional[float]) -> Optional[float]:
    """
    Calcule le prix au kilo ou au litre
    """
    if price is None or weight is None or weight == 0:
        return None
    return round(price / weight * 1000, 2)  # Prix pour 1000g ou 1000ml

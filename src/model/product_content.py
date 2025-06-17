import re
from typing import Optional


def convert_weight_format_to_gr_or_ml(unit: str | None) -> tuple[str, int] | None:
    if not isinstance(unit, str):
        return None
    weight_multiplier: int = 1
    base_weight_unit: str = ''
    # print("unit: " + str(unit))
    unit_lower = unit.lower()
    match unit_lower:
        case 'g':
            weight_multiplier = 1
            base_weight_unit = 'g'
        case 'kg':
            weight_multiplier = 1000
            base_weight_unit = 'g'
        case 'ml':
            weight_multiplier = 1
            base_weight_unit = 'ml'
        case 'cl':
            weight_multiplier = 10
            base_weight_unit = 'ml'
        case 'l':
            weight_multiplier = 1000
            base_weight_unit = 'ml'
        case _:
            return None
    return (base_weight_unit, weight_multiplier)


def convert_format_product(description: str | None) -> Optional[tuple[str, float]]:
    '''
    return a tuple containing base_weigth_unit and total_weight
    '''
    tuple_result: Optional[tuple[str, float]] = (None, None)
    if not isinstance(description, str) or len(description) == 0:
        return tuple_result
    description = description.replace(".", ",")
    match_unite = re.search(r'les\s+(\d+)\s+(\S+)\s+de\s+(\d+(?:,\d+)?)\s*(kg|g|cL|L|ml)', description, re.IGNORECASE)
    match_direct2 = re.search(r'(\d+)x(\d+(?:,\d+)?)\s*(kg|g|cL|L|ml)', description, re.IGNORECASE)
    match_direct3 = re.search(r'(\d+(?:,\d+)?)\s*(kg|g|cL|L|ml)', description, re.IGNORECASE)
    match_direct4 = re.search(r'(\d+(?:,\d+)?)\s*', description, re.IGNORECASE)
    match_direct5 = re.search(r'(\d+)\s?([a-zA-Z]+)$', description, re.IGNORECASE)
    # print("match_unite: " + str(match_unite))
    # print("match_direct2: " + str(match_direct2))
    # print("match_direct3: " + str(match_direct3))
    # print("match_direct4: " + str(match_direct4))
    # print("match_direct5: " + str(match_direct5))
    result: str = None
    if match_unite:
        quantity = float(match_unite.group(1))
        unite_produit = match_unite.group(2)
        quantity_unitaire = float(match_unite.group(3).replace(',', '.'))
        unite_poids = match_unite.group(4)
        # print("quantity: " + str(quantity) + ", unite_produit: " + str(unite_produit) +
        #        ", quantity_unitaire: " + str(quantity_unitaire) +
        #        ", unite_poids: " + str(unite_poids))

        (base_weigth_unit, weight_multiplier) = convert_weight_format_to_gr_or_ml(unite_poids)
        # print("base_weigth_unit:" + str(base_weigth_unit) + ", weight_multiplier: " + str(weight_multiplier))
        weight_multiplier = weight_multiplier if weight_multiplier is not None else 1
        base_weigth_unit = base_weigth_unit if base_weigth_unit is not None else 1
        quantity_unitaire = quantity_unitaire if quantity_unitaire > 0 else 1
        total_weight = float(quantity * quantity_unitaire * weight_multiplier)
        total_weight_str = f"{total_weight:.0f}{base_weigth_unit}"
        result = total_weight_str
        tuple_result = (base_weigth_unit, total_weight)
        # print("input:" + str(description) + ", quantity: " + str(quantity) + ", unite_produit: " + str(unite_produit)
        #       + ", quantity_unitaire: " + str(quantity_unitaire) + ", unite_poids: " + str(unite_poids) + ", result1: " + str(result))
    elif match_direct2:
        quantity = float(match_direct2.group(1))
        poids_unitaire = float(match_direct2.group(2).replace(',', '.'))
        unite_poids = match_direct2.group(3)
        # print("quantity: " + str(quantity) +
        # ", poids_unitaire: " + str(poids_unitaire) +
        # ", unite_poids: " + str(unite_poids))
        (base_weigth_unit, weight_multiplier) = convert_weight_format_to_gr_or_ml(unite_poids)
        total_weight = float(quantity * poids_unitaire * weight_multiplier)
        result = f"{total_weight:.0f}{base_weigth_unit}"
        tuple_result = (base_weigth_unit, total_weight)
        # print("input:" + description + ", quantity: " + str(quantity) + ", poids_unitaire: " + str(poids_unitaire)
        #       + ", unite_poids: " + str(unite_poids) + ", result2: " + str(result))
    elif match_direct3:
        poids_unitaire = float(match_direct3.group(1).replace(',', '.'))
        unite_poids = match_direct3.group(2)
        # print("poids_unitaire: " + str(poids_unitaire) +
        # ", unite_poids: " + str(unite_poids))
        (base_weigth_unit, weight_multiplier) = convert_weight_format_to_gr_or_ml(unite_poids)
        total_weight = float(poids_unitaire * weight_multiplier)
        result = f"{total_weight}{base_weigth_unit}"
        tuple_result = (base_weigth_unit, total_weight)
        # print("input:" + description + ", poids: " + str(poids_unitaire) + ", unite: " + str(unite_poids)
        #       + ", result3: " + str(result))
    elif match_direct4:
        quantity = match_direct4.group(1)
        # print("match_direct4 quantity: " + str(quantity))
        quantity = quantity.replace(",", ".")
        quantity = float(quantity)
        tuple_result = ("u", float(quantity))
    else:
        # print("step 5")
        result = None  # "Format non reconnu"
    # print("convert_format_product result: " + result)
    value = tuple_result[1]
    return (tuple_result[0], int(value) if value and value.is_integer() else value)


def convertir_format_produit(description):
    match_unite = re.search(r'les\s+(\d+)\s+(\S+)\s+de\s+(\d+(?:,\d+)?)\s*(\S+)', description, re.IGNORECASE)

    if match_unite:
        quantity = int(match_unite.group(1))
        unite_produit = match_unite.group(2)
        quantity_unitaire = float(match_unite.group(3).replace(',', '.'))
        unite_poids = match_unite.group(4)

        total_weight = quantity * quantity_unitaire
        total_weight_str = f"{total_weight:.0f}{unite_poids}"
        return total_weight_str
    else:
        match_direct = re.search(r'(\d+)x(\d+(?:,\d+)?)\s*(kg|g|cL|L)', description, re.IGNORECASE)
        if match_direct:
            quantity = int(match_direct.group(1))
            poids_unitaire = float(match_direct.group(2).replace(',', '.'))
            unite = match_direct.group(3)
            total_weight = quantity * poids_unitaire
            return f"{total_weight:.0f}{unite}"
        else:
            match_direct = re.search(r'(\d+(?:,\d+)?)\s*(kg|g|cL|L)', description, re.IGNORECASE)
            if match_direct:
                poids = match_direct.group(1)
                unite = match_direct.group(2)
                return f"{poids}{unite}"
            else:
                return "Format non reconnu"


iA_keywords_for_ingredients_groups = ["milk", "wheat", "cocoa", "soy"]
iA_keywords_to_remove = ["vitamin"]  # ["oil", "vitamin", "whole", "powder", "thickener", "natural", "flavoring", "flavors", "flavor", "extract", "minerals", "mineral", "concentrate"]
# Exemples
exemples = [
    "La barquette d'1,5Kg",
    "les 16 bâtonnets de 2 cubes - 128 g",
    "les 10 unités de 0.9 kg",
    "la boite de 12",
    "la plaquette de 250g",
    "les 3 briques de 20cL",
    "le pot de 497g",
    "la bouteille de 40cL",
    "la barquette de 500g",
    "la bouteille de 40cL",
    "la poche de 33cL",
    "la bombe de 250g",
    "le rouleau de 250g",
    "la brique de 1L",
    "le paquet de 8 - 280g",
    "le sachet de 450g",
    "les 6 brioches de 50g",
    "le paquet de 16 - 320g",
    "les 10 pains de 35g",
    "les 8 portions - 200g",
    "la pièce de 350g",
    "la pintade de 1,400kg",
    "la boite de 4 - 400 g",
    "la boite de 25 nuggets - 500g",
    "la portion de 1,5Kg",
    "le poulet de 1,600Kg",
    "le colis de 3Kg",
    "4x250g",
    "4x 250g",
    "4 x250g"
]

'''OUTPUT:
INPUT: la plaquette de 250g, OUTPUT: 250g
INPUT: les 3 briques de 20cL, OUTPUT: 60cL
INPUT: le pot de 497g, OUTPUT: 497g
INPUT: la bouteille de 40cL, OUTPUT: 40cL
INPUT: la barquette de 500g, OUTPUT: 500g
INPUT: la barquette de 2 - 230g, OUTPUT: 230g
INPUT: la bouteille de 40cL, OUTPUT: 40cL
INPUT: la poche de 33cL, OUTPUT: 33cL
INPUT: la bombe de 250g, OUTPUT: 250g
INPUT: le rouleau de 250g, OUTPUT: 250g
INPUT: la brique de 1L, OUTPUT: 1L
INPUT: le paquet de 8 - 280g, OUTPUT: 280g
INPUT: le sachet de 450g, OUTPUT: 450g
INPUT: les 6 brioches de 50g, OUTPUT: 300g
INPUT: le paquet de 16 - 320g, OUTPUT: 320g
INPUT: les 10 pains de 35g, OUTPUT: 350g
INPUT: les 8 portions - 200g, OUTPUT: 200g
INPUT: la pièce de 350g, OUTPUT: 350g
INPUT: la pintade de 1,400kg, OUTPUT: 1,400kg
INPUT: la boite de 4 - 400 g, OUTPUT: 400g
INPUT: la boite de 25 nuggets - 500g, OUTPUT: 500g
INPUT: la portion de 1,5Kg, OUTPUT: 1,5Kg
INPUT: le poulet de 1,600Kg, OUTPUT: 1,600Kg
INPUT: le colis de 3Kg, OUTPUT: 3Kg
INPUT: 4x250g, OUTPUT: 1000g
'''
if __name__ == "__main__":
    for exemple in exemples:
        (base_weigth_unit, total_weight) = convert_format_product(exemple)
        print(f"INPUT: {exemple}, OUTPUT: {total_weight} {base_weigth_unit}")

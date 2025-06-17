import re

def convert_unit(description):
    # Define regular expressions
    unit_regex = ["kg","g","cL","L","ml"]
    number_regex = r"(\d+([\.,]\d+)?)"

    # Define lists
    first_list=["barquette","bouteille","poche","pot","bombe","rouleau","brique","sachet","paquet","pintade","boite","colis","poulet","plaquette","portion","pièce"]
    second_list =["la pièce","la portion","la poule"]
    auchan_list=["oeufs","portions","bâtonnets","pièce","pièces","pots","œufs","barquettes"]
    fourth_list=["bidon de",""]
    
    def multiplication(description):
        """
        Calcule le produit d'un nombre et d'un poids et retourne la valeur finale avec l'unité.
        """
        print(description)
    
        if (",")in description:
            description= description.replace(",",".")
            
        print(description)
        regex = r"(?P<valeur>\d+)(?:,?\d+)?x?(?P<poids>\d+(?:\.\d+)?)(?P<unite>[a-zA-Z]+)?"

        match = re.search(regex, description)
        if match:
            valeur = float(match.group("valeur"))
            print(valeur)
            poids = float(match.group("poids"))
            print(poids)
            unité = match.group("unite")
            print(unité)

            resultat = valeur * poids
            final_result = f"{int(resultat)} {unité}"    # Append unit to the result
            return final_result
        else:
            return description  # Handle cases where the pattern doesn't match


            
    def extract_and_multiplication(description):
        match = re.search(r"(\d+)\s+(\w+)\s+de\s+(\d+\w+)", description)

        if match:
            nombre = int(match.group(1))
            poids_str = match.group(3)
            for u in unit_regex:
                if u in poids_str:
                    poids_match = re.match(r"(\d+)", poids_str)
                    
                    if poids_match:
                        poids = int(poids_match.group(1))
                        resultat = nombre * poids
                        final_result = f"{resultat} {u}"
                        print("Résultat final:", final_result)
                    else:
                        print("Impossible d'extraire le poids.")
        else:
            print("Aucune correspondance trouvée.")
        return final_result

    
   
    def extract_bidon_contenance(texte):
        """
        Extrait la valeur numérique de la contenance d'un bidon et l'unité.

        Args:
            texte (str): Le texte contenant la description du bidon.

        Returns:
            str: La valeur numérique de la contenance suivie de l'unité, ou None si elle n'est pas trouvée.
        """
        # Expression régulière pour extraire la valeur numérique et l'unité
        regex = r"(?P<valeur>\d+)(?:\s*(?P<unite>[Ll])?)?"

        # Exécution de la recherche
        match = re.search(regex, texte)

        # Extraction de la valeur numérique et de l'unité
        if match:
            valeur = match.group("valeur")
            
            unite = match.group("unite")
            
            if unite:
                return f"{valeur}{unite}"
            else:
                return valeur
        else:
            return None

    # for test_list1 in first_list:
    #     if test_list1 in description:
    #         convert_desc_to_mesure(description)
    #         print(convert_desc_to_mesure(description))
    #         break

    # for test_list3 in third_list:
    #     if test_list3 in description:
    #         extract_and_multiplication(description)
    #         break
        
    # for test_list2 in second_list:
    #     if test_list2 in description:
    #         unit= "u"
    #         final_result = f"{test_list2}{unit}"
    #         print("final result",final_result)
    #         return final_result
    #         break
    
    
    if "bidon" in description:
        return extract_bidon_contenance(description)
    for auchan_desc in auchan_list:
        if auchan_desc in description:
            description= description.replace(auchan_desc, "u")
            print(description)
            return description
        else:
            description= description 

   
    if "x" in description:
        print("x")
        if (',') in description:
            print("virguel")
            description = description.replace(",", ".")
            return multiplication(description)
        else:
            return multiplication(description)
    else:
        print(description)
        return description
    #pots
        

desc = "2,5kg"

con = convert_unit(desc)
print("con",con)


def extract_unit(s: str) -> str:
    """
    Extracts the unit from a string containing a value followed by a unit.
    
    Example:
    extract_unit("19,96 € / kg") -> "kg"
    """
    
    if s is None:
        return ""  # Si la chaîne est None, retourner une chaîne vide
    
    # Split the string by "/"
    parts = s.split("/")
    
    # If there are at least two parts after splitting, return the second part (trimming any leading or trailing whitespace)
    if len(parts) >= 2:
        return parts[1].strip()
    else:
        return ""
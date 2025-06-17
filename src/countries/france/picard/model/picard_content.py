import json
import re
import sys
from typing import Final, List, Optional, Tuple, override
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from src.countries.france.picard.robots.picard_brands_scanner import ScannerPicardBrands
from src.model.my_model import ProductType
from src.model.product import Nutrition
from src.utils.my_utils import (
    all_attrs_are_none,
    are_string_exist_in_list,
    are_strings_equal,
    convert_to_float,
    convert_to_target_unit,
    get_all_files_inside_given_folder,
  
    remove_substring_and_clean,
   
)

class ProductContentPicard:
    
    BIO_PRESENCE: Final[List[str]] = ["bio"]
    VEGAN_PRESENCE: Final[List[str]] = ["vegan"]
    FRENCH_PRESENCE: Final[List[str]] = ["origine France", "provient de France", "provenant de l'agriculture biologique en France", "d'origine France",
                                         "Fabriqué en France", "élaboré en France", "Elaboré en France", "Origine : France",
                                         "cultivés en France", "cultivé en France", "cultivée en France",
                                         "fabriquées en France", "Fabriqués en France", "Fabriqué en France", "100% FRANCE", "de la France", "de France",
                                         "hauts france", "MADE IN FRANCE", "Farine de froment : France", "Fabriqué France",
                                         "Farine de blé France", "agriculture biologique en France", "NATURE DE FRANCE", "cultivés et surgelés en France",
                                         "fabriquée en Provence"]
    FRENCH_ABSENCE: Final[List[str]] = ["conditionnés en France",
                                        "conditionné en France", "conditionnées en France", "torréfié lentement en France"]

    LACTOSE_PRESENCE: Final[List[str]] = [", lactose", "lactosérum en poudre", "lactoserum en poudre", "lactose (de LAIT)", "LACTOSÉRUM (LAIT)", "contient du lactose",
                                          "protéines de lactoseruM", "extrait de lactosérum", "lactose (LAIT)", "LAIT en poudre entier", "LACTOSE et protéines de LAI"]
    LACTOSE_ABSENCE: Final[List[str]] = ["sans lactose", "aucun lactose",
                                         "si vous êtes intolérant(e) au lactose.", "convient aux intolérants au lactose"]
    FAT_ABSENCE: Final[List[str]] = [" 0% MG", " 0% de matière grasse",
                                     " 0% de MG", " 0% de mat gr", " 0% mat g", "Pauvre en matières grasses"]
    GMO_ABSENCE: Final[List[str]] = ["sans ogm", "Ne contient pas d'OGM", "OGM : Absence", "OGM 0,", "aucun ingrédient génétiquement modifié",
                                     "aucun de nos ingrédients n'a été maltraité par des OGM", "aucun ingrédient génétiquement modifié",
                                     "aucun ingrédient, additif ou arôme OGM"]
    ADDITIVE_ABSENCE: Final[List[str]] = ["sans additif", "ni additif", "ni d'additif", " 0% additif", "aucun additif", "aucun ajout d'additif",
                                          "aucun ingrédient, additif", "aucun conservateur, colorant ou autre additif"]
    DYE_ABSENCE: Final[List[str]] = ["sans colorant", "ni colorant", "sans arômes et colorant", "NI DE COLORANT", "aucun colorant", "aucun arôme artificiel, colorant",
                                     "ni de conservateurs et colorant", "sans arôme, colorant et conservateur", "Sans additifs, couleur", "aucun conservateur, colorant"]
    PRESERVATIVE_ABSENCE: Final[List[str]] = ["aucun ajout de conservateur", "sans conservateur", "ni conservateur", "pas de conservateur", "sans ajout de conservateur", "aucun conservateur", "aucun arôme artificiel, colorant, conservateur",
                                              "ni de conservateur", "sans arôme, colorant et conservateur", "aucun ajout d'additifs ou de conservateur", "aucun ajout de liants ou de conservateur"]
    GLUTEN_ABSENCE: Final[List[str]] = ["sans gluten", "ni gluten", "absence de gluten",
                                        "pas de gluten", "Dépourvu de gluten"]
    GLUTEN_PRESENCE: Final[List[str]] = ["gluten", "Traces de GLUTEN possibles", "contient de GLUTEN", "Peut contenir des traces de GLUTEN",
                                         "Traces éventuelles de GLUTEN", "Traces éventuelles de FRUITS A COQUE et de GLUTEN", "chapelure (dont GLUTEN)",
                                         "Allergènes :\nGluten", "Traces possibles d'arachide, de fruits à coque, de gluten", "Traces possibles d'arachides, de fruits à coques, de gluten",
                                         "Traces possibles de céleri, de gluten", "peut présenter des traces de GLUTEN", "Traces de LAIT et de GLUTEN",
                                         "Peut contenir : Autres FRUITS A COQUE,GLUTEN", "Allergènes : Gluten", "Traces de LAIT, d'ŒUF, de SOJA, de CELERI et de GLUTEN",
                                         "Présence possible de GLUTEN", "GLUTEN de BLE", "gluten de blé", "Peut contenir : FRUITS A COQUE, LAIT,GLUTEN",
                                         "Présence de GLUTEN", "Trace éventuelle de GLUTEN", "Traces éventuelles de produits à base de GLUTEN"]
    SUGAR_ABSENCE: Final[List[str]] = ["sans sucre", " 0% de sucre", "ne contient pas de sucres ajoutés", "sans adjonctions de sucre",
                                       "aucun sucre"]
    # sugar if < 0.9% ==> sugar free
    # pregnant if  description = non pasteurisé ou = cru ou = alcool ou Non Pasteurisé ou Non Pasteurisée ou Non Pasteurisés ou Non Pasteurisées ou inférieure à la pasteurisation
    INGREDIENTS_SUBSTRINGS: Final[List[str]] = ["Ingrédients biologiques", "de france", "de Meurthe-et-Moselle", "d'Equateur", "d'Occitanie", "de Provence", "de nouvelle-aquitaine", "de Suède", "d'Espagne", "préparation à base de", "présence enfonction de l'acidité des fruits", "issus de l'agriculture biologique", "produits issus de l'agriculture biologique naturellement sans gluten", "matières grasses végétales", "caramel", "voir les photos", "vierge extra", "lichette de jus de", "un petit extrait de", "un soupçon d'", "pincée extrait de", "une lichette d'extrait de", "un doigt de", "un peu de jus de", "un peu de bon", "graines de", "un filet de", "en purée", "mixée", "mixé", "de l'eau de", "écrasées", "un trait d'infusion de", "un trait d'", "une lichette de", "une lichette d'",
                                                "(jus de saison été)", "pressées", "jus de fruits à base de concentrés", "jus et purées de fruits à base de concentrés", "jus et purées de fruits à base de concentrés", "contient des sucres naturellement présents dans les fruits, comme tous les jus", "françaises", "une touché de", "une pincée de", "purée d'", "un morceau de", "une pointe d'extrait de", "antioxydant :", "antioxydant", "un zeste de", " et rien d'autre", "sans sucres ajoutés", "issu de l'agriculture biologique", "ingrédients issus de l'agriculture biologique", "un soupçon de", "une lichette de", "pressés", "pressée", "pressé", "presses", "ajoutées", "quelques", "un peu d'extrait de", "extrait de", "un peu d'", "un trait de", "mixées", "extrait de", "Jus de ", "Jus d'", "pulpe d'", "purée de ", "concentré de", "*", "colorant :", "colorant:", "acidifiant :", "acidifiant:", "stabilisant:", "stabilisant :", "concentré", "concentrée", "jus de saison été"]

    @classmethod
    def get_brand_from_title(cls, title: str) -> str:
        
        product_brand = "Picard"
        product_title_upper = title.upper()
        for brand in ScannerPicardBrands:
            if brand.upper() in product_title_upper:
                product_brand = brand
                print(f"product_brand: {product_brand}, product: {title}")
                break
        return product_brand.upper()
    
    @classmethod
    def extract_product_origin(cls, driver, product_id: str, logger) -> dict:
        # Extraction de l'origine
        origin = {}
        logger.debug(f"Début de l'extraction de l'origine pour {product_id}")
        try:
            country_mapping = {
                "france": "FR",
                "italie": "IT",
                "espagne": "ES",
                "allemagne": "DE",
                "belgique": "BE",
                "portugal": "PT",
                "pays-bas": "NL",
                "royaume-uni": "GB",
                "suisse": "CH",
                "ue": "EU",
                "union européenne": "EU",
                "chine": "CN",
                "japon": "JP",
                "canada": "CA",
                "états-unis": "US"
            }
                
            try:
                origin_tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "tab5id"))
                )
                # Vérifier si l'onglet n'est pas déjà actif
                if origin_tab.get_attribute("aria-expanded") != "true":
                    driver.execute_script("arguments[0].click();", origin_tab)
                    logger.debug(f"Onglet 'Origine' (tab5id) activé pour {product_id}")
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.ID, "tab5"))
                    )
                # Extraire le contenu de l'onglet
                origin_content = driver.find_elements(By.CSS_SELECTOR, "#tab5 .pi-ProductTabsCms-text")
                origin_text = ""
                for content in origin_content:
                    text = content.text.strip().lower()
                    if text:
                        origin_text = text
                        logger.debug(f"Texte d'origine trouvé dans #tab5 .pi-ProductTabsCms-text pour {product_id}: {origin_text}")
                        break 
                        
                if not origin_text:
                    logger.debug(f"Aucun texte trouvé dans #tab5 .pi-ProductTabsCms-text pour {product_id}")
                    
                # Motifs regex pour détecter l'origine
                origin_patterns = [
                    r'origine\s*[:=]\s*([\w\s-]+)',
                    r'origin\s*[:=]\s*([\w\s-]+)',
                    r'\(origine\s*[:=]\s*([\w\s-]+)\)',
                    r'produit\s*(en|à)\s*([\w\s-]+)',
                    r'fabriqué\s*(en|à)\s*([\w\s-]+)',
                    r'origine\s*([\w\s-]+)',
                    r'issu\s*.*\s*(en|de|à)\s*([\w\s-]+)',
                    r'élaboré\s*(en|à)\s*([\w\s-]+)',
                    
                ] 
                # Chercher l'origine dans le texte de l'onglet
                if origin_text:
                    for pattern in origin_patterns:
                        match = re.search(pattern, origin_text, re.IGNORECASE)
                        if match:
                            country = match.group(1) if match.group(1) not in ('en', 'à', 'de') else match.group(2)
                            country = country.strip().lower()
                            
                            # Gérer les cas où le pays contient des espaces
                            for mapped_country, code in country_mapping.items():
                                if mapped_country in country or country in mapped_country:
                                    origin["explicit"] = code
                                    logger.info(f"Origine trouvée pour {product_id}: {origin['explicit']} (pays: {country})")
                                    break
                            if origin:
                                break
                    # Recherche approximative si aucun motif regex ne correspond
                    if not origin:
                        for country, code in country_mapping.items():
                            if country in origin_text:
                                origin["explicit"] = code
                                logger.info(f"Origine trouvée par correspondance approximative pour {product_id}: {code} (pays: {country})")
                                break
                            
                    # Log si aucune origine n'est trouvée
                    if not origin:
                        logger.warning(f"Aucune origine identifiée dans le texte de l'onglet 'Origine' pour {product_id}: {origin_text}")
                    
            except (NoSuchElementException, TimeoutException) as e:
                logger.error(f"Onglet 'Origine' (tab5id) non trouvé ou non cliquable pour {product_id}: {str(e)}")
                
        
        except Exception as e:
            logger.error(f"Erreur inattendue lors de l'extraction de l'origine pour {product_id}: {str(e)}")
            
        logger.info(f"Retour de extract_product_origin pour {product_id}: {origin}") 
        logger.debug(f"Valeur finale de origin avant retour pour {product_id}: {origin}")
        return origin     
                        
    

    @classmethod
    def get_packaging_info(cls, product_pricing_unit: Optional[str]) -> tuple[str | None, str | None, float] | None:
        if not isinstance(product_pricing_unit, str):
            print(f"print2: {product_pricing_unit}")
            return (None, None, None)
        else:
            product_pricing_unit = product_pricing_unit.lower()

        # warning: another ProductType called "U"
        matter = ProductType.OTHER.name
        unit_of_mesure = "Kg"
        product_pricing_unit = product_pricing_unit if product_pricing_unit is not None else ''
        if "kilogramme" in product_pricing_unit or "kg" in product_pricing_unit:
            matter = ProductType.SUBSTANCE.name
            unit_of_mesure = "Kg"
            product_pricing_unit = product_pricing_unit.replace(
                "kilogramme", "").replace("kg", "").replace("g", "").replace("gr", "")
        elif "gramme" in product_pricing_unit or "g" in product_pricing_unit or "gr" in product_pricing_unit:
            matter = ProductType.SUBSTANCE.name
            product_pricing_unit = product_pricing_unit.replace(
                "g", "").replace("gr", "")
            unit_of_mesure = "g"

        elif product_pricing_unit.find("pièce") != -1 or product_pricing_unit.find("u") != -1 or product_pricing_unit.find("pce") != -1:
            matter = ProductType.PIECE.name
            product_pricing_unit = product_pricing_unit.replace(
                "pièce", "")
            unit_of_mesure = "piece"
        elif "l" in product_pricing_unit or "litre" in product_pricing_unit:
            matter = ProductType.LIQUID.name
            product_pricing_unit = product_pricing_unit.replace(
                "L", "").replace("litre", "")
            unit_of_mesure = "l"
        else:
            matter = ProductType.OTHER.name

        product_pricing_unit_all = re.findall(
            r"[-+]?\d*\.\d+|\d+", product_pricing_unit)
        product_pricing_unit = product_pricing_unit_all[0] if len(
            product_pricing_unit_all) > 0 else ""
        product_pricing_unit = float(product_pricing_unit) if product_pricing_unit else None
        print(f"unit_of_mesure: {unit_of_mesure}, matter: {matter}, product_pricing_unit: {product_pricing_unit}")
        return unit_of_mesure, matter, product_pricing_unit


class NutritionPicard(Nutrition):
    NUTRITION_MAPPING = {
        # Énergie
        "énergie": "energy_kj",
        "energie": "energy_kj",
        "valeur énergétique kj": "energy_kj",
        "valeur énergétique (kj)": "energy_kj",
        "valeur énergétique kcal": "energy_kcal",
        "valeur énergétique (kcal)": "energy_kcal",
        # Macronutriments
        "matières grasses": "fats",
        "lipides": "fats",
        "dont acides gras saturés": "saturated_fats",
        "acides gras saturés": "saturated_fats",
        "glucides": "carbohydrates",
        "dont sucres": "sugars",
        "sucres": "sugars",
        "fibres alimentaires": "fiber",
        "fibre": "fiber",
        "protéines": "proteins",
        "sel": "salt",
    }
    @classmethod
    @override
    def convert_dict_to_nutrition_object(cls, nutritions: dict | None) -> Nutrition | None:
        if not isinstance(nutritions, dict):
            return None
        nutrition = Nutrition()
        energies = Nutrition.Energy()
        fats = Nutrition.Fats()
        fats_measurement = Nutrition.Fats.get_measurement_unit()
        carbohydrates = Nutrition.Carbohydrates()
        carbohydrates_measurement = Nutrition.Carbohydrates.get_measurement_unit()
        proteins = Nutrition.Proteins()
        proteins_measurement = Nutrition.Proteins.get_measurement_unit()
        minerals = Nutrition.Minerals()
        minerals_measurement = Nutrition.Minerals.get_measurement_unit()
        

        for key, value in nutritions.items():
            print(f"Processing key: {key}, value: {value}")
            # energy
            if key == 'energy_kj':
                energies.kj = convert_to_float(value)
            elif key == 'energy_kcal':
                energies.kcal = convert_to_float(value)

            # macronutrients
            elif key == 'fats':
                fats.fats = convert_to_target_unit(value, fats_measurement)
            elif key == 'saturated_fats':
                fats.saturates = convert_to_target_unit(value, fats_measurement)
            elif key == 'carbohydrates':
                carbohydrates.carbohydrates = convert_to_target_unit(value, carbohydrates_measurement)
            elif key == 'sugars':
                carbohydrates.of_which_sugars = convert_to_target_unit(value, carbohydrates_measurement)
            elif key == 'fiber':
                carbohydrates.dietary_fiber = convert_to_target_unit(value, carbohydrates_measurement)
            elif key == 'proteins':
                proteins.proteins = convert_to_target_unit(value, proteins_measurement)
            elif key == 'salt':
                minerals.salt = convert_to_target_unit(value, minerals_measurement)
            else:
                print(f"Ignored key: {key}, value: {value}")
               
           
        nutrition.energies = energies if not all_attrs_are_none(energies) else None
        nutrition.fats = fats if not all_attrs_are_none(fats) else None
        nutrition.carbohydrates = carbohydrates if not all_attrs_are_none(carbohydrates) else None
        nutrition.proteins = proteins if not all_attrs_are_none(proteins) else None
        nutrition.minerals = minerals if any(getattr(minerals, attr) is not None for attr in vars(minerals)) else None
        nutrition = nutrition if not all_attrs_are_none(nutrition) else None
        
        return nutrition

    @classmethod
    def extract_last_integer(cls, text: str) -> str | None:
        """Extract the last integer from the given text."""
        print(f"Extract the last integer from: {text}")

        pattern = r'(?<=\/\s)(\d+)(?=\s?(?:mL|g))'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else None

    @classmethod
    def process_value(cls, last_value: str, value: str) -> str:
        """Multiply the first number in the value by (100 / last_value) if last_value is present."""
        substring_for_g = "/ " + last_value + " g"
        substring_for_ml = "/ " + last_value + " ml"
        last_value = float(last_value)
        message = ("value:" + str(value))
        if substring_for_g in value:
            match = re.search(r'(\d+(?:\.\d+)?)', value)
            if match:
                number = float(match.group(1))
                doubled_number: float = number * (100/last_value)
                # Format the doubled number to 2 decimal places
                formatted_number = f"{doubled_number:.3f}"
                formatted_number = f"{float(formatted_number):.10f}".rstrip('0').rstrip(
                    '.')  # Format with enough decimal places to handle cases

                output = re.sub(r'(\d+(?:\.\d+)?)', str(formatted_number),
                                value, 1).replace(substring_for_g, "").strip()  # .replace(substring_for_g, "/ 100 g")
                message += f", output: {output}"
                print(message)
                return output
        elif substring_for_ml in value:
            match = re.search(r'(\d+(?:\.\d+)?)', value)
            if match:
                number = float(match.group(1))
                doubled_number: float = number * (100/last_value)
                # Format the doubled number to 2 decimal places
                formatted_number = f"{doubled_number:.3f}"
                formatted_number = f"{float(formatted_number):.10f}".rstrip('0').rstrip(
                    '.')  # Format with enough decimal places to handle cases

                output = re.sub(r'(\d+(?:\.\d+)?)', str(formatted_number),
                                value, 1).replace(substring_for_ml, "").strip()  # .replace(substring_for_ml, "/ 100 ml")
                message += f", output: {output}"
                print(message)
                return output
        print(message)
        return value

    @classmethod
    def compute_nutrition_values_per_100_g_or_ml(cls, nutrition: dict) -> dict:
        '''
        Modify the nutrition values
        '''
        print(f"Modify the nutrition values...")
        if not isinstance(nutrition, dict):
            return None
        for key, value in nutrition.items():
            if not isinstance(value, str):
                nutrition[key] = value
                continue
            last_value = cls.extract_last_integer(value)
            if last_value is not None:
                nutrition[key] = cls.process_value(last_value=last_value.lower(), value=value.lower())
            else:
                try:
                    value = value.replace(',', '.')
                    match = re.search(r'(\d+\.?\d*)', value)
                    if match:
                        nutrition[key] = float(match.group(1))
                    else:
                        nutrition[key] = value
                except Exception:
                    print(f"Erreur lors de la conversion de {key}: {value}, erreur: {e}")
                    nutrition[key] = value
             
        return nutrition

    @classmethod
    def modify_nutrition_in_file(cls, file_path: str, overwrite: bool = False):
        # Step 1: Read the JSON file
        print(f"Step 1: Read the JSON file")
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Step 2: Loop over each item in the list (each product with 'ean')
        print(f"Step 2: Loop over each item in the list")
        for product in data:
            evolutions = product.get('evolutions', [])

            # Step 3: Process each evolution
            print(f"Step 3: Process each evolution")
            for evolution in evolutions:
                if 'nutrition' in evolution:
                    nutrition = evolution['nutrition']
                    # Step 4: Modify the nutrition values
                    nutrition = cls.compute_nutrition_values_per_100_g_or_ml(
                        nutrition=nutrition)
                    nutrition = cls.convert_dict_to_nutrition_object(nutrition)
                    evolution['nutrition'] = nutrition

        # Step 5: Save the modified data back to the same JSON file
        print(f"Step 5: Save the modified data back to the same JSON file")
        file_path = file_path if overwrite else file_path.replace(".json", "_2.json")
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4,
                      ensure_ascii=False,
                      allow_nan=False,
                      default=lambda o: dict(
                          (key, value) for key, value in o.__dict__.items() if value is not None))
        print(f"Nutrition values updated and saved.")

    @classmethod
    def modify_all_nutrition_values(cls):
        folder_path = "src/countries/france/Picard/robots/products/Produits_nutrition"
        json_files = get_all_files_inside_given_folder(folder_path)
        for file_path in json_files:
            print(file_path)
            Nutrition.modify_nutrition_in_file(file_path)


# Custom JSON encoder
def custom_serializer(obj):
    if isinstance(obj, Nutrition):
        return obj.__dict__  # Converts the object's attributes to a dictionary
    raise TypeError(f"Object of type {
                    obj.__class__.__name__} is not JSON serializable")




CONVERT_NUTRITION_DICT_TO_OBJECT = "CONVERT_NUTRITION_DICT_TO_OBJECT"

if __name__ == "__main__":
    cmdargs = sys.argv

    # Print it
    print(f"The total numbers of args passed to the script: {len(cmdargs)}, Args list: {cmdargs}")

    json_file_path = None  

    if CONVERT_NUTRITION_DICT_TO_OBJECT in cmdargs:
        index = cmdargs.index(CONVERT_NUTRITION_DICT_TO_OBJECT)
        json_file_path = str(cmdargs[index + 1]) if len(cmdargs) >= index + 2 else None

    # Si json_file_path est toujours None, afficher une erreur
    if not json_file_path:
        print("Error: No JSON file path provided.")
        sys.exit(1)

   
    NutritionPicard.modify_nutrition_in_file(file_path=json_file_path, overwrite=False)




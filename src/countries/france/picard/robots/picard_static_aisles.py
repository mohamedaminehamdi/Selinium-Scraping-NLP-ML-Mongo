import logging
import os
import sys
from typing import Final, List, Optional, Union

from typing_extensions import override

from src.model.static_category_aisle import StaticAisle, StaticCategory
from src.utils.my_utils import get_filename_from_filepath

sys.path.append("src")
current_file_directory = os.path.dirname(os.path.abspath(__file__))

FOLDER_PATH: Final[str] = os.path.join(current_file_directory, "products")

class CategoryParser:
    @classmethod
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        raise NameError("fatal error, this method should be overriden")

    @staticmethod
    def category_path() -> str:
        raise NameError("fatal error, this method should be overriden")

class PicardPlatsCuisines(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "plats_cuisines")
        os.makedirs(path, exist_ok=True)  
        return path
    _CATEGORY_PATH = category_path.__func__()
    
    TYPE_PLATS_CUISINE = StaticAisle(
        name = "Types de plats cuisinés",
        url = "https://www.picard.fr/rayons/plats-cuisines/types-de-plats-cuisines",
        original_file_uri = os.path.join(_CATEGORY_PATH, "types_plats.json"),
    )

    FORMAT =  StaticAisle(
        name = "Formats",
        url = "https://www.picard.fr/rayons/plats-cuisines/formats",
        original_file_uri = os.path.join(_CATEGORY_PATH, "formats.json"),
    )

    GAMMES = StaticAisle(
        name = "Gammes",
        url = "https://www.picard.fr/rayons/plats-cuisines/gammes",
        original_file_uri = os.path.join(_CATEGORY_PATH, "gammes.json"),    
    )

    aisles: Final[List[StaticAisle]] = [
        TYPE_PLATS_CUISINE,
        FORMAT,
        GAMMES,
    ]
    
    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "TYPE_PLATS_CUISINE":
                    aisles = [cls.TYPE_PLATS_CUISINE]
                case "FORMAT":
                    aisles = [cls.FORMAT]
                case "GAMMES":
                    aisles = [cls. GAMMES]
                    
        return aisles

class PicardAperitifsEtEntrees(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Apéritifs_et_entrées")
        os.makedirs(path, exist_ok=True)  
        return path

    _CATEGORY_PATH = category_path.__func__()
    
    APERITIFS = StaticAisle(
        name = "Apéritifs",
        url = "https://www.picard.fr/rayons/aperitifs-et-entrees/aperitifs",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Aperitifs.json"),
    )

    ENTREES =  StaticAisle (
        name = "Entrées",
        url = "https://www.picard.fr/rayons/plats-cuisines/snacks-salades",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Entrees.json"),
    )

    aisles: Final[List[StaticAisle]] = [
        APERITIFS,
        ENTREES,
       
    ]
    
    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "APERITIFS":
                    aisles = [cls.APERITIFS]
                case "ENTREES":
                    aisles = [cls.ENTREES]
                
                    
        return aisles



class PicardLegumesfruits(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Legumes_et_fruits")
        os.makedirs(path, exist_ok=True) 
        return path
    
    _CATEGORY_PATH = category_path.__func__()
    
    LEGUMES = StaticAisle(
        name = "Légumes",
        url = "https://www.picard.fr/rayons/legumes-et-fruits/legumes",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Legumes.json"),
    )

    FRUITS = StaticAisle(
        name = "Fruits",
        url = "https://www.picard.fr/rayons/legumes-et-fruits/fruits",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Fruits.json"),
    )

    LEGUMES_CUISINE = StaticAisle(
        name = "Légumes cuisinés",
        url = "https://www.picard.fr/rayons/legumes-et-fruits/legumes-cuisines",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Legumes__cuisines.json"),
    )

    FECULENTS = StaticAisle(
        name = "Féculents",
        url = "https://www.picard.fr/rayons/legumes-et-fruits/feculents",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Feculents.json"),
    )

    aisles: Final[List[StaticAisle]] = [
        LEGUMES,
        FRUITS,
        LEGUMES_CUISINE,
        FECULENTS,
    ]

    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "LEGUMES":
                    aisles = [cls.LEGUMES]
                case "FRUITS":
                    aisles = [cls.FRUITS]
                case "LEGUMES_CUISINE":
                    aisles = [cls.LEGUMES_CUISINE]
                case "FECULENTS":
                    aisles = [cls.FECULENTS]

        return aisles



class PicardViandesEtPoissons(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Viandes_et_poissons")
        os.makedirs(path, exist_ok=True)
        return path
    
    _CATEGORY_PATH = category_path.__func__()
    
    VIANDES = StaticAisle(
        name = "Viandes ",
        url = "https://www.picard.fr/rayons/viandes-et-poissons/viandes",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Viandes.json"),
    )

    VOLAILLES = StaticAisle(
        name = "Volailles",
        url = "https://www.picard.fr/rayons/viandes-et-poissons/volailles",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Volailles.json"),
    )

    POISSONS = StaticAisle(
        name = "Poissons",
        url = "https://www.picard.fr/rayons/viandes-et-poissons/poissons",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Poissons.json"),
    )

    FRUITS_DE_MER = StaticAisle(
        name = "Fruits de mer",
        url = "https://www.picard.fr/rayons/viandes-et-poissons/fruits-de-mer",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Fruits_de_mer.json"),
    )

    aisles: Final[List[StaticAisle]] = [
        VIANDES,
        VOLAILLES,
        POISSONS,
        FRUITS_DE_MER,
    ]

    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "VIANDES":
                    aisles = [cls.VIANDES]
                case "VOLAILLES":
                    aisles = [cls.VOLAILLES]
                case "POISSONS":
                    aisles = [cls.POISSONS]
                case "FRUITS_DE_MER":
                    aisles = [cls.FRUITS_DE_MER]

        return aisles

  
    
class PicardPainsETViennoiseries(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Pains_et_viennoiseries")
        os.makedirs(path, exist_ok=True)  
        return path
    
    _CATEGORY_PATH = category_path.__func__()
    
    VIENNOISERIES = StaticAisle(
        name = "Viennoiseries",
        url = "https://www.picard.fr/rayons/pains-et-patisseries/patisseries",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Viennoiseries.json"),
    )

    PAINS = StaticAisle(
        name = "Pains",
        url = "https://www.picard.fr/rayons/pains-et-patisseries/pains-viennoiseries",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Pains.json"),
    )

    PATES_CUIRE = StaticAisle(
        name = "Pâtes à cuire",
        url = "https://www.picard.fr/rayons/pains-et-patisseries/pates-a-cuire",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Pates_cuire.json"),
    )

   

    aisles: Final[List[StaticAisle]] = [
        VIENNOISERIES,
        PAINS,
        PATES_CUIRE,
    ]

    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "VIENNOISERIES":
                    aisles = [cls.VIENNOISERIES]
                case "PAINS":
                    aisles = [cls.PAINS]
                case "Pates_cuire":
                    aisles = [cls.PATES_CUIRE]
                

        return aisles
    
class PicardPromotions(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Promotions")
        os.makedirs(path, exist_ok=True)  
        return path
    
    _CATEGORY_PATH = category_path.__func__()
    
    PROMOTION_DU_MOMENT = StaticAisle(
        name = "Promotions du moment",
        url = "https://www.picard.fr/rayons/promotions/promotions-du-moment",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Promotions.json"),
    )

   

   

    aisles: Final[List[StaticAisle]] = [
        PROMOTION_DU_MOMENT,
       
    ]

    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        
        print(f"selected_aisle: {split_list}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            selected_aisle = split_list[-1].replace("-", "_").upper()
            print(f"selected_aisle: {selected_aisle}")
            
            match selected_aisle:
                case "PROMOTION_DU_MOMENT":
                    aisles = [cls.PROMOTION_DU_MOMENT]
                case _:
                    print(f"Rayon non reconnu: {selected_aisle}")
                    raise ValueError(f"Rayon non reconnu: {args}")

        return aisles
              
                

  

class PicardGlaceEtSorbets(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Glaces_et_sorbets")
        os.makedirs(path, exist_ok=True)  
        return path
    
    _CATEGORY_PATH = category_path.__func__()
    
    PARFUMS = StaticAisle(
        name = "Parfums",
        url = "https://www.picard.fr/rayons/glaces-et-sorbets/parfums",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Parfums.json"),
    )

    TYPES_FORMATS = StaticAisle(
        name = "Types, Formats",
        url = "https://www.picard.fr/rayons/glaces-et-sorbets/types-formats",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Types_Formats.json"),
    )

    MARQUES = StaticAisle(
        name = "Marques",
        url = "https://www.picard.fr/rayons/glaces-et-sorbets/marques",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Marques.json"),
    )

  
    aisles: Final[List[StaticAisle]] = [
        PARFUMS,
        TYPES_FORMATS,
        MARQUES,
    ]

    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "PARFUMS":
                    aisles = [cls.PARFUMS]
                case "TYPES_FORMATS":
                    aisles = [cls.TYPES_FORMATS]
                case "MARQUES":
                    aisles = [cls.MARQUES]
               
        return aisles



class PicardCuisineDuMonde(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Cuisine_du_monde")
        os.makedirs(path, exist_ok=True) 
        return path
    
    _CATEGORY_PATH = category_path.__func__()
    
    PAYS = StaticAisle(
        name = "Pays",
        url = "https://www.picard.fr/rayons/cuisine-du-monde/pays",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Pays.json"),
    )

    TYPES_DE_PLATS = StaticAisle(
        name = "Types de plat",
        url = "https://www.picard.fr/rayons/cuisine-du-monde/types-de-plat",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Types_de_plat.json"),
    )

    FORMATS = StaticAisle(
        name = "Formats",
        url = "https://www.picard.fr/rayons/cuisine-du-monde/formats",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Formats.json"),
    )

   

    aisles: Final[List[StaticAisle]] = [
        PAYS,
        TYPES_DE_PLATS,
        FORMATS,
      
    ]

    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "PAYS":
                    aisles = [cls.PAYS]
                case "TYPES_DE_PLATS":
                    aisles = [cls.TYPES_DE_PLATS]
                case "FORMATS":
                    aisles = [cls.FORMATS]
               

        return aisles

 
 
class PicardPizzasEtTartes(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Pizzas_et_tartes")
        os.makedirs(path, exist_ok=True)  
        return path
    
    _CATEGORY_PATH = category_path.__func__()
    
    PIZZAS = StaticAisle(
        name = "Pizzas",
        url = "https://www.picard.fr/rayons/pizzas-et-tartes/pizzas",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Pizzas.json"),
    )

    TARTES_SALEES = StaticAisle(
        name = "Tartes salées",
        url = "https://www.picard.fr/rayons/pizzas-et-tartes/tartes-salees",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Tartes_salees.json"),
    )

   

    aisles: Final[List[StaticAisle]] = [
        PIZZAS,
        TARTES_SALEES,
       
    ]

    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "PIZZAS":
                    aisles = [cls.PIZZAS]
                case "TARTES_SALEES":
                    aisles = [cls.TARTES_SALEES]
               
        return aisles

 


class PicardRegimesAlimentairesNutrition(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Regimes_alimentaires_et_nutrition")
        os.makedirs(path, exist_ok=True)  
        return path
    
    _CATEGORY_PATH = category_path.__func__()
    
    REGIMES_ALIMENTAIRES = StaticAisle(
        name = "Régimes alimentaires",
        url = "https://www.picard.fr/rayons/regimes-alimentaires-et-nutrition/regimes-alimentaires",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Regimes_alimentaires.json"),
    )

    NUTRITION = StaticAisle(
        name = "Nutrition",
        url = "https://www.picard.fr/rayons/regimes-alimentaires-et-nutrition/nutrition",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Nutrition.json"),
    )

  
    aisles: Final[List[StaticAisle]] = [
        REGIMES_ALIMENTAIRES,
        NUTRITION,
        
    ]

    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "REGIMES_ALIMENTAIRES":
                    aisles = [cls.REGIMES_ALIMENTAIRES]
                case "NUTRITION":
                    aisles = [cls.NUTRITION]
                
        return aisles


   

class PicardEpicerie(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Epicerie")
        os.makedirs(path, exist_ok=True)
        return path
    
    _CATEGORY_PATH = category_path.__func__()
    
    EPICERIE_SALEE = StaticAisle(
        name = "Épicerie salée",
        url = "https://www.picard.fr/rayons/epicerie/epicerie-salee",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Epicerie_salee.json"),
    )

    EPICERIE_SUCREE = StaticAisle(
        name = "Épicerie sucrée",
        url = "https://www.picard.fr/rayons/epicerie/epicerie-sucree",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Epicerie_sucree.json"),
    )

 

    aisles: Final[List[StaticAisle]] = [
        EPICERIE_SALEE,
        EPICERIE_SUCREE,
       
    ]

    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "EPICERIE_SALEE":
                    aisles = [cls.EPICERIE_SALEE]
                case "EPICERIE_SUCREE":
                    aisles = [cls.EPICERIE_SUCREE]
            

        return aisles
        

class PicardDesserts(CategoryParser):
    @staticmethod
    @override
    def category_path() -> str:
        path = os.path.join(FOLDER_PATH, "Desserts")
        os.makedirs(path, exist_ok=True)
        return path
    
    _CATEGORY_PATH = category_path.__func__()

    PATISSERIES = StaticAisle(
        name = "Pâtisseries",
        url = "https://www.picard.fr/rayons/desserts/patisseries",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Patisseries.json"),
    )

    DESSERTS_GLACES = StaticAisle(
        name = "Desserts glacés",
        url = "https://www.picard.fr/rayons/desserts/desserts-glaces",
        original_file_uri = os.path.join(_CATEGORY_PATH, "Desserts_glaces.json"),
    )

 

    aisles: Final[List[StaticAisle]] = [
        PATISSERIES,
        DESSERTS_GLACES,
       
    ]

    @classmethod
    @override
    def get_aisles(cls, args: str) -> List[StaticAisle]:
        aisles: List[StaticAisle] = []
        split_list = args.split(".")
        selected_aisle = split_list[1].upper() if len(split_list) > 1 else None
        print(f"selected_aisle: {selected_aisle}")

        if len(split_list) == 1:
            aisles = cls.aisles
        else:
            match selected_aisle:
                case "PATISSERIES":
                    aisles = [cls.PATISSERIES]
                case "DESSERTS_GLACES":
                    aisles = [cls.DESSERTS_GLACES]
                    
        return aisles
        
  




picard_categories_with_uris: Final[list[StaticCategory]] = [
    StaticCategory(
        name = "Plats cuisinés",
        url = "https://www.picard.fr/rayons/plats-cuisines",
        aisles = PicardPlatsCuisines.aisles,
    ),
    
    StaticCategory(
        name = "Apéritifs et entrées",
        url = "https://www.picard.fr/rayons/aperitifs-et-entrees",
        aisles = PicardAperitifsEtEntrees.aisles,
    ),
    
    StaticCategory(
        name = "Viandes et poissons",
        url = "https://www.picard.fr/rayons/viandes-et-poissons",
        aisles = PicardViandesEtPoissons.aisles,
    ),
    
    StaticCategory(
        name = "Légumes et fruits",
        url = "https://www.picard.fr/rayons/legumes-et-fruits",
        aisles = PicardLegumesfruits.aisles,
    ),
    StaticCategory(
        name = "Pains et viennoiseries",
        url = "https://www.picard.fr/rayons/pains-et-viennoiseries",
        aisles = PicardPainsETViennoiseries.aisles,
    ),
    
    StaticCategory(
        name = "Desserts",
        url = "https://www.picard.fr/rayons/desserts",
        aisles = PicardDesserts.aisles,
    ),
    
    StaticCategory(
        name = "Glaces et sorbets",
        url = "https://www.picard.fr/rayons/glaces-et-sorbets",
        aisles = PicardGlaceEtSorbets.aisles,
    ),
    
    StaticCategory(
        name = "Cuisine du monde",
        url = "https://www.picard.fr/rayons/cuisine-du-monde",
        aisles = PicardCuisineDuMonde.aisles,
    ),
    
    StaticCategory(
        name = "Pizzas et tartes",
        url = "https://www.picard.fr/rayons/pizzas-et-tartes",
        aisles = PicardPizzasEtTartes.aisles,
    ),
    
     StaticCategory(
        name = "Régimes alimentaires et nutrition",
        url = "https://www.picard.fr/rayons/regimes-alimentaires-et-nutrition",
        aisles = PicardRegimesAlimentairesNutrition.aisles,
    ),
    
       StaticCategory(
        name = "Épicerie",
        url = "https://www.picard.fr/rayons/epicerie",
        aisles = PicardEpicerie.aisles,
    ),
       
    
     StaticCategory(
        name = "Promotions",
        url = "https://www.picard.fr/rayons/promotions",
        aisles = PicardPromotions.aisles,
    )
]






def get_static_aisles_from_user_cmdargs(cmdargs: list[str]) -> list[StaticAisle]:
    """
    first argument can be either: category name or aisle name or file path
    """
    if not isinstance(cmdargs, list):
        return []
    aisles: list[StaticAisle] = []
    if len(cmdargs) == 1:
        logging.warning(
            f"Parse ALL categories at once will take a lot of time!! parse them one by one!"
        )
        print("\033[91mThis is red text\033[0m")
        sys.exit()
        for category in picard_categories_with_uris:
            print(
                f"""category.name: {category.name}, 
                  aisles length: {len(category.aisles)}"""
            )
            aisles += category.aisles

    elif len(cmdargs) >= 2:
        print(f"going to parse: {cmdargs[1]}")
        if os.path.isdir(cmdargs[1]):
            logging.error(
                f"args should be a file or aisle not a folder, args:{cmdargs[1]}"
            )
            sys.exit()
        elif os.path.isfile(cmdargs[1]):
            res = get_filename_from_filepath(cmdargs[1])
            print(f"file name to parse: {res}")
            sys.exit()
            aisle = StaticAisle(
                name=str(res),
                url=None,
                original_file_uri=cmdargs[1],
                created_from_file=True,
            )
            aisles.append(aisle)
            print(f"aisles to parse: {aisles}")

        else:
            split_list = cmdargs[1].split(".")
            category = split_list[0] if len(split_list) > 1 else cmdargs[1]
            match category:
                case "PicardPlatsCuisines":
                    aisles = PicardPlatsCuisines.get_aisles(cmdargs[1])
                case "PicardAperitifsEtEntrees":
                    aisles = PicardAperitifsEtEntrees.get_aisles(cmdargs[1])
                case "PicardLegumesfruits":
                    aisles = PicardLegumesfruits.get_aisles(cmdargs[1])
                case "PicardPainsETViennoiseries":
                    aisles =PicardPainsETViennoiseries.get_aisles(cmdargs[1])
                case "PicardPizzasEtTartes":
                    aisles = PicardPizzasEtTartes.get_aisles(cmdargs[1])
                case "PicardRegimesAlimentairesNutrition":
                    aisles = PicardRegimesAlimentairesNutrition.get_aisles(cmdargs[1])
                case "PicardCuisineDuMonde":
                    aisles = PicardCuisineDuMonde.get_aisles(cmdargs[1])
                case "PicardPromotions":
                    aisles = PicardPromotions.get_aisles(cmdargs[1])
                case "PicardViandesEtPoissons":
                    aisles = PicardViandesEtPoissons.get_aisles(cmdargs[1])
                case "PicardDesserts":
                    aisles = PicardDesserts.get_aisles(cmdargs[1]) 
                case "PicardGlaceEtSorbets":
                    aisles = PicardGlaceEtSorbets.get_aisles(cmdargs[1])
                case "PicardEpicerie":
                    aisles = PicardEpicerie.get_aisles(cmdargs[1])

                case _:
                    logging.error(f"args source not found: {cmdargs[1]}")
                    sys.exit()
                    
        return aisles
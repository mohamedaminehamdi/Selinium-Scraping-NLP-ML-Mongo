from __future__ import annotations
import json
import os
import sys
from pydantic.dataclasses import dataclass
from dataclasses import asdict
from datetime import datetime
from typing import Callable, Final, List, Optional
from pydantic import BaseModel, ValidationError

from src.model.static_category_aisle import StaticAisle
from src.utils.ean_country_checker import get_country_code_from_country_name_in_french_lang, get_country_code_from_ean
from src.utils.my_utils import days_between, extract_folder_and_file, get_latest_file_in_folder, xstr

parent_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..', '..', 'utils'))
sys.path.append(parent_dir)

# Clean Architecture: 1. Entities (Domain Layer)


@dataclass
class Category:
    id: Optional[int] = None
    label: Optional[str] = None

    @classmethod
    def from_dict_to_object(cls, data: dict):
        # u = Category(**data)
        # print("u.label: " + str(u.label))

        if isinstance(data, dict):
            id1 = data.get("id")
            label = data.get("label")
            item = Category(id=id1, label=label)
            return item
        return None

    def __str__(self):
        value = (f"id: {xstr(self.id)}, label: {xstr(self.label)}")
        return value

    def __eq__(self, other):
        return (self.id == other.id)  # and (self.g == other.g)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.id < other.id)  # and (self.g < other.g)

    def __gt__(self, other):
        return (self.id > other.id)  # and (self.g > other.g)

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)


@dataclass
class CustomerReviews:
    average: Optional[float] = None
    count: Optional[int] = None

    def __eq__(self, other):
        '''
        Custom equality comparison based on count
        '''
        if not isinstance(other, CustomerReviews):
            return NotImplemented
        return self.count == other.count

    @classmethod
    def from_dict_to_object(cls, data: dict):
        if isinstance(data, dict):
            average = data.get("average")
            count = data.get("count")
            item = CustomerReviews(average=average, count=count)
            return item
        return None


@dataclass
class Links:
    links_self: Optional[str] = None
    reviews: Optional[str] = None

    @classmethod
    def from_dict_to_object(cls, dict_links: dict):
        if isinstance(dict_links, dict):
            links = dict_links.get("self")
            reviews = dict_links.get("reviews")
            links = Links(links_self=links, reviews=reviews)
            return links


@dataclass
class Market:
    name: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None

    @classmethod
    def from_dict_to_object(cls, product: dict):
        market_name = product.get("market")
        market_address = product.get("address")
        market_country = product.get("market_country") or "FR"
        return Market(name=market_name, country=market_country, address=market_address)


@dataclass
class Origin:
    ean: Optional[str] = None
    explicit: Optional[str] = None
    partial: Optional[str] = None

    @classmethod
    def from_dict_to_object(cls, product: dict):
        ean = product.get("ean")
        origin_dict = product.get("origin", {})
        explicit = origin_dict.get("explicit") if isinstance(origin_dict, dict) else origin_dict
        partial = origin_dict.get("partial") if isinstance(origin_dict, dict) else None
        
        ean_code = get_country_code_from_ean(ean=ean) if ean else None
        if explicit and not explicit in ["FR", "EU", "IT", "DE", "ES"]:  
            explicit = get_country_code_from_country_name_in_french_lang(explicit)

        return cls(
            ean=ean_code,
            explicit=explicit if explicit else None,
            partial=partial
        )


@dataclass
class Freshness:
    value: Optional[int] = None
    period: Optional[str] = None

    @classmethod
    def from_dict_to_object(cls, product: dict):
        raise NameError("fatal error, this method should be overriden")

    def get_freshness_days_from_object(self) -> Optional[int]:
        freshness_value = None
        """convert Freshness object to number of freshness days"""
        if self.value is None or self.period is None:
            return None

        if self.period == 'WEEK':
            freshness_value = self.value * 7
        elif self.period == 'DAY':
            freshness_value = self.value * 1
        elif self.period == 'MONTH':
            freshness_value = self.value * 30
        return freshness_value


@dataclass
class Treenuts:
    treenuts1: Optional[bool] = None
    almonds: Optional[bool] = None
    walnuts: Optional[bool] = None
    cashews: Optional[bool] = None
    pecans: Optional[bool] = None
    pistachios: Optional[bool] = None
    hazelnuts: Optional[bool] = None
    macadamianuts: Optional[bool] = None
    brazilnuts: Optional[bool] = None

    @property
    def treenuts(self) -> Optional[bool]:
        return self.treenuts1 or self.almonds or self.walnuts or self.cashews or self.pecans or self.pistachios or self.hazelnuts or self.macadamianuts or self.brazilnuts


@dataclass
class Crustacean:
    shrimp: Optional[bool] = None
    crab: Optional[bool] = None
    lobster: Optional[bool] = None
    crayfish: Optional[bool] = None
    prawn: Optional[bool] = None

    @property
    def treenuts(self) -> Optional[bool]:
        return self.shrimp or self.crab or self.lobster or self.crayfish or self.prawn


@dataclass
class Mollusk:
    squid: Optional[bool] = None
    octopus: Optional[bool] = None
    mussels: Optional[bool] = None
    snails: Optional[bool] = None
    clams: Optional[bool] = None
    oysters: Optional[bool] = None
    abalone: Optional[bool] = None
    scallops: Optional[bool] = None

    @property
    def mollusk(self) -> Optional[bool]:
        return self.squid or self.octopus or self.mussels or self.snails or self.clams or self.oysters or self.abalone or self.scallops


@dataclass
class Fish:
    salmon: Optional[bool] = None
    tuna: Optional[bool] = None
    cod: Optional[bool] = None
    haddock: Optional[bool] = None

    @property
    def fish(self) -> Optional[bool]:
        return self.salmon or self.tuna or self.cod or self.haddock


@dataclass
class Allergens:
    treenuts: Optional[Treenuts] = None
    crustacean: Optional[Crustacean] = None
    mollusk: Optional[Mollusk] = None
    fish: Optional[Fish] = None
    eggs: Optional[bool] = None
    soy: Optional[bool] = None
    gluten: Optional[bool] = None
    wheat: Optional[bool] = None
    sesame: Optional[bool] = None
    mustard: Optional[bool] = None
    lupin: Optional[bool] = None
    sulphites: Optional[bool] = None
    lactose: Optional[bool] = None

    @classmethod
    def from_dict_to_object(cls, product: dict):
        raise NameError("fatal error, this method should be overriden")


@dataclass
class Label:
    bio: Optional[bool] = None
    frozen: Optional[bool] = None
    halal: Optional[bool] = None
    dye: Optional[bool] = None
    preservative: Optional[bool] = None
    additive: Optional[bool] = None
    fr_greengrocery: Optional[bool] = None
    pregnancy_unsafe: Optional[bool] = None
    lactose: Optional[bool] = None
    vegan: Optional[bool] = None
    vegetarian: Optional[bool] = None
    # aucune forme de sucre, ni naturellement présent ni ajouté
    sugar_free: Optional[bool] = None
    sugar_added_free: Optional[bool] = None
    sel_free: Optional[bool] = None
    # https://www.carrefour.fr/p/haricots-verts-sans-sel-ajoute-bio-jardin-bio-etic-3760020505943
    sel_added_free: Optional[bool] = None
    caffeine_free: Optional[bool] = None
    gluten_free: Optional[bool] = None
    gmo_free: Optional[bool] = None
    fat_free: Optional[bool] = None
    # https://www.carrefour.fr/p/jambon-superieur-sans-nitrite-carrefour-extra-3560071449681
    nitrite_free: Optional[bool] = None

    # Changement temporaire de recette: https://www.carrefour.fr/p/ravioles-au-saint-marcellin-reflets-de-france-3560070430109

    @classmethod
    def from_dict_to_object(cls, product: dict):
        raise NameError("fatal error, this method should be overriden")


@dataclass
class Desc:
    title: Optional[str] = None
    packaging: Optional[str] = None
    desc: Optional[str] = None
    images: Optional[List[str]] = None
    links: Optional[Links] = None

    def __eq__(self, other):
        '''
        Custom equality comparison based on description
        '''
        if not isinstance(other, Desc):
            return NotImplemented
        return self.desc == other.desc

    def __hash__(self):
        return hash(self.desc)

    @classmethod
    def from_dict_to_object(cls, desc: dict | None) -> Desc | None:
        if isinstance(desc, dict):
            details_desc_title = desc.get("title")
            details_desc_packaging = desc.get("packaging")
            details_desc = desc.get("desc")
            details_desc_images = desc.get("images")
            links = desc.get("links")
            links = Links(links.get("self"), links.get(
                "reviews")) if links is not None else None

            desc1 = Desc(desc=details_desc, images=details_desc_images, links=links,
                         packaging=details_desc_packaging, title=details_desc_title)
            return desc1
        return None

    def to_dict(self):

        # Convert the object to a dictionary and remove fields that are None
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class LangDesc:
    fr: Optional[Desc] = None
    en: Optional[Desc] = None
    de: Optional[Desc] = None
    es: Optional[Desc] = None
    it: Optional[Desc] = None

    def __eq__(self, other):
        '''
        Custom equality comparison based on description
        '''
        if not isinstance(other, LangDesc):
            return NotImplemented
        return self.fr == other.fr and self.en == other.en and self.es == other.es and self.it == other.it

    def __hash__(self):
        return hash((self.fr, self.en, self.de, self.es, self.it))

    @classmethod
    def from_dict_to_object(cls, lang_desc: dict):
        if isinstance(lang_desc, dict):
            details_desc_fr = lang_desc.get("FR")
            details_desc_fr = Desc.from_dict_to_object(details_desc_fr)

            details_desc_en = lang_desc.get("EN")
            details_desc_en = Desc.from_dict_to_object(details_desc_en)

            details_desc_de = lang_desc.get("DE")
            details_desc_de = Desc.from_dict_to_object(details_desc_de)

            details_desc_es = lang_desc.get("ES")
            details_desc_es = Desc.from_dict_to_object(details_desc_es)

            details_desc_it = lang_desc.get("IT")
            details_desc_it = Desc.from_dict_to_object(details_desc_it)

            desc = LangDesc(fr=details_desc_fr, en=details_desc_en,
                            de=details_desc_de, es=details_desc_es, it=details_desc_it)
            return desc


@dataclass
class Offer:
    id: Optional[str] = None
    description: Optional[LangDesc] = None
    requiredProductQuantity: Optional[int] = None

    @classmethod
    def extractInfo(cls, desc: str) -> 'Offer':
        raise NameError("fatal error, extractInfo should be overriden")

    def __eq__(self, other):
        '''
        Custom equality comparison based on description
        '''
        if not isinstance(other, Offer):
            return NotImplemented
        return self.description == other.description

    def __hash__(self):
        '''
        Custom hash function based on description for using in sets
        '''
        return hash(self.description)


@dataclass
class Nutrition:
    '''
    La différence entre "acides gras saturés" et "dont acides gras saturés" dans les tableaux nutritionnels est importante :
    "Acides gras saturés" : fait référence à la quantité totale de graisses saturées présentes dans un aliment.
    Ce sont les graisses qui augmentent le taux de cholestérol LDL et sont considérées comme moins saines en excès.
    "Dont acides gras saturés" : est généralement utilisé sous la catégorie "Matières grasses" (graisses totales).
    Cela indique la proportion de graisses totales qui sont saturées. Autrement dit, c'est une sous-catégorie du total des matières grasses.
    Exemple dans un tableau nutritionnel :
    Matières grasses : 10 g
    Dont acides gras saturés : 3 g
    Cela signifie que sur les 10 g de matières grasses, 3 g sont des acides gras saturés.
    '''

    '''
    La différence entre "dont sucres" et "sucres" dans un tableau nutritionnel est similaire à celle des acides gras saturés.
    Sucres : fait référence à la quantité totale de sucres naturellement présents et ajoutés dans un aliment.
    Cela inclut tous les types de sucres, qu'ils soient naturellement présents dans les fruits, les produits laitiers, etc., ou ajoutés lors de la transformation.
    Dont sucres : est généralement utilisé sous la catégorie "Glucides". Il indique la part des glucides qui sont des sucres simples.
    En d'autres termes, il s'agit de la quantité de sucres simples (glucose, fructose, saccharose) dans la totalité des glucides présents.
    Exemple dans un tableau nutritionnel :
    Glucides : 20 g
    Dont sucres : 10 g
    Cela signifie que sur les 20 g de glucides, 10 g sont des sucres simples.
    Glucides = Sucres simples (glucides simples, qu'ils soient d'origine naturelle ou ajoutés) + Sucres complexes (amidon, Les fibres alimentaires)
    Carbohydrates: category
        ==> Sugars: subcategory
            ==> Of which Sugars (added sugars)
        ==> Fiber: subcategory
    '''
    # Energy
    @dataclass
    class Energy:
        kj: Optional[float] = None
        kcal: Optional[float] = None

    # Macronutrients ====:>
    # fats
    @dataclass
    class Fats:
        fats: Optional[float] = None
        saturates: Optional[float] = None

        @classmethod
        def get_measurement_unit(cls) -> str:
            return "g"

    # proteins
    @dataclass
    class Proteins:
        proteins: Optional[float] = None

        @classmethod
        def get_measurement_unit(cls) -> str:
            return "g"

    # carbohydrates section

    @dataclass
    class Carbohydrates:
        carbohydrates: Optional[float] = None  # carbohydrates
        sugars: Optional[float] = None  # (simple carbohydrates)
        of_which_sugars: Optional[float] = None  # carbohydrates
        fiber: Optional[float] = None  # (indigestible carbohydrates)
        # carbohydrates Dietary fiber specifically refers to the naturally occurring fiber found in whole foods such as fruits, vegetables, grains, and legumes.
        dietary_fiber: Optional[float] = None
        # They are used as sweeteners and can provide fewer calories than regular sugars.Common polyols include sorbitol, mannitol, xylitol, and erythritol.
        polyols: Optional[float] = None
        starch: Optional[float] = None  # (complex carbohydrates)
        lactose: Optional[float] = None
        gal: Optional[float] = None

        @classmethod
        def get_measurement_unit(cls) -> str:
            return "g"

    # Vitamins

    @dataclass
    class Vitamins:
        vitamin_a: Optional[float] = None
        vitamin_b1: Optional[float] = None  # thiamine
        vitamin_b2: Optional[float] = None  # riboflavine
        vitamin_b3: Optional[float] = None  # niacin
        vitamin_b5: Optional[float] = None  # pantothenic_acid
        vitamin_b6: Optional[float] = None  # Pyridoxine
        vitamin_b7: Optional[float] = None  # biotin
        vitamin_b9: Optional[float] = None  # folic_acid
        vitamin_b12: Optional[float] = None  # Cobalamin
        vitamin_c: Optional[float] = None
        vitamin_d: Optional[float] = None
        vitamin_e: Optional[float] = None
        vitamin_k: Optional[float] = None

        @classmethod
        def get_measurement_unit(cls) -> str:
            return "mg"

    # minerals
    @dataclass
    class Minerals:
        sodium: Optional[float] = None  # mineral
        salt: Optional[float] = None  # mineral or sodium
        calcium: Optional[float] = None  # mineral g and mg
        manganese: Optional[float] = None  # mineral g, mg, ug
        magnesium: Optional[float] = None  # mineral g, mg
        potassium: Optional[float] = None  # mineral g, mg
        phosphorus: Optional[float] = None  # mineral g, mg
        iron: Optional[float] = None  # mineral g, mg
        zinc: Optional[float] = None  # mineral g, mg
        iodine: Optional[float] = None  # mineral ug only
        chloride: Optional[float] = None  # mineral
        copper: Optional[float] = None  # mineral ug, g, mg
        fluoride: Optional[float] = None  # mineral
        selenium: Optional[float] = None  # mineral ug
        chromium: Optional[float] = None  # mineral mg

        @classmethod
        def get_measurement_unit(cls) -> str:
            return "mg"

    # Fatty acids
    @dataclass
    class FattyAcids:
        omega_3: Optional[float] = None  # Fatty Acids
        saturated_fatty_acids: Optional[float] = None  # saturated fatty acids
        monounsaturated_fatty_acids: Optional[float] = None  # Fatty Acids
        # Fatty Acids
        including_monounsaturated_fatty_acids: Optional[float] = None
        # Fatty Acids
        including_polyunsaturated_fatty_acids: Optional[float] = None
        linoleic_acid: Optional[float] = None  # omega-6 fatty acid
        alpha_linolenic_acid: Optional[float] = None  # omega-3 fatty acid

        @classmethod
        def get_measurement_unit(cls) -> str:
            return "g"

    # Essential Nutrients or Vitamin-like

    @dataclass
    class VitaminLikes:
        choline: Optional[float] = None
        inositol: Optional[float] = None
        lcarnitine: Optional[float] = None
        fos: Optional[float] = None
        gos: Optional[float] = None

        @classmethod
        def get_measurement_unit(cls) -> str:
            return "mg"

    energies: Optional[Energy] = None
    vitamins: Optional[Vitamins] = None
    minerals: Optional[Minerals] = None
    fatty_acids: Optional[FattyAcids] = None
    vitamin_likes: Optional[VitaminLikes] = None
    fats: Optional[Fats] = None
    proteins: Optional[Proteins] = None
    carbohydrates: Optional[Carbohydrates] = None
    unknown: Optional[dict] = None
    '''
    In the EU and UK, the term "salt" on nutrition table is the equivalent amount of sodium chloride, not just sodium. 
    It is often calculated as: Salt(g)=Sodium(g) x 2.5
    This formula reflects the conversion from sodium to salt (NaCl), as sodium makes up about 40% of the weight of salt.
    In countries like the U.S., the term "sodium" is often used directly on nutrition labels rather than "salt." 
    Here, the focus is on the actual sodium content, and the amount of sodium is listed in milligrams (mg).
    '''
    '''
    assumption 1 mL = 1 gr for Water-Based Solutions (e.g., Juice, Milk)
    Oil has a density of about 0.92 g/mL, so 1 mL ≈ 0.92 grams.
    Salt is a combination of two minerals: sodium and chloride.
    so it can be classified under mineral section or under sedium section
    '''

    '''
    In nutrition tables, salt is often listed under sodium, 
    since sodium is the component that has more relevance for health
    '''

    @classmethod
    def convert_dict_to_nutrition_object(cls, nutritions: dict) -> 'Nutrition':
        """
        Def:
            Converts a fr/de/es/it nutrition names to its English equivalent.

        Args:
            nutrition_name (str): The dict nutrition names.

        Returns:
            str: The english nutrition object.
        """
        raise NameError(
            "fatal error, convert_dict_to_nutrition_object should be overriden")


@dataclass
class Evolution:
    parsing_date: str = datetime.now().isoformat(timespec="minutes")
    format: Optional[str] = None
    format2: Optional[str] = None
    availability: Optional[bool] = True
    nutriscore: Optional[str] = None
    certification: Optional[str] = None
    nutrition: Optional[Nutrition] = None
    ingredients: Optional[str] = None
    ingredients_clean: Optional[str] = None
    ingredients_ia: Optional[List[str]] = None
    allergens: Optional[List[str]] = None
    reviews: Optional[CustomerReviews] = None
    on_discount: Optional[bool] = None
    weight_per_packaging: Optional[float] = None
    price_per_packaging: Optional[float] = None
    price_per_packaging_with_discount: Optional[float] = None
    price_per_unit: Optional[float] = None
    price_per_unit_with_discount: Optional[float] = None
    is_organic: Optional[bool] = None
    is_vegan: Optional[bool] = None
    offers: Optional[List[Offer]] = None

    @classmethod
    def merge_evolutions(cls, new_evolution: 'Evolution', old_evolutions: List['Evolution'], equality_func: Callable[['Evolution', 'Evolution'], bool | None]) -> List[Evolution]:
        all_evolutions: List[Evolution] = []
        if old_evolutions:
            latest_evol = Evolution.latest_evolution(old_evolutions)
            is_equal = equality_func(latest_evol, new_evolution) if latest_evol and new_evolution else None
            short_delta = Evolution.short_delta(new_evolution, latest_evol) if latest_evol else None
            if is_equal and short_delta:
                # keep only the new_evolution and remove the latest_evol
                print("old_evolutions len: " + str(len(old_evolutions)))
                if latest_evol:
                    old_evolutions.remove(latest_evol)
                print("old_evolutions len: " + str(len(old_evolutions)))
            elif is_equal and not short_delta:
                # create new evolution containing only a date
                new_evolution = Evolution()
            elif not is_equal:
                # keep the new created evolution:
                print("nothing to do")
            all_evolutions.extend(old_evolutions)
        all_evolutions.append(new_evolution)
        return all_evolutions

    @classmethod
    def is_shallow_equal(cls, l: 'Evolution', r: 'Evolution') -> bool | None:
        '''
        Custom equality comparison based on price_per_unit
        '''
        if not l or not r:
            return None
        return l.price_per_unit == r.price_per_unit and l.availability == r.availability

    @classmethod
    def is_medium_equal(cls, l: 'Evolution', r: 'Evolution') -> bool | None:
        '''
        Custom medium equality comparison based on the infos available on products list
        '''
        raise NameError("fatal error, this method should be overriden")

    @classmethod
    def is_deep_equal(cls, l: 'Evolution', r: 'Evolution') -> bool | None:
        '''
        Custom deep equality comparison based on all params
        '''
        result = False
        if not cls.is_medium_equal(l=l, r=r):
            print("is_deep_equal 1")
            result = False
        elif l.has_details() and r.has_details():
            if l.nutrition == r.nutrition and l.certification == r.certification and l.ingredients == r.ingredients:
                result = True
                print("is_deep_equal 2")
            else:
                result = False
                print("is_deep_equal 3")
        else:
            result = True
            print("is_deep_equal 4")

        print(f"is_deep_equal, l.None?: {
              l is not None}, r.None?: {r is not None}: {result}")
        return result

    @classmethod
    def short_delta(cls, l: 'Evolution', r: 'Evolution', delta_threshold: int = 7) -> bool | None:
        '''
        Custom deep equality comparison based on all params
        '''
        if not isinstance(l, Evolution) or not isinstance(r, Evolution):
            return None
        delta = days_between(l.parsing_date, r.parsing_date)
        if delta and delta <= delta_threshold:
            return True
        return False

    def __eq__(self, other):
        '''
        should not be used, use: is_deep_equal or is_shallow_equal
        '''
        return NotImplemented

    def __lt__(self, other):
        '''
        Custom sorting method (comparison by parsing_date)
        '''
        if not isinstance(other, Evolution):
            return NotImplemented
        return self.parsing_date > other.parsing_date

    def has_details(self) -> bool:
        # print("nutrition: " + str(self.nutrition))
        return self.nutrition is not None

    @classmethod
    def latest_evolution(cls, evolutions: List['Evolution']) -> Evolution | None:
        print("newest_evolution1...")
        if not isinstance(evolutions, List) or len(evolutions) == 0:
            return None
        import datetime

        # exclude evolutions that have only dates
        filtered_evolutions = [
            evol for evol in evolutions if evol.price_per_unit is not None]
        # either this:
        # return max(evolutions, key=lambda evo: datetime.datetime.fromisoformat(evo.parsing_date))
        # or this:
        sorted_list = sorted(filtered_evolutions)
        return sorted_list[0] if sorted_list else None

    @classmethod
    def from_dict_to_object(cls, evol: dict):
        if isinstance(evol, dict):
            evol_date = evol.get("date")
            evol_format = evol.get("format")
            evol_availabilty = evol.get("availabilty")

            evol_price = evol.get("price")
            evol_price_without_discount = evol.get("price_without_discount")
            evol_pricePerUnit = evol.get("price_per_unit")
            evol_price_unit_without_discount = evol.get(
                "price_unit_without_discount")
            evol_price_unit_with_discount = evol.get(
                " price_unit_with_discount")
            evol_nutriscore = evol.get("nutriscore")
            evol_certification = evol.get("certification")
            evol_description = evol.get("Description")
            evol_nutrition = evol.get("nutrition")  # dict
            evol_ingredients = evol.get("ingredients")  # dict
            evol_allergens = evol.get("allergens")  # dict
            evol_customerReviews = evol.get("customerReviews")  # dict
            customerReviews = CustomerReviews.from_dict_to_object(
                evol_customerReviews)

            on_discount = evol.get("on_discount", False)

            evol = Evolution(parsing_date=evol_date, format=evol_format, availability=evol_availabilty,
                             price_per_unit=evol_pricePerUnit,
                             price=evol_price, price_without_discount=evol_price_without_discount, price_unit_with_discount=evol_price_unit_with_discount,
                             price_unit_without_discount=evol_price_unit_without_discount, nutriscore=evol_nutriscore, certification=evol_certification, nutrition=evol_nutrition,
                             ingredients=evol_ingredients, allergens=evol_allergens, reviews=customerReviews,
                             on_discount=on_discount, Description=evol_description)
            return evol

    def to_dict(self):
        # Convert the object to a dictionary and remove fields that are None
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Product:
    # _id: Optional[str] = None # for mongo and dacite interoperability
    ean: Optional[str] = None
    title: Optional[str] = None
    cdbase: Optional[str] = None
    brand: Optional[str] = None
    business_type: Optional[str] = 'food'
    categories: Optional[List[Category]] = None
    origin: Optional[Origin] = None
    matter: Optional[str] = None
    freshness: Optional[int] = None
    market: Optional[Market] = None
    lang_desc: Optional[LangDesc] = None
    evolutions: Optional[List[Evolution]] = None
    mesure_unit_for_packaging: Optional[str] = None  # g, U
    mesure_unit_for_price_per_unit: Optional[str] = None
    label: Optional[Label] = None
    created_at: Optional[str] = datetime.now().isoformat(timespec="minutes")
    updated_at: Optional[str] = datetime.now().isoformat(timespec="minutes")
    parsing_duration: Optional[int] = None

    def to_dict(self):
        # Convert the object to a dictionary and remove fields that are None
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def merge_product1_into_product2(cls, product1: Product, product2: Product) -> Product | None:
        if product1.ean is not product2.ean:
            return None
        product2.title = product1.title
        product2.cdbase = product1.cdbase
        product2.brand = product1.brand
        product2.categories = product1.categories
        product2.origin = product1.origin
        product2.matter = product1.matter
        product2.freshness = product1.freshness
        product2.market = product1.market
        product2.lang_desc = product1.lang_desc
        product2.mesure_unit_for_packaging = product1.mesure_unit_for_packaging
        product2.mesure_unit_for_price_per_unit = product1.mesure_unit_for_price_per_unit
        product2.label = product1.label
        product2.created_at = product1.created_at
        product2.updated_at = product1.updated_at
        product2.parsing_duration = product1.parsing_duration

    @classmethod
    def from_dict_to_object(cls, product: dict):
        raise NameError("fatal error, this method should be overriden")

    def toJSON(self):
        # return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return json.dumps(self,
                          default=lambda o: dict(
                              (key, value) for key, value in o.__dict__.items() if value),
                          indent=4,
                          sort_keys=True,
                          allow_nan=False,
                          ensure_ascii=False)

    def __str__(self):
        return self.toJSON()


def get_product_by_ean(ean: str | None, products: List[Product]) -> Product | None:
    if not isinstance(ean, str) or products is None or len(products) == 0:
        return None
    for product in products:
        if isinstance(product, Product):
            ean1 = product.ean
            # print("ean1: " + str(ean1))
            if ean1 == ean:
                return product
        else:
            ean1 = product.get("ean")
            # print("ean2: " + str(ean1))
            if ean1 == ean:
                return product
    return None

# get latest or the one having more products?


def get_latest_parsed_products(aisle: StaticAisle) -> Optional[List[Product]]:
    if not aisle.original_file_uri:
        return None
    (folder_path, file_name) = extract_folder_and_file(
        path=aisle.original_file_uri)
    file_name = file_name.replace(".json", "")
    # some asiles have common named such as: fruits and fruits_sec and fruits_legumes.
    # with the "_20" should fix the issue. 20 is the prefix of the year which is fine for files created
    # between 2000 and 2099.
    file_name_prefix = file_name  # + "_20"
    latest_file = get_latest_file_in_folder(
        folder_path=folder_path, file_name_prefix=file_name_prefix)
    if latest_file is None:
        return []
    # load json file
    json_file = open(latest_file, encoding='utf-8')
    latest_parsed_products: List[Product] = json.load(json_file)

    print("latest_parsed_products length: " + str(len(latest_parsed_products)) if latest_parsed_products is not None
          else "none")
    return latest_parsed_products if latest_parsed_products is not None else []

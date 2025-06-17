import datetime
import json
import random
import re
import sys
from typing import List, Optional, override
from src.model.my_model import ProductBrand

from pydantic.dataclasses import dataclass
from src.model.product import Category, CustomerReviews, Desc, Evolution, Freshness, Label, LangDesc, Market, Offer, Origin, Product
from src.countries.france.picard.model.picard_content import Nutrition, ProductContentPicard
from src.model.my_model import from_dict_to_objects

from src.utils.ean_country_checker import get_country_code_from_country_name_in_french_lang, get_country_code_from_ean
from src.utils.my_utils import find_all_substrings_in_text, is_any_string_in_string_list, is_substring_in_list
from typing import Optional, List, Dict, Any
sys.path.append('src')

ALLERGENS = [
    "Arachide", "Céleri", "Crustacés", "Crabe", "Crevette", "Écrevisse", "Homard", "Langoustine",
    "Avoine", "Blé", "Épeautre", "Kamut et leurs souches hybridées", "Orge", "Seigle",
    "Fruits à coque", "Amande", "Noisette", "Noix", "Noix du Brésil", "Noix de cajou",
    "Noix de macadamia", "Noix de pécan", "Noix du Queensland", "Pistache",
    "Lait", "Lupin", "Œuf", "Poisson", "Boulot", "Calamar", "Escargot", "Huitre",
    "Moule", "Palourde", "Pétoncle", "Pieuvre", "Moutarde", "Sésame", "Soja", "Sulfites",
    "Gluten" ]
ALLERGEN_PATTERNS = {
    "Gluten": r"\b(blé|seigle|orge|avoine|gluten|épeautre|kamut|kamut et leurs souches hybridées)\b",
    "Lait": r"\b(lait|lactose|fromage|crème|beurre|yogourt|lactosérum|caséine)\b",
    "Œuf": r"\b(œuf|oeuf|oeufs|ovoproduit|albumen)\b",
    "Poisson": r"\b(poisson|boulot|calamar|anchois|saumon|morue|thon|hareng)\b",
    "Crustacés": r"\b(crustacé|crabe|crevette|écrevisse|homard|langoustine)\b",
    "Arachide": r"\b(arachide|cacahuète|peanut)\b",
    "Soja": r"\b(soja|soya|lécithine de soja)\b",
    "Fruits à coque": r"\b(amande|noisette|noix|noix du brésil|noix de cajou|noix de macadamia|noix de pécan|noix du queensland|pistache)\b",
    "Céleri": r"\b(céleri|celeriac)\b",
    "Moutarde": r"\b(moutarde|graine de moutarde)\b",
    "Sésame": r"\b(sésame|graine de sésame|tahini)\b",
    "Sulfites": r"\b(sulfite|dioxyde de soufre|sulphite)\b",
    "Lupin": r"\b(lupin)\b",
    "Mollusques": r"\b(mollusque|moule|huître|palourde|pétoncle|pieuvre|escargot)\b"
}
@dataclass
class LabelPicard(Label):
    @classmethod
    def from_dict_to_object(cls, product: dict):
        title = product.get("title")
        details = product.get("details")  # dict
        details_halal: Optional[str] = None
        details_gmo: Optional[str] = None
        details_preservative: Optional[str] = None
        details_additive: Optional[str] = None
        details_gluten: Optional[str] = None
        details_vegan: Optional[str] = None
        details_lactose: Optional[str] = None
        if details is not None:
            details_bio = details.get("bio")
            details_vegetarian = details.get("vegetarian")
            details_halal = details.get("halal")
            details_vegan = details.get(("vegan"))
            details_lactose = details.get(("lactose"))
            details_dye = details.get("dye")
            details_gmo = details.get("gmo")
            details_fat = details.get("fat")
            details_preservative = details.get("preservative")
            details_additive = details.get("additive")
            details_sugar = details.get("sugar")
            details_frozen = details.get("frozen")
            details_gluten = details.get("gluten")
            details_fr_greengrocery = details.get("fr_greengrocery")
            details_pregnant = details.get("pregnant")
            details_fr_greengrocery = details.get("fr_greengrocery")
            details_desc = details.get("desc")

            if details_lactose is None and find_all_substrings_in_text(ProductContentPicard.LACTOSE_PRESENCE, details_desc) is not None:
                details_lactose = True
            elif details_lactose is None and find_all_substrings_in_text(ProductContentPicard.LACTOSE_ABSENCE, details_desc) is not None:
                details_lactose = False

            if details_vegan is None and find_all_substrings_in_text(ProductContentPicard.VEGAN_PRESENCE, details_desc) is not None:
                details_vegan = True

            if details_halal is None and find_all_substrings_in_text(ProductContentPicard.HALAL_PRESENCE, title) is not None:
                details_halal = True

            if details_bio is None and find_all_substrings_in_text(ProductContentPicard.BIO_PRESENCE, title) is not None:
                details_bio = True

            if details_fat is None and find_all_substrings_in_text(ProductContentPicard.FAT_ABSENCE, details_desc) is not None:
                details_fat = False

            if details_gmo is None and find_all_substrings_in_text(ProductContentPicard.GMO_ABSENCE, details_desc) is not None:
                details_gmo = False

            if details_additive is None and find_all_substrings_in_text(ProductContentPicard.ADDITIVE_ABSENCE, details_desc) is not None:
                details_additive = False

            if details_dye is None and find_all_substrings_in_text(ProductContentPicard.DYE_ABSENCE, details_desc) is not None:
                details_dye = False

            if details_preservative is None and find_all_substrings_in_text(ProductContentPicard.PRESERVATIVE_ABSENCE, details_desc) is not None:
                details_preservative = False

            if details_gluten is None and find_all_substrings_in_text(ProductContentPicard.GLUTEN_ABSENCE, details_desc) is not None:
                details_gluten = False
            elif details_gluten is None and find_all_substrings_in_text(ProductContentPicard.GLUTEN_PRESENCE, details_desc) is not None:
                details_gluten = True

            if details_sugar is None and find_all_substrings_in_text(ProductContentPicard.SUGAR_ABSENCE, details_desc) is not None:
                details_sugar = False

            return LabelPicard(bio=details_bio, frozen=details_frozen, halal=details_halal, fr_greengrocery=details_fr_greengrocery, gluten=details_gluten,
                               pregnant=details_pregnant, vegan=details_vegan, vegetarian=details_vegetarian, sugar=details_sugar, lactose=details_lactose)
        return None

class OfferPicard(Offer):
    @override
    @classmethod
    def extractInfo(cls, desc: str) -> 'OfferPicard':
        if not isinstance(desc, str):
            return None
        
        desc = desc.lower()
        required_product_quantity = None
        discount_percentage = None
        requires_loyalty_card = False
        minimum_amount = None
        promo_code = None
        offer_type = "product"
        
        # Détection des promotions globales
        if "livraison offerte" in desc:
            offer_type = "global"
            match = re.search(r'dès (\d+)', desc)
            minimum_amount = float(match.group(1)) if match else None
            code_match = re.search(r'code ([\w]+)', desc)
            promo_code = code_match.group(1) if code_match else None
        
        # Détection des promotions nécessitant une carte de fidélité
        if "carte fidélité" in desc or "avec la carte" in desc:
            requires_loyalty_card = True
        
        # Détection des promotions simples (sans quantité minimale)
        if is_any_string_in_string_list(["% d'économies", "a saisir", "promotion", "vu en catalogue", "promo :", "picard & nous"], desc):
            required_product_quantity = 1
        
        # Détection des promotions avec pourcentage
        percentage_match = re.search(r'(\d+)%', desc)
        if percentage_match:
            discount_percentage = float(percentage_match.group(1))
            if "2ème" in desc or "deuxième" in desc or "second" in desc:
                required_product_quantity = 2
            elif "réduction de" in desc:
                required_product_quantity = 1
        
        # Détection des promotions "X achetés = payez Y"
        quantity_match = re.search(r'(\d+).*pour.*(\d+)', desc) or re.search(r'(\d+).*achetés.*=\.*(\d+)', desc)
        if quantity_match:
            numbers = quantity_match.groups()
            required_product_quantity = int(numbers[0])
        
        # Détection des promotions avec "ème à"
        if "ème à" in desc:
            number_match = re.search(r'(\d+)(?:ème|eme)', desc)
            required_product_quantity = int(number_match.group(1)) if number_match else 2
        
        # Cas par défaut : si aucune quantité détectée, on suppose 1 produit
        if required_product_quantity is None and offer_type != "global":
            required_product_quantity = 1
         

        
        return OfferPicard(
            description=LangDesc(fr=Desc(desc=desc)),
            requiredProductQuantity=required_product_quantity,
            discount_percentage=discount_percentage,
            requires_loyalty_card=requires_loyalty_card,
            minimum_amount=minimum_amount,
            promo_code=promo_code,
            type=offer_type
            )

class EvolutionPicard(Evolution):
    def __init__(
        self,
        parsing_date: str,
        format: Optional[str] = None,
        weight_per_packaging: Optional[float] = None,
        price_per_packaging: Optional[float] = None,
        price_per_unit: Optional[float] = None,
        nutriscore: Optional[str] = None,
        availability: Optional[bool] = None,
        ingredients: Optional[str] = None,
        nutrition: Optional[Nutrition] = None,
        allergens: Optional[List[str]] = None,
        offers: Optional[List[dict]] = None,
        reviews: Optional[CustomerReviews] = None,
        on_discount: Optional[bool] = False,
        preparation: Optional[str] = None,  # Nouveau champ
        conservation: Optional[str] = None,  # Nouveau champ
        original_price: Optional[float] = None, 
        requires_loyalty_card: Optional[bool] = False,  # Nouveau champ pour la carte de fidélité
    ):
        super().__init__(
            parsing_date=parsing_date,
            format=format,
            weight_per_packaging=weight_per_packaging,
            price_per_packaging=price_per_packaging,
            price_per_unit=price_per_unit,
            nutriscore=nutriscore,
            availability=availability,
            ingredients=ingredients,
            nutrition=nutrition,
            allergens=allergens,
            offers=offers,
            reviews=reviews,
            on_discount=on_discount,
        )
        self.preparation = preparation
        self.conservation = conservation
        self.original_price = original_price
        self.requires_loyalty_card = requires_loyalty_card
        
        # Validation des données
        if self.original_price is not None and self.price_per_packaging is not None:
            if self.original_price < self.price_per_packaging:
                self.logger.warning(f"Validation échouée pour {self}: original_price ({self.original_price}) doit être >= price_per_packaging ({self.price_per_packaging})")
                self.original_price = self.price_per_packaging  # Correction automatique

    @override
    @classmethod
    def is_medium_equal(cls, l: 'Evolution', r: 'Evolution') -> bool | None:
        if not l or not r:
            print("is_medium_equal 1")
            return None
        if l.parsing_date == r.parsing_date:
            print("is_medium_equal 2")
            return True
        
        if not cls.is_shallow_equal(l=l, r=r):
            print("is_medium_equal 3")
            return False  
       
        if (set(l.offers or []) == set(r.offers or []) and
            l.nutriscore == r.nutriscore and l.reviews == r.reviews and
            l.original_price == r.original_price and  # Ajout de la comparaison
            l.requires_loyalty_card == r.requires_loyalty_card):  # Ajout de la comparaison
            
            print("is_medium_equal 4")
            return True
        else:
            print("is_medium_equal 5")
            return False

    @override
    @classmethod
    def from_dict_to_object(cls, evol: dict):
        if isinstance(evol, dict):
            evol_date = evol.get("parsing_date")
            evol_format = evol.get("format")
            evol_availability = evol.get("availability")
            evol_price_per_unit = evol.get("price_per_unit")
            evol_price = evol.get("price_per_packaging")
            evol_nutriscore = evol.get("nutriscore")
            evol_certification = evol.get("certification")
            evol_nutrition = evol.get("nutrition")  # dict
            evol_nutrition = Nutrition.convert_dict_to_nutrition_Object(nutritions=evol_nutrition) if evol_nutrition else None
            evol_ingredients = evol.get("ingredients")  # str
            evol_allergens = evol.get("allergens")  # List[str]
            evol_customer_reviews = evol.get("reviews")  # dict
            evol_customer_reviews = CustomerReviews.from_dict_to_object(evol_customer_reviews) if evol_customer_reviews else None
            evol_on_discount = evol.get("on_discount", False)
            evol_preparation = evol.get("preparation")  # Nouveau champ
            evol_conservation = evol.get("conservation")  # Nouveau champ
            evol_original_price = evol.get("original_price")  # Nouveau champ
            evol_requires_loyalty_card = evol.get("requires_loyalty_card", False)  # Nouveau champ

            return EvolutionPicard(
                parsing_date=evol_date,
                format=evol_format,
                availability=evol_availability,
                price_per_unit=evol_price_per_unit,
                price_per_packaging=evol_price,
                nutriscore=evol_nutriscore,
                certification=evol_certification,
                nutrition=evol_nutrition,
                ingredients=evol_ingredients,
                allergens=evol_allergens,
                reviews=evol_customer_reviews,
                on_discount=evol_on_discount,
                preparation=evol_preparation,
                conservation=evol_conservation,
                original_price=evol_original_price,
                requires_loyalty_card=evol_requires_loyalty_card,
            )
        return None

class MarketPicard(Market):
    @classmethod
    @override
    def from_dict_to_object(cls, product: dict):
        market_name = product.get("market") or "picard"
        market_address = product.get("address") or "market Paris Alésia"
        market_country = product.get("market_country") or "FR"
        return MarketPicard(name=market_name, country=market_country, address=market_address)

    @override
    def __init__(self, name="picard", country="FR"):
        super().__init__(name="picard", country="FR")
        self.name = name
        
        self.country = country

class ProductPicard(Product):
    def __init__(self, ean, business_type, lang_desc, evolutions, offers=None, market=None, origin=None, unit_of_measure=None, freshness=None, created_at=None, updated_at=None, categories=None, label=None, customer_reviews=None, brand: Optional[ProductBrand] = None):
        
        super().__init__(
            ean=ean,
            business_type=business_type,
            lang_desc=lang_desc,
            evolutions=evolutions,
            origin=origin,
            unit_of_measure=unit_of_measure,
            freshness=freshness,
            created_at=created_at,
            updated_at=updated_at,
            market=market,
            categories=categories,
            label=label
        )
        self.brand = brand
        self.offers = offers
        self.customer_reviews = customer_reviews
      
        
    @override
    @classmethod
    def from_dict_to_object(cls, product: dict) -> 'ProductPicard':
        ean = product.get("ean")
        business_type = product.get("business_type")

        origin = Origin(
            ean=get_country_code_from_ean(ean=ean),
            explicit=get_country_code_from_country_name_in_french_lang(product.get("origin")),
            partial=product.get("partial_origin")
        )

        unit_of_measure = product.get("unit_of_measure")
        freshness = Freshness(value=product.get("freshness_value"), period=product.get("freshness_period"))
        freshness = freshness.get_freshness_days_from_object()

        created_at = product.get("created_at")
        updated_at = product.get("updated_at")

        market = MarketPicard(
            name=product.get("market"),
            country=product.get("market_country"),
            address=product.get("market_address")
        )

        categories = product.get("categories")  # list
        categories: list[Category] = from_dict_to_objects(Category, categories)

        lang_desc = product.get("lang_desc")  # dict
        lang_desc = LangDesc.from_dict_to_object(lang_desc=lang_desc)
        

        label = LabelPicard.from_dict_to_object(product=product)

        evolutions = product.get("evolutions")  # list
        evolutions = from_dict_to_objects(EvolutionPicard, evolutions)
        
        offers = product.get("offers")  # list
        offers = from_dict_to_objects(OfferPicard, offers) if offers else None
        
        customer_reviews = product.get("customer_reviews")
        
        brand_dict = product.get("brand")
        brand = ProductBrand(name=brand_dict["name"], brand_id=brand_dict["brand_id"]) if brand_dict else None
        return ProductPicard(
            ean=ean,
            brand=brand,
            business_type=business_type,
            origin=origin,
            unit_of_measure=unit_of_measure,
            freshness=freshness,
            created_at=created_at,
            updated_at=updated_at,
            market=market,
            categories=categories,
            lang_desc=lang_desc,
            evolutions=evolutions,
            label=label,
            offers=offers,
            customer_reviews=customer_reviews
        )
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["brand"] = self.brand.to_dict() if self.brand else None
        result["offers"] = [offer.to_dict() for offer in self.offers] if self.offers else None
        result["customer_reviews"] = self.customer_reviews
        return result
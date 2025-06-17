import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any
from pymongo import MongoClient
from fuzzywuzzy import fuzz
import logging
from dotenv import load_dotenv
from dateutil.parser import parse  # Ajout pour gérer les dates non standards
import os
load_dotenv()
mongo_uri = os.getenv('MONGO_URI')

# Configurer le logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Étape 1 : Charger les fichiers JSON avec chemins absolus
def load_json_files(folder: str) -> List[Dict[str, Any]]:
    products = []
    folder_path = os.path.abspath(folder)
    if not os.path.exists(folder_path):
        logger.error(f"Le dossier {folder_path} n'existe pas.")
        return products
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            filepath = os.path.join(folder_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        products.extend(data)
                    else:
                        products.append(data)
                logger.info(f"Chargé {filename} avec {len(data)} produits")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de {filename} : {e}")
    return products

# Étape 2 : Nettoyer les données
def clean_data(products: List[Dict[str, Any]], source: str) -> List[Dict[str, Any]]:
    cleaned_products = []
    for product in products:
        try:
            cleaned_product = product.copy()

            # Initialiser les structures par défaut
            if 'evolutions' not in cleaned_product or not isinstance(cleaned_product['evolutions'], list):
                cleaned_product['evolutions'] = [{}]
            if 'lang_desc' not in cleaned_product:
                cleaned_product['lang_desc'] = {'fr': {'title': '', 'desc': '', 'images': [], 'links': None}}
            if 'brand' not in cleaned_product:
                cleaned_product['brand'] = {'name': 'Unknown'}
            if 'evolutions' in cleaned_product and not cleaned_product['evolutions']:
                cleaned_product['evolutions'] = [{}]

            # Normalisation des prix
            price = cleaned_product['evolutions'][0].get('price_per_packaging')
            if price:
                try:
                    cleaned_product['evolutions'][0]['price_per_packaging'] = float(price)
                    if cleaned_product['evolutions'][0]['price_per_packaging'] < 0:
                        cleaned_product['evolutions'][0]['price_per_packaging'] = None
                except (ValueError, TypeError):
                    cleaned_product['evolutions'][0]['price_per_packaging'] = None
            else:
                cleaned_product['evolutions'][0]['price_per_packaging'] = None

            # Normalisation de price_per_unit (spécifique à Naturalia)
            price_per_unit = cleaned_product['evolutions'][0].get('price_per_unit')
            if price_per_unit:
                try:
                    cleaned_product['evolutions'][0]['price_per_unit'] = float(price_per_unit)
                    if cleaned_product['evolutions'][0]['price_per_unit'] < 0:
                        cleaned_product['evolutions'][0]['price_per_unit'] = None
                except (ValueError, TypeError):
                    cleaned_product['evolutions'][0]['price_per_unit'] = None
            else:
                cleaned_product['evolutions'][0]['price_per_unit'] = None

            # Normalisation des unités de mesure (poids)
            weight = cleaned_product['evolutions'][0].get('weight_per_packaging')
            unit = cleaned_product['evolutions'][0].get('unit_of_measure', 'g')
            if weight:
                try:
                    weight = float(weight)
                    if unit.lower() in ['kg', 'kilogram', 'l', 'litre']:
                        weight *= 1000
                        unit = 'g' if unit.lower() in ['kg', 'kilogram'] else 'ml'
                    elif unit.lower() in ['mg', 'milligram']:
                        weight /= 1000
                        unit = 'g'
                    cleaned_product['evolutions'][0]['weight_per_packaging'] = weight
                    cleaned_product['evolutions'][0]['unit_of_measure'] = unit
                except (ValueError, TypeError):
                    cleaned_product['evolutions'][0]['weight_per_packaging'] = None
                    cleaned_product['evolutions'][0]['unit_of_measure'] = None
            else:
                cleaned_product['evolutions'][0]['weight_per_packaging'] = None
                cleaned_product['evolutions'][0]['unit_of_measure'] = None

            # Normalisation des dates
            parsing_date = cleaned_product['evolutions'][0].get('parsing_date')
            if parsing_date:
                try:
                    cleaned_product['evolutions'][0]['parsing_date'] = parse(parsing_date).isoformat()
                except ValueError:
                    cleaned_product['evolutions'][0]['parsing_date'] = datetime.now().isoformat()
            else:
                cleaned_product['evolutions'][0]['parsing_date'] = datetime.now().isoformat()

            # Normalisation des dates created_at et updated_at
            for field in ['created_at', 'updated_at']:
                if cleaned_product.get(field):
                    try:
                        cleaned_product[field] = parse(cleaned_product[field]).isoformat()
                    except ValueError:
                        cleaned_product[field] = datetime.now().isoformat()
                else:
                    cleaned_product[field] = datetime.now().isoformat()

            # Normalisation des textes
            cleaned_product['lang_desc']['fr']['title'] = str(cleaned_product['lang_desc']['fr'].get('title', '')).strip()
            cleaned_product['lang_desc']['fr']['desc'] = str(cleaned_product['lang_desc']['fr'].get('desc', '')).strip()
            cleaned_product['brand']['name'] = str(cleaned_product['brand'].get('name', 'Unknown')).strip()

            # Nettoyage des ingrédients
            ingredients = cleaned_product['evolutions'][0].get('ingredients')
            desc = cleaned_product['lang_desc']['fr'].get('desc', '')
            if isinstance(ingredients, str) and ingredients.strip() == desc.strip():
                logger.warning(f"Ingredients semble être une description pour {cleaned_product.get('ean', 'inconnu')} de {source}")
                cleaned_product['evolutions'][0]['ingredients'] = []
            else:
                cleaned_product['evolutions'][0]['ingredients'] = ingredients if isinstance(ingredients, list) else []

            # Gestion des champs manquants ou spécifiques
            cleaned_product['ean'] = cleaned_product.get('ean') or None
            if not cleaned_product['ean'] or not cleaned_product['ean'].isdigit():
                logger.warning(f"EAN non standard détecté : {cleaned_product['ean']} pour {source}")
            cleaned_product['lang_desc']['fr']['images'] = cleaned_product['lang_desc']['fr'].get('images') or []
            cleaned_product['lang_desc']['fr']['links'] = cleaned_product['lang_desc']['fr'].get('links', {}).get('links_self') or None
            cleaned_product['evolutions'][0]['nutrition'] = cleaned_product['evolutions'][0].get('nutrition') or {}
            cleaned_product['evolutions'][0]['allergens'] = cleaned_product['evolutions'][0].get('allergens') or []
            cleaned_product['evolutions'][0]['nutriscore'] = cleaned_product['evolutions'][0].get('nutriscore') or None
            cleaned_product['evolutions'][0]['preparation'] = cleaned_product['evolutions'][0].get('preparation') or None
            cleaned_product['evolutions'][0]['conservation'] = cleaned_product['evolutions'][0].get('conservation') or None
            cleaned_product['evolutions'][0]['format'] = cleaned_product['evolutions'][0].get('format') or None
            cleaned_product['evolutions'][0]['availability'] = cleaned_product['evolutions'][0].get('availability') or None
            cleaned_product['evolutions'][0]['requires_loyalty_card'] = cleaned_product['evolutions'][0].get('requires_loyalty_card') or False
            cleaned_product['evolutions'][0]['is_organic'] = cleaned_product['evolutions'][0].get('is_organic') or False
            cleaned_product['evolutions'][0]['is_vegan'] = cleaned_product['evolutions'][0].get('is_vegan') or False
            cleaned_product['business_type'] = cleaned_product.get('business_type') or None
            cleaned_product['market'] = cleaned_product.get('market') or {'name': source.lower(), 'country': 'FR', 'address': None}
            cleaned_product['customer_reviews'] = cleaned_product.get('customer_reviews') or None
            cleaned_product['origin'] = cleaned_product.get('origin') or {"explicit": None, "partial": None}

            # Normalisation des catégories
            if 'categories' in cleaned_product:
                if isinstance(cleaned_product['categories'], list):
                    cleaned_product['categories'] = cleaned_product['categories']
                elif isinstance(cleaned_product['categories'], dict):
                    cleaned_product['categories'] = [cleaned_product['categories']]
                else:
                    cleaned_product['categories'] = []
            else:
                cleaned_product['categories'] = []

            # Normalisation des offres
            cleaned_product['offers'] = cleaned_product['evolutions'][0].get('offers') or []
            if source == 'Picard' and cleaned_product['evolutions'][0].get('on_discount'):
                cleaned_product['offers'].append({'discount': 'On discount'})

            # Normalisation des nutrition_values
            nutrition = cleaned_product['evolutions'][0]['nutrition']
            if nutrition:
                for category, values in nutrition.items():
                    if isinstance(values, dict):
                        for key, value in values.items():
                            if isinstance(value, str):
                                try:
                                    num = re.search(r'[\d,.]+', value)
                                    values[key] = float(num.group().replace(',', '.')) if num else None
                                except:
                                    values[key] = None

            # Ajouter la source
            cleaned_product['source'] = source

            cleaned_products.append(cleaned_product)
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage du produit {product.get('ean', 'inconnu')} de {source} : {e}")
    
    return cleaned_products

# Étape 3 : Fusionner les données
def merge_data(naturalia_products: List[Dict[str, Any]], picard_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged_products = []
    seen_products = {}

    all_products = naturalia_products + picard_products
    for product in all_products:
        product_key = product.get('ean')
        if not product_key or not product_key.isdigit():
            product_key = (
                product.get('lang_desc', {}).get('fr', {}).get('title', '').lower().strip(),
                product.get('brand', {}).get('name', '').lower().strip()
            )

        matched_key = None
        if isinstance(product_key, tuple):
            for key in seen_products:
                if isinstance(key, tuple):
                    if (
                        fuzz.ratio(product_key[0], key[0]) > 90
                        and fuzz.ratio(product_key[1], key[1]) > 90
                    ):
                        matched_key = key
                        break
        else:
            matched_key = product_key if product_key in seen_products else None

        if matched_key:
            existing = seen_products[matched_key]
            new_price = product.get('evolutions', [{}])[0].get('price_per_packaging')
            existing_price = existing.get('evolutions', [{}])[0].get('price_per_packaging')
            if new_price and existing_price:
                existing['evolutions'][0]['price_per_packaging'] = min(new_price, existing_price)
            elif new_price:
                existing['evolutions'][0]['price_per_packaging'] = new_price

            new_price_unit = product.get('evolutions', [{}])[0].get('price_per_unit')
            existing_price_unit = existing.get('evolutions', [{}])[0].get('price_per_unit')
            if new_price_unit and existing_price_unit:
                existing['evolutions'][0]['price_per_unit'] = min(new_price_unit, existing_price_unit)
            elif new_price_unit:
                existing['evolutions'][0]['price_per_unit'] = new_price_unit

            existing['source'] = list(set(existing.get('source', []) + [product['source']]))

            existing['evolutions'][0]['ingredients'] = list(set(
                existing.get('evolutions', [{}])[0].get('ingredients', []) +
                product.get('evolutions', [{}])[0].get('ingredients', [])
            ))
            existing['evolutions'][0]['allergens'] = list(set(
                existing.get('evolutions', [{}])[0].get('allergens', []) +
                product.get('evolutions', [{}])[0].get('allergens', [])
            ))

            # Fusionner les offres (simplifié sans json.dumps)
            existing_offers = existing.get('offers', [])
            new_offers = product.get('offers', [])
            existing['offers'] = existing_offers + [o for o in new_offers if o not in existing_offers]

            for field in ['nutriscore', 'preparation', 'conservation', 'format', 'availability', 'requires_loyalty_card', 'is_organic', 'is_vegan']:
                existing_val = existing['evolutions'][0].get(field)
                new_val = product['evolutions'][0].get(field)
                if new_val and not existing_val:
                    existing['evolutions'][0][field] = new_val

            for field in ['business_type', 'market', 'customer_reviews', 'created_at', 'updated_at', 'origin']:
                existing_val = existing.get(field)
                new_val = product.get(field)
                if new_val and not existing_val:
                    existing[field] = new_val
        else:
            seen_products[product_key] = product
            merged_products.append(product)

    return merged_products

# Étape 4 : Structurer pour MongoDB
def structure_for_mongodb(products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    structured_products = []
    for product in products:
        try:
            category = None
            if product.get('categories'):
                if isinstance(product['categories'], list) and product['categories']:
                    category = product['categories'][0].get('label')
                elif isinstance(product['categories'], dict):
                    category = product['categories'].get('label')

            structured_product = {
                'brand': {
                    'name': product.get('brand', {}).get('name', 'Unknown'),
                    'description': None,
                    'logo': None,
                    'category': category
                },
                'product': {
                    'name': product.get('lang_desc', {}).get('fr', {}).get('title', ''),
                    'image': product.get('lang_desc', {}).get('fr', {}).get('images', [None])[0],
                    'category': category,
                    'price': product.get('evolutions', [{}])[0].get('price_per_packaging', None),
                    'price_per_unit': product.get('evolutions', [{}])[0].get('price_per_unit', None),
                    'title': product.get('lang_desc', {}).get('fr', {}).get('title', ''),
                    'description': product.get('lang_desc', {}).get('fr', {}).get('desc', ''),
                    'ingredients': product.get('evolutions', [{}])[0].get('ingredients', []),
                    'nutrition_values': product.get('evolutions', [{}])[0].get('nutrition', {}),
                    'instructions': product.get('evolutions', [{}])[0].get('preparation', None),
                    'conservation': product.get('evolutions', [{}])[0].get('conservation', None),
                    'weight': product.get('evolutions', [{}])[0].get('weight_per_packaging', None),
                    'weight_unit': product.get('evolutions', [{}])[0].get('unit_of_measure', None),
                    'ean': product.get('ean', None),
                    'nutriscore': product.get('evolutions', [{}])[0].get('nutriscore', None),
                    'allergens': product.get('evolutions', [{}])[0].get('allergens', []),
                    'origin': product.get('origin', {}).get('explicit', None),
                    'format': product.get('evolutions', [{}])[0].get('format', None),
                    'availability': product.get('evolutions', [{}])[0].get('availability', None),
                    'requires_loyalty_card': product.get('evolutions', [{}])[0].get('requires_loyalty_card', False),
                    'is_organic': product.get('evolutions', [{}])[0].get('is_organic', False),
                    'is_vegan': product.get('evolutions', [{}])[0].get('is_vegan', False)
                },
                'offers': product.get('offers', []),
                'customer_reviews': product.get('customer_reviews', None),
                'business_type': product.get('business_type', None),
                'market': product.get('market', {'name': product.get('source', '').lower(), 'country': 'FR', 'address': None}),
                'created_at': product.get('created_at', datetime.now().isoformat()),
                'updated_at': product.get('updated_at', datetime.now().isoformat()),
                'last_updated': datetime.now().isoformat()
            }
            structured_products.append(structured_product)
        except Exception as e:
            logger.error(f"Erreur lors de la structuration du produit {product.get('ean', 'inconnu')} : {e}")
    return structured_products

# Étape 5 : Insérer dans MongoDB
def insert_into_mongodb(products: List[Dict[str, Any]]) -> None:
    
    try:
        mongo = os.getenv('MONGO_URI')
        # Utiliser des variables d'environnement pour les identifiants
        mongo_uri = os.getenv('MONGO_URI', mongo)
        client = MongoClient(mongo_uri)
        db = client['DB_Produits_Alimentaires']  # Corrigé pour correspondre à ton message précédent
        collection = db['products']

        # Valider les données avant insertion
        for product in products:
            if not product.get('product', {}).get('ean') or not product.get('product', {}).get('title'):
                logger.warning(f"Produit manquant ean ou titre : {product.get('product', {}).get('ean', 'inconnu')}")
            if not product.get('product', {}).get('ingredients'):
                logger.warning(f"Ingredients vides pour {product.get('product', {}).get('ean', 'inconnu')}")

        # Insérer ou mettre à jour avec upsert
        for product in products:
            if product.get('product', {}).get('ean') and product['product']['ean'].isdigit():
                collection.update_one(
                    {'ean': product['product']['ean']},
                    {'$set': product},
                    upsert=True
                )
            else:
                # Insérer sans index unique pour les EAN non standards
                collection.insert_one(product)
        logger.info(f"Traitement de {len(products)} produits dans MongoDB terminé")

        # Créer des index (sauf unique sur ean si non standard)
        collection.create_index([('product.name', 'text'), ('brand.name', 'text')])
        collection.create_index([('source', 1)])
    except Exception as e:
        logger.error(f"Erreur lors de l'insertion dans MongoDB : {e}")
    finally:
        client.close()

# Exécuter le pipeline
if __name__ == "__main__":
    # Charger les données avec chemins absolus
    folder = r"C:\Users\amine\Desktop\Selinium-Scraping-NLP-ML\products"
   
    products = load_json_files(folder)
    logger.info(f"Chargé {len(products)} produits")

    # Nettoyer
    cleaned= clean_data(products, 'Picard')
    logger.info(f"Nettoyé {len(cleaned)} produits ")

    

    # Structurer
    structured_products = structure_for_mongodb(cleaned)

    # Sauvegarder en JSON
    output_path = os.path.join(os.path.dirname(__file__), 'merged_cleaned_products.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(structured_products, f, ensure_ascii=False, indent=4)
    logger.info(f"Données nettoyées sauvegardées dans {output_path}")

    # Insérer dans MongoDB
    insert_into_mongodb(structured_products)
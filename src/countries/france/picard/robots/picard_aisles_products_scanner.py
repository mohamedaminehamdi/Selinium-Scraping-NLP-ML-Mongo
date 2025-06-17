import json
import logging
import os
import re
import sys
import time
from typing import List, Optional
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from unidecode import unidecode
from selenium.webdriver.common.action_chains import ActionChains
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from src.model.my_model import ProductBrand
from src.countries.france.picard.model.product_picard import EvolutionPicard, MarketPicard, OfferPicard, ProductPicard
from src.countries.france.picard.model.picard_content import NutritionPicard, ProductContentPicard
from src.countries.france.picard.robots import picard_static_aisles,webdriverInstance

from src.model.static_category_aisle import StaticAisle
from src.countries.france.picard.model.product_picard import ALLERGENS, ALLERGEN_PATTERNS

from src.utils.my_utils import dump_json_then_write_it_to_file

from src.model.product import (
    CustomerReviews,
    Desc,
    Evolution,
    LangDesc,
    Links,
    Nutrition,
    Offer,
    Product,
    Category,
    get_product_by_ean,
    Origin
)


class PicardAislesProductsScanner:
    def __init__(self):
        self.total_products_number = 0
        self.first_access = True
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
       
    def handle_cookies(self, driver):
        """Rejet des cookies"""
        try:
            close_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "onetrust-close-btn-handler"))
            )
            close_btn.click()
            self.logger.info("Bouton 'Continuer sans accepter' cliqué.")
        except TimeoutException:
            self.logger.info("Panneau de cookies non trouvé ou déjà fermé")

    def scroll_to_bottom(self, driver, max_products_to_load: Optional[int] = None):
        """Défilement pour charger tous les produits sur une page"""
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_attempts = 15

        while scroll_attempts < max_attempts:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(driver, 5).until(
                    lambda d: d.execute_script("return document.body.scrollHeight") > last_height
                )
            except TimeoutException:
                break
            
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts += 1
            if max_products_to_load:
                current_products = len(driver.find_elements(By.CSS_SELECTOR, 'ul#search-result-items > li[class*="ProductGrid-item"]'))
                if current_products >= max_products_to_load:
                    break
        self.logger.info(f"Défilement terminé après {scroll_attempts} tentatives")

   
    def normalize_text(self, text):
        text = unidecode(text)
        return text.lower()
    
    def extract_product_id(self, url: str) -> Optional[str]:
        """Extraction de l'ID produit depuis l'URL"""
        if not url:
            return None
        try:
            parts = url.split('-')
            if parts:
                return parts[-1].split('.')[0]
            return None
        except Exception as e:
            self.logger.warning(f"Erreur d'extraction de l'ID depuis l'URL {url}: {str(e)}")
            return None
        
   

    def extract_global_offers(self, driver):
        global_offers = []
        try:
            banner_elements = driver.find_elements(By.CSS_SELECTOR, '[class*="banner"], [class*="promo"]')
            
            for banner in banner_elements:
                if banner.is_displayed():
                    banner_text = banner.text.strip().lower()
                    if banner_text and not banner_text.isspace() and len(banner_text) > 1:  # Filtre les textes vides ou trop courts
                        self.logger.info(f"Bannière trouvée: {banner_text}")
                    offer = {
                        "description": {"fr": {"desc": banner_text}}}
                    
                    #Détection des pourcentages
                    percentage_match = re.search(r'-(\d+\.?\d*)%|\b(\d+\.?\d*) ?%', banner_text)
                    if percentage_match:
                        percentage = float(percentage_match.group(1) or percentage_match.group(2))
                        offer["discount_percentage"] = percentage
                        code_match = re.search(r'code ([\w]+)', banner_text)
                        offer["promo_code"] = code_match.group(1) if code_match else None
                    
                    global_offers.append(offer)
                    self.logger.info(f"Offre globale ajoutée: {banner_text}")
            if not global_offers:
                self.logger.info("Aucune bannière de promotion trouvée sur la page")
            return global_offers
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'extraction des bannières: {str(e)}")
            return []


    def parse_products(self, driver: webdriver, aisle: StaticAisle, parse_only_ean_title_url_price: bool, parse_only_first_x_products: Optional[int] = None, parse_only_from_index: Optional[int] = None, latest_parsed_products: List[ProductPicard] = [], max_products: Optional[int] = None) -> List[Product]:
        aisle_url = f"{aisle.url}?sz=100"
        products = []
        nb_parsed_results = 0
        parsed_eans = set()
        self.logger.info(f"Début du parsing du rayon: {aisle.name} | URL: {aisle_url}")
        driver.get(aisle_url)

        if self.first_access:
            self.handle_cookies(driver)
            self.first_access = False
         
        # Détection du nombre total de pages
        try:
            page_links = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.pi-Pagination-listItem .pi-Pagination-link'))
            )
            page_numbers = [int(link.text.strip()) for link in page_links if link.text.strip().isdigit()]
            total_pages = max(page_numbers) if page_numbers else 1
            self.logger.info(f"Nombre total de pages: {total_pages}")
        except (TimeoutException, ValueError, IndexError):
            self.logger.warning("Nombre total de pages non trouvé, supposition d'une seule page")
            total_pages = 1

        current_page = 1
        max_products = parse_only_first_x_products or max_products or float('inf')
        while current_page <= total_pages and nb_parsed_results < max_products:
            self.logger.info(f"Traitement de la page {current_page}/{total_pages}")
           
            self.scroll_to_bottom(driver, max_products)
            
            #Extraire les offres globales
            global_offers = []
            try:
                global_offers = self.extract_global_offers(driver)
                self.logger.info(f"Offres globales extraites: {global_offers}")
            except Exception as e:
                self.logger.warning(f"Erreur lors de l'extraction des offres globales: {str(e)}")


            # Collecte des données des produits
            product_data = []
            products_els = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul#search-result-items > li[class*='ProductGrid-item']"))
            )
            self.logger.info(f"Nombre d'éléments produits trouvés sur la page {current_page}: {len(products_els)}")
            start_index = parse_only_from_index or 0
            for i, el in enumerate(products_els[start_index:start_index + max_products - nb_parsed_results]):
                try:
                    product_url_el = WebDriverWait(el, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.pi-ProductCard-link'))
                    )
                    self.logger.info(f"Traitement du produit à l'index {i}")
                    product_url_el =  el.find_element(By.CSS_SELECTOR, 'a.pi-ProductCard-link')
                    self.logger.info(f"URL du produit trouvée à l'index {i}")
                    product_url = product_url_el.get_attribute('href')
                    self.logger.info(f"URL extraite: {product_url}")
                    product_id = self.extract_product_id(product_url)
                    self.logger.info(f"ID du produit: {product_id}")
                    product_title = el.find_element(By.CSS_SELECTOR, 'h3.pi-ProductCard-name').text.strip()
                    self.logger.info(f"Titre du produit: {product_title}")
                    # Extraction de la marque depuis le titre
                    brand = ProductBrand(name="Picard", brand_id=None) 
                    if parse_only_ean_title_url_price:
                        try:
                            excluded_words = {
                                'jambon', 'filets', 'poulet', 'crêpes', 'poêlée', 'sarlandaise', 'sarladaises', 'pommes',
                                'terre', 'nems', 'baozis', 'perles', 'bouchées', 'brochettes', 'dim', 'sum', 'de', 'au',
                                'aux', 'avec', 'et', 'sauce', 'fromage', 'emmental', 'porc', 'coco', 'nuoc-mâm', 'saté',
                                'canard', 'persil', 'ail', 'huile', 'tournesol', 'prefrites', 'cuisinées', 'la', 'le',
                                'végétal', 'légumes', 'riz', 'pâte', 'galette', 'fourrées'
                            }
                            valid_brands = set(ProductBrand.getAllKnownBrands() + [
                                "Picard", "Cuisine Evasion", "Picard Gourmet", "Picard Bio",
                                "Sélection Picard", "Collection Picard"
                            ])
                            brand_match = re.search(
                                r'marque\s*:\s*([^\n]+)|(?:\b(Picard|Cuisine Evasion|[A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\b)',
                                product_title,
                                re.IGNORECASE
                            )
                            if brand_match:
                                potential_brand = brand_match.group(1) or brand_match.group(2)
                                if (potential_brand.lower() not in excluded_words and
                                        potential_brand.lower() in [b.lower() for b in valid_brands]):
                                    brand = ProductBrand(name=potential_brand, brand_id=None)
                                    self.logger.info(f"Marque extraite pour {product_id} depuis le titre: {brand}")
                                else:
                                    self.logger.info(f"Marque potentielle '{potential_brand}' exclue (mot non valide), utilisation de 'Picard' par défaut pour {product_id}")
                            else:
                                self.logger.info(f"Aucune marque trouvée dans le titre pour {product_id}, utilisation de 'Picard' par défaut")
                        except Exception as e:
                            self.logger.info(f"Erreur lors de l'extraction de la marque pour {product_id}, utilisation de 'Picard' par défaut: {e}")
                  
                    #Extraction du prix réduit et du prix initial
                    price = None
                    original_price = None
                    requires_loyalty_card = False
                    try:
                        price_el = el.find_element(By.CSS_SELECTOR, '.pi-ProductCardPrice-salesPrice:not(.pi-ProductOffer-pricee85a08)')
                        price_text = price_el.get_attribute('innerText').strip().replace('Prix soldé', '').replace('\n', '').replace('€', '').replace(',', '.').strip()
                        price = float(price_text)
                        self.logger.debug(f"Prix standard trouvé pour {product_id}: {price} €")
                    except NoSuchElementException:
                        self.logger.debug(f"Aucun prix standard trouvé pour {product_id}")
                        
                        
                    try:
                        fidelity_price_el = el.find_element(By.CSS_SELECTOR, '.pi-ProductCardPrice-salesPrice.pi-ProductOffer-pricee85a08')
                        fidelity_price_text = fidelity_price_el.get_attribute('innerText').strip().replace('Prix soldé carte fidélité', '').replace('\n', '').replace('€', '').replace(',', '.').strip()
                        original_price = price or float(fidelity_price_text) 
                        price = float(fidelity_price_text)
                        requires_loyalty_card = True
                        self.logger.debug(f"Prix fidélité trouvé pour {product_id}: {price} €") 
                    except NoSuchElementException:
                        self.logger.debug(f"Aucun prix fidélité trouvé pour {product_id}")
                        
                    # Extraction des promotions 
                    offers = []
                    seen_offers = set()  # Pour éviter les doublons
                    try:
                        offer_els = el.find_elements(By.CSS_SELECTOR, '.pi-ProductCardTag-title, [class*="promo"]')
                        for offer_el in offer_els:
                            if offer_el.is_displayed():
                                offer_text = offer_el.text.strip()
                                if offer_text and not offer_text.isspace() and len(offer_text) > 1:  # Vérifie que le texte est non vide, non espace, et a une longueur suffisante
                                    self.logger.debug(f"Promotion trouvée pour {product_id} dans la liste: {offer_text}")
                                if f"{product_id}:{offer_text}" not in seen_offers:
                                    offer = {
                                        "description": {"fr": {"desc": offer_text}},
                                        "requiredProductQuantity": 1
                                    }
                                    #detection des pourcentages génériques
                                    percentage_match = re.search(r'-(\d+\.?\d*)%|\b(\d+\.?\d*) ?%', offer_text)
                                    if percentage_match:
                                        percentage = float(percentage_match.group(1) or percentage_match.group(2))
                                        offer["discount_percentage"] = percentage
                                        if "carte" in offer_text:
                                            offer["requires_loyalty_card"] = True
                                            requires_loyalty_card = True
                                            offer["description"]["fr"]["desc"] = f"-{percentage}% avec la carte fidélité"
                                        else:
                                            offer["description"]["fr"]["desc"] = f"-{percentage}%"
                                   
                                   
                                    #détection des réductions fixes
                                    fixed_discount_match = re.search(r'-(\d+\.?\d*)€', offer_text)
                                    if fixed_discount_match:
                                        discount_value = float(fixed_discount_match.group(1).replace(',', '.'))
                                        offer["discount_value"] = discount_value
                                        offer["discount_type"] = "fixed_amount"
                                        if "carte" in offer_text:
                                            offer["requires_loyalty_card"] = True
                                            requires_loyalty_card = True
                                            offer["description"]["fr"]["desc"] = f"-{discount_value}€ avec la carte fidélité"
                                    
                                    #detection des offres sur le 2éme produit
                                    elif re.search(r'(\d+)%.*(2ème|deuxième|second)', offer_text):
                                        percentage = float(re.search(r'(\d+)%', offer_text).group(1))
                                        offer["description"]["fr"]["desc"] = f"-{percentage}% sur le 2ème produit"
                                        offer["discount_percentage"] = percentage
                                        offer["requiredProductQuantity"] = 2
                                    
                                    # Détection des offres "X pour Y"
                                    elif re.search(r'(\d+).*pour.*(\d+)', offer_text):
                                        numbers = re.findall(r'\d+', offer_text)
                                        if len(numbers) >= 2 and int(numbers[0]) >= int(numbers[1]):
                                            offer["description"]["fr"]["desc"] = f"{numbers[0]} achetés = payez {numbers[1]}"
                                            offer["requiredProductQuantity"] = int(numbers[0])
                                        else:
                                            self.logger.warning(f"Offre 'X pour Y' invalide pour {product_id}: {offer_text}")
                                    else:
                                        # Offre générique si aucune condition spécifique
                                        offer["description"]["fr"]["desc"] = offer_text
                                    
                                    offers.append(offer)
                                    seen_offers.add(f"{product_id}:{offer_text}")
                                    self.logger.info(f"Offre ajoutée pour {product_id}: {offer_text}")

                                            
                                    # Extraire la période de validité
                                    try:
                                        parent_tag = WebDriverWait(offer_el, 5).until(
                                            EC.presence_of_element_located(
                                                (By.XPATH, './ancestor::div[contains(@class, "pi-ProductCardTag")]')
                                            )
                                        )
                                        overlay_button = parent_tag.find_element(By.CSS_SELECTOR, '.pi-ProductCardTag-overlayArrow')
                                        driver.execute_script("arguments[0].scrollIntoView(true);", overlay_button)
                                        driver.execute_script("arguments[0].click();", overlay_button)
                                        WebDriverWait(driver, 3).until(
                                            EC.visibility_of_element_located((By.CSS_SELECTOR, '.pi-ProductCardTag-overlay'))
                                        )
                                        
                                        overlay_el = parent_tag.find_element(By.CSS_SELECTOR, '.pi-ProductCardTag-overlay')
                                        if overlay_el.is_displayed():
                                            overlay_text = overlay_el.text.strip()
                                            offer["validity"] = overlay_text
                                            self.logger.debug(f"Période de validité trouvée pour {product_id}: {overlay_text}")
                                        else:
                                            self.logger.debug(f"Overlay non visible pour {product_id}")
                                    
                                    except NoSuchElementException:
                                        self.logger.debug(f"Aucune période de validité trouvée pour {product_id}")
                                   
                     
                        if not offers:
                            self.logger.info(f"Aucune promotion trouvée pour {product_id} dans la liste du rayon {aisle.name}")

                    except NoSuchElementException:
                        self.logger.info(f"Aucune promotion trouvée pour {product_id} dans la liste du rayon {aisle.name}")

                    # Ajouter une offre si un prix réduit est détecté
                    if original_price and price and original_price > price:      
                        discount_percentage = round(((original_price - price) / original_price) * 100, 2)
                        existing_offer = next((o for o in offers if "carte" in o["description"]["fr"]["desc"].lower() and abs(o.get("discount_percentage", 0) - discount_percentage) < 1), None)
                        if not existing_offer:
                            offer_text = f"Réduction de {discount_percentage}% sur le prix initial"
                            if offer_text not in seen_offers:
                                offer = {
                                    "description": {"fr": {"desc": f"Réduction de {discount_percentage}% sur le prix initial"}},
                                    "discount_percentage": discount_percentage,
                                    "requiredProductQuantity": 1
                                }   
                                if requires_loyalty_card or "carte" in offer_text.lower():
                                    offer["requires_loyalty_card"] = True
                                    offer["description"]["fr"]["desc"] += " avec la carte fidélité"   
                                offers.append(offer)
                                seen_offers.add(f"{product_id}:{offer_text}")
                                self.logger.info(f"Offre ajoutée pour {product_id}: {offer_text}")
                        else:
                            
                            self.logger.debug(f"Texte d'offre ignoré pour {product_id} : '{offer_text}'")
                                
                    # Ajouter les promotions globales au produit
                    if global_offers:
                        for global_offer in global_offers:
                            global_offer_text = global_offer["description"]["fr"]["desc"].lower()
                            if global_offer_text and not global_offer_text.isspace() and len(global_offer_text) > 1:
                                if global_offer_text not in seen_offers:
                                    offers.append(global_offer)
                                    seen_offers.add(global_offer_text)
                                    self.logger.info(f"Offre globale ajoutée pour {product_id}: {global_offer_text}")
                            else:
                                self.logger.debug(f"Offre globale ignorée pour {product_id}: '{global_offer_text}'")
                    
                    self.logger.info(f"Offres finales pour {product_id}: {[o['description']['fr']['desc'] for o in offers]}")
                    if product_id and product_url and product_title and product_id not in parsed_eans:
                        product_data.append((product_id, product_title, product_url, price, original_price, offers, requires_loyalty_card))
                        self.logger.info(f"Produit ajouté à product_data: {product_id}")
                    else:
                        self.logger.warning(f"Produit ignoré (invalide ou déjà parsé): {product_id}")
                        
                except Exception as e:
                    self.logger.error(f"Erreur extraction produit à l'index {i + start_index}: {str(e)}")
                    continue
            
            self.logger.info(f"Nombre de produits dans product_data: {len(product_data)}")

            # Parsing des produits collectés
            for product_id, product_title, product_url, price, original_price, offers, requires_loyalty_card in product_data:
                try:
                    if parse_only_ean_title_url_price:
                        product = ProductPicard(
                            ean=product_id,
                            business_type="food",
                            brand=brand,
                            lang_desc=LangDesc(fr=Desc(title=product_title, links=Links(links_self=product_url))),
                            evolutions=[EvolutionPicard(
                                price_per_packaging=price,
                                parsing_date=datetime.now().isoformat(timespec="minutes"),
                                requires_loyalty_card=requires_loyalty_card,
                                original_price=original_price,
                                on_discount=bool(offers) 
                            )],
                            offers=[OfferPicard(**o) for o in offers] if offers else None,
                            categories=[Category(label=aisle.name)]
                        )
                    else:
                        product = self._parse_full_product(driver, product_id, product_title, product_url, price, aisle_url, aisle)
                        if product:
                            product.evolutions[0].original_price = original_price
                            product.evolutions[0].requires_loyalty_card = requires_loyalty_card or any("carte" in o["description"]["fr"]["desc"].lower() for o in offers)
                            product.evolutions[0].on_discount = bool(offers)
                            if offers:
                                if product.offers is None:
                                    product.offers = [OfferPicard(**o) for o in offers]
                                else:
                                    product.offers.extend([OfferPicard(**o) for o in offers])
                                
                        else:
                            product = ProductPicard(
                                ean=product_id,
                                business_type="food",
                                brand=brand,
                                lang_desc=LangDesc(fr=Desc(title=product_title, links=Links(links_self=product_url))),
                                evolutions=[EvolutionPicard(
                                    price_per_packaging=price,
                                    parsing_date=datetime.now().isoformat(timespec="minutes"),
                                    requires_loyalty_card=requires_loyalty_card,
                                    original_price=original_price,
                                    on_discount=bool(offers)
                                )],
                                offers=[OfferPicard(**o) for o in offers] if offers else None
                            )
                            self.logger.warning(f"Produit {product_id} partiellement parsé")
                    products.append(product)
                    parsed_eans.add(product_id)
                    nb_parsed_results += 1
                    self.logger.info(f"Produit {product_id} traité: {product_title}")
                except Exception as e:
                    self.logger.error(f"Erreur lors du traitement du produit {product_id}: {str(e)}")
                    continue

            if nb_parsed_results >= max_products:
                self.logger.info(f"Limite de {max_products} produits atteinte, arrêt du parsing.")
                break

            if current_page < total_pages:
                self.logger.info(f"Passage à la page suivante {current_page + 1}")
                if not self._go_to_next_page(driver):
                    self.logger.warning("Impossible de passer à la page suivante, arrêt du parsing")
                    break
                current_page += 1
                time.sleep(1)
            else:
                self.logger.info("Dernière page atteinte, fin du parsing.")
                break

        self.logger.info(f"Total produits parsés: {nb_parsed_results}")
        return products

    def _go_to_next_page(self, driver):
        try:
            self.logger.info("Début du défilement jusqu'au bas de la page")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
         
            # Attendre que la pagination soit présente
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pi-Pagination-nav'))
            )
            self.logger.info("Pagination détectée dans le DOM")
            try:
                next_page_link = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a.pi-Pagination-link[rel="next"]'))
                )
            except Exception as e:
                self.logger.warning(f"Aucun lien 'suivant' détecté : {e}")
                return False
            next_page_url = next_page_link.get_attribute('href')
            
            
            if not next_page_url:
                self.logger.warning("Aucune URL de page suivante trouvée")
                return False
            
            if "disabled" in next_page_link.get_attribute("class"):
                self.logger.info("Le lien 'suivant' est désactivé (fin de pagination)")
                return False
        
            # Naviguer directement vers l'URL de la page suivante
            self.logger.info(f"Navigation vers la page suivante: {next_page_url}")
            driver.get(next_page_url)
            
            self.scroll_to_bottom(driver)
            
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul#search-result-items > li[class*="ProductGrid-item"]'))
            )
            self.logger.info("Page suivante chargée avec succès")
            return True
  
        except Exception as e:
            self.logger.warning(f"Erreur lors de la navigation vers la page suivante: {str(e)}")
            return False
    
    def _parse_full_product(self, driver, product_id, title, url, price, aisle_url, aisle):
        """Parsing complet d'un produit en visitant sa page"""
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img[class*='ProductCard-image']"))
            )
                   
            # Extraction de l'image
            product_img = None
            try:
                img_el = driver.find_element(By.CSS_SELECTOR, 'img[class*="ProductCard-image"]')
                product_img = img_el.get_attribute('src') if img_el else None
            except Exception as e:
                self.logger.warning(f"Erreur lors de l'extraction de l'image pour {product_id}: {str(e)}")

            # Extraction de la préparation
            preparation = []
            try:
                preparation_sections = driver.find_elements(By.CSS_SELECTOR, "div.pi-ProductTabsManual-nav.js-ProductTabsManual-accordion")
                for section in preparation_sections:
                    button = section.find_element(By.CSS_SELECTOR, "button.pi-ProductTabsManual-navItem.js-ProductTabsManual-trigger")
                    button_text = button.text.strip()
                    if "Conservation" in button_text:
                        continue
                
                    if "pi-ProductTabsManual-navItem--active" not in button.get_attribute("class"):
                        driver.execute_script("arguments[0].click();", button)
                        WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.ID, button.get_attribute("data-target")))
                        )
                        
                    target_id = button.get_attribute("data-target")
                    content = driver.find_element(By.ID, target_id)
                    blocks = content.find_elements(By.CSS_SELECTOR, "li.pi-ProductTabsManual-contentBlock")
                    for block in blocks:
                        prep_title = block.find_element(By.CSS_SELECTOR, "span.pi-ProductTabsManual-contentTitle").text.strip()
                        subtitle = block.find_element(By.CSS_SELECTOR, "strong.pi-ProductTabsManual-contentSubtitle").text.strip()
                        text = block.find_element(By.CSS_SELECTOR, "div.pi-ProductTabsManual-contentText").text.strip()
                        cooking_info = block.find_element(By.CSS_SELECTOR, "div.pi-ProductTabsManual-contentTime").text.strip() if block.find_elements(By.CSS_SELECTOR, "div.pi-ProductTabsManual-contentTime") else ""
                        preparation.append(f"{prep_title}\n{subtitle}{cooking_info}\n{text}")
                preparation = "\n\n".join(preparation) if preparation else None
                self.logger.info(f"Préparation trouvée pour {product_id}: {preparation}")
                
            except Exception as e:
                self.logger.error(f"Erreur lors de l'extraction de la préparation pour {product_id}: {e}")
            
            # Extraction de la conservation
            conservation = None
            try:
                conservation_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(), 'CONSERVATION', 'conservation'), 'conservation')]"))
                )
                target_id = conservation_button.get_attribute("data-target")
                if "pi-ProductTabsManual-navItem--active" not in conservation_button.get_attribute("class"):
                    driver.execute_script("arguments[0].click();", conservation_button)
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.ID, target_id))
                    ) 
                conservation_content = driver.find_element(By.ID, target_id)

                conservation_items = conservation_content.find_elements(By.CSS_SELECTOR, "p.pi-ProductTabsManual-contentText")
                if conservation_items:
                    conservation = "\n".join(item.text.strip() for item in conservation_items if item.text.strip())
                    self.logger.info(f"Conservation trouvée pour {product_id}: {conservation}")
                else:
                    self.logger.warning(f"Aucun contenu trouvé dans l'onglet Conservation pour {product_id}")
            except Exception as e:
                self.logger.info(f"Conservation non trouvée pour {product_id}: {e}")
                
            # Extraction des ingrédients
            ingredients = None
            allergens = []
            description = None
            try:
                ingredients_tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "tab2id"))
                )
                if not ingredients_tab.get_attribute("aria-expanded") == "true":
                    driver.execute_script("arguments[0].click();", ingredients_tab)
                    WebDriverWait(driver, 3).until(
                        EC.visibility_of_element_located((By.ID, "tab2"))
                    )
                ingredient_content = driver.find_element(By.ID, "tab2")
                # Extraire la dénomination légale
                denomination_block = ingredient_content.find_element(By.XPATH, ".//h4[contains(text(), 'Dénomination légale')]/following-sibling::div[contains(@class, 'pi-ProductTabsCms-text')]")
                description = denomination_block.text.strip()
                self.logger.info(f"Dénomination légale trouvée pour {product_id}: {description}")
                
                # Extraire la liste des ingrédients
                ingredients_block = ingredient_content.find_element(By.XPATH, ".//h4[contains(text(), 'Liste des ingrédients')]/following-sibling::div[contains(@class, 'pi-ProductTabsCms-text')]")
                ingredients = ingredients_block.text.strip()
                self.logger.info(f"Ingrédients trouvés pour {product_id}: {ingredients}")
                ingredients_normalized = self.normalize_text(ingredients)
                
                # Identifier les allergènes explicites dans les ingrédients avec ALLERGEN_PATTERNS
                for allergen_key, pattern in ALLERGEN_PATTERNS.items():
                    if re.search(pattern, ingredients_normalized, re.IGNORECASE):
                        if allergen_key not in allergens:
                            allergens.append(allergen_key)
                            
                # Identifier les traces possibles
                trace_blocks = ingredient_content.find_elements(By.XPATH, ".//div[contains(@class, 'pi-ProductTabsCms-text') and contains(text(), 'Produit élaboré dans un atelier qui utilise')]")
                for block in trace_blocks:
                    trace_text = block.text
                    trace_text_normalized = self.normalize_text(trace_text)
                    
                    for allergen_key, pattern in ALLERGEN_PATTERNS.items():
                        if re.search(pattern, trace_text_normalized, re.IGNORECASE) and f"Traces de {allergen_key}" not in allergens:
                            allergens.append(f"Traces de {allergen_key}")
          
                self.logger.info(f"Allergènes trouvés pour {product_id}: {allergens}")
            except Exception as e:
                self.logger.warning(f"Erreur lors de l'extraction des ingrédients/allergènes pour {product_id}: {str(e)}")
                return None

            #Extraction de la marque depuis le titre et la description
            brand = ProductBrand(name="Picard", brand_id=None)
            try:
                combined_text = f"{title} {description if description else ''}"
                valid_brands = set(ProductBrand.getAllKnownBrands() + ["Picard", "Cuisine Evasion", "Picard Gourmet", "Picard Bio", "Sélection Picard", "Collection Picard"])
                excluded_words = {'jambon', 'filets', 'poulet', 'crêpes', 'poêlée', 'sarlandaise', 'sarladaises', 'pommes', 'terre', 'nems', 'baozis', 'perles', 'bouchées', 'brochettes', 'dim', 'sum', 'de', 'au', 'aux', 'avec', 'et', 'sauce', 'fromage', 'emmental', 'porc', 'coco', 'nuoc-mâm', 'saté', 'canard', 'persil', 'ail', 'huile', 'tournesol', 'prefrites', 'cuisinées', 'la', 'le', 'végétal', 'légumes', 'riz', 'pâte', 'galette', 'fourrées'} 
                brand_match = re.search(r'marque\s*:\s*([^\n]+)|(?:\b(Picard|Cuisine Evasion|[A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\b)', combined_text, re.IGNORECASE)
                if brand_match:
                    potential_brand = brand_match.group(1) or brand_match.group(2)
                    if potential_brand.lower() not in excluded_words and potential_brand.lower() in [b.lower() for b in valid_brands]:
                        brand = ProductBrand(name=potential_brand, brand_id=None)
                        self.logger.info(f"Marque extraite pour {product_id}: {potential_brand}")
        
            except Exception as e:
                self.logger.info(f"Erreur lors de l'extraction de la marque pour {product_id}, utilisation de 'Picard' par défaut: {e}")
           
            # Extraction de l'origine
            self.logger.debug(f"Avant appel extract_product_origin pour {product_id}")
            origin_dict = ProductContentPicard.extract_product_origin(driver, product_id, self.logger)
            self.logger.debug(f"Après appel extract_product_origin pour {product_id}, origin_dict: {origin_dict}")
            try:
                origin = Origin(
                    explicit=origin_dict.get("explicit", None),
                    ean=None,
                    partial=origin_dict.get("partial", None)
                )
                self.logger.debug(f"Origine extraite pour {product_id}: {origin.__dict__}")
            except Exception as e:
                self.logger.error(f"Erreur lors de la création de l'objet Origin pour {product_id}: {str(e)}")
                origin = Origin(explicit=None, ean=None, partial=None)
              

            # Extraction des informations nutritionnelles
            nutrition_data = {}
            try:
                WebDriverWait(driver, 7).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(translate(., 'VALEURSNUTRITIONNELLES', 'valeursnutritionnelles'), 'valeurs nutritionnelles')]"))
                )
                table = driver.find_element(By.XPATH, "(//*[contains(translate(., 'VALEURSNUTRITIONNELLES', 'valeursnutritionnelles'), 'valeurs nutritionnelles')]/following::table)[1]")
                processed_divs = set()
                for row in table.find_elements(By.TAG_NAME, "tr"):
                    cells = row.find_elements(By.XPATH, ".//*[self::td or self::th]")
                    if len(cells) >= 2:
                        raw_key = cells[0].text.strip()
                        self.logger.debug(f"Clé brute extraite : {raw_key}")
                        
                       
                        key_parts = raw_key.split('\n') if '\n' in raw_key else raw_key.split('<br>') if '<br>' in raw_key.lower() else [raw_key]
                        key_parts = [unidecode(part.strip().lower()) for part in key_parts]
                        key_parts = [re.sub(r'[^\w\s]', '', part) for part in key_parts]
                        self.logger.debug(f"Clés normalisées : {key_parts}")
                        
                        value_cell = cells[1]  
                        value_divs = value_cell.find_elements(By.TAG_NAME, "div")
                       
                 
                        
                        for i, div in enumerate(value_divs):
                            div_id = id(div) 
                            if div_id in processed_divs:
                                continue
                            
                            div_text = div.text.strip()
                            self.logger.debug(f"Texte de div : {div_text}")
                            value = self._extract_nutrition_value(div_text)
                            if value is None:
                                continue
                            
                            key_index = min(i, len(key_parts) - 1)  
                            key_cell = key_parts[key_index]
                            
                            for key, mapped_key in NutritionPicard.NUTRITION_MAPPING.items():
                                cleaned_key = unidecode(key.lower())
                                cleaned_key = re.sub(r'[^\w\s]', '', cleaned_key)
                                if cleaned_key == key_cell:
                                    if mapped_key in ['fats', 'carbohydrates', 'proteins', 'salt', 'fiber', 'sugars', 'saturated_fats']:
                                        nutrition_data[mapped_key] = value
                                    elif mapped_key == 'energy_kj':
                                        nutrition_data['energy_kj'] = value
                                        if i + 1 < len(value_divs):
                                            next_div = value_divs[i + 1]
                                            next_div_id = id(next_div)
                                            if next_div_id not in processed_divs:
                                                next_value = self._extract_nutrition_value(next_div.text.strip())
                                                if next_value is not None:
                                                    nutrition_data['energy_kcal'] = next_value
                                                    self.logger.debug(f"Clé mappée : energy_kcal, Valeur : {next_value}")
                                                    processed_divs.add(next_div_id)
                                    
                                    break
                
                self.logger.info(f"Données nutritionnelles extraites pour {product_id}: {nutrition_data}")
                
                # Convertir en objet NutritionPicard
                nutrition = NutritionPicard.convert_dict_to_nutrition_object(nutrition_data)
                if nutrition:
                    self.logger.info(f"Données nutritionnelles converties pour {product_id}: {nutrition.__dict__}")
            except Exception as e:
                self.logger.warning(f"Erreur lors de l'extraction des informations nutritionnelles pour {product_id}: {str(e)}")
                nutrition = None

            # Extraction du avis 
            customer_reviews = None
            try:
                # Trouver la note moyenne
                rating_text_el = driver.find_element(By.CSS_SELECTOR, ".pi-Reviews-linksRate .sr-only")
                rating_text = rating_text_el.text.strip()  # Ex. "2.73 sur 5"
                average_rating = float(re.search(r'(\d+\.\d+|\d+)', rating_text).group())
                
                # Trouver le nombre total d'avis
                reviews_link_el = driver.find_element(By.CSS_SELECTOR, ".pi-Reviews-linksItem.js-GoToReviews")
                reviews_text = reviews_link_el.text.strip()  # Ex. "Lire 139 avis"
                total_reviews = int(re.search(r'\d+', reviews_text).group())
                
                customer_reviews = {
                    "average_rating": average_rating,
                    "total_reviews": total_reviews
                }
                self.logger.info(f"Avis clients trouvés pour {product_id}: {customer_reviews}")
           
            except NoSuchElementException:
                self.logger.info(f"Aucun avis client présent pour {product_id} (élément introuvable)")
            
            except AttributeError:
                self.logger.warning(f"Format de texte inattendu pour les avis (rating ou total) sur {product_id}")
            
            except Exception as e:
                self.logger.warning(f"Erreur inconnue lors de l’extraction des avis pour {product_id}: {e}")
            
            
            # Extraction du format 
            format_match = re.search(r'(\d+\s*(à|-)\s*\d+\s*(pièces|tranches|portions|parts|crêpes)|sachet\s*de\s*(\d+\.?\d*\s*(g|kg))|\d+\.?\d*\s*(g|kg))', title, re.IGNORECASE)
            product_format = format_match.group(0) if format_match else None
            if not format_match:
                try:
                   weight_el = driver.find_element(By.CSS_SELECTOR, "div.pi-ProductDetails-weight span")
                   weight_text = weight_el.text.strip()
                   product_format = weight_text 
                except:
                    product_format = None
            
            # Extraction du poids 
            weight = None
            unit = None
            try:
                weight_el =driver.find_element(By.CSS_SELECTOR, "div.pi-ProductDetails-weight span")
                weight_text = weight_el.text.strip()
                
                self.logger.debug(f"Poids trouvé pour {product_id}: {weight}")
               
                # Extraire le poids avec une expression régulière
                weight_match = re.search(r'(\d+\.?\d*)\s*(g|kg)', weight_text, re.IGNORECASE)
                if weight_match:
                    weight = float(weight_match.group(1))
                    unit = weight_match.group(2).lower()
                    if unit == "kg":
                        weight *= 1000 
                    self.logger.info(f"Poids trouvé pour {product_id}: {weight} g")
                else:
                    self.logger.info(f"Format de poids invalide pour {product_id}: {weight_text}")
                        
            except Exception:
                self.logger.info(f"Poids non trouvé pour {product_id}")
                
            # Utiliser le titre ou la description pour extraire le poids
            if not weight:
                try:
                    
                    combined_text = f"{title} {description if description else ''}"
                    weight_match = re.search(r'(\d+\.?\d*)\s*(g|kg)', combined_text, re.IGNORECASE)
                    if weight_match:
                        weight = float(weight_match.group(1))
                        unit = weight_match.group(2).lower()
                        if unit == "kg":
                             weight *= 1000
                        self.logger.info(f"Poids extrait du titre/description pour {product_id}: {weight} g")
                    else:
                        self.logger.info(f"Poids non trouvé dans le titre/description pour {product_id}")
                        
                except Exception as e:
                    self.logger.info(f"Erreur lors de l'extraction du poids depuis le titre/description pour {product_id}: {str(e)}")
                    
                    
            #definir unit_of_measure
            unit_of_measure = "g" if weight is not None else None
            self.logger.info(f"Unit of measure défini pour {product_id}: {unit_of_measure}")

            # Extraction du nutriscore
            nutriscore = None
            try:
                nutriscore_el = driver.find_element(By.CSS_SELECTOR, '.pi-ProductTabsNutrition-nutriscoreBlock .sr-only')
                nutriscore_text = nutriscore_el.text.strip().lower()  # Ex: "nutriscore-d"
                nutriscore = nutriscore_text.replace("nutriscore-", "").upper()  # Ex: "D"
            except NoSuchElementException:
                self.logger.info(f"Nutriscore non disponible pour {product_id}")
          
            
            # Création de l'objet produit
            evolution = EvolutionPicard(
                parsing_date=datetime.now().isoformat(timespec="minutes"),
                weight_per_packaging=weight,
                price_per_packaging=price,
                format=product_format,  
                nutriscore=nutriscore,
                availability=True,
                ingredients=ingredients,
                nutrition=nutrition,
                allergens=allergens if allergens else None,
                preparation=preparation,
                conservation=conservation
            )
            
            return ProductPicard(
                ean=product_id,
                business_type="food",
                brand=brand,
                lang_desc=LangDesc(
                    fr=Desc(
                        title=title,
                        desc=description,
                        images=[product_img] if product_img else None,
                        links=Links(links_self=url)
                    )
                ),
                evolutions=[evolution],
                offers=None,
                market=MarketPicard(),
                customer_reviews=customer_reviews if customer_reviews else None,
                origin=origin,
                categories=[Category(label=aisle.name)] 
            )

        except Exception as e:
            self.logger.error(f"Erreur lors du parsing complet du produit {product_id}: {str(e)}")
            return None

    def _extract_nutrition_value(self, text):
        """Extraction des valeurs nutritionnelles"""
        try:
            clean_text = text.lower().replace(',', '.').strip('~* ')
            # Gérer les valeurs comme "< 0,5"
            if '<' in clean_text:
                clean_text = clean_text.replace('<', '').strip()
                return 0.5  
            matches = re.findall(r'(\d+\.?\d*)\s*(kj|kcal|g)?', clean_text)
            if matches:
                value = float(matches[0][0])
                return value
            return None
        except Exception as e:
            self.logger.debug(f"Erreur extraction valeur depuis '{text}': {str(e)}")
            return None

if __name__ == "__main__":
    cmdargs = sys.argv
    if len(cmdargs) > 1:
        max_products = None
        if len(cmdargs) > 2 and cmdargs[2].isdigit():
            max_products = int(cmdargs[2])
        
        picard = PicardAislesProductsScanner()
        aisles: List[StaticAisle] = picard_static_aisles.get_static_aisles_from_user_cmdargs(cmdargs=cmdargs)
        print(f"Selected aisles: {aisles}")
        if not aisles:
            print("No aisles found")
            sys.exit()

        for aisle in aisles:
            print(f"Scraping l'URL: {aisle.url}")
            new_products = picard.parse_products(
                webdriverInstance,
                aisle,
                parse_only_ean_title_url_price=False,
                parse_only_first_x_products=max_products,  # Limiter à max_products (ex. 3)
                parse_only_from_index=None,
                latest_parsed_products=[],
                max_products=max_products
            )
            if not new_products:
                print(f"Aucun produit trouvé pour {aisle.name} ({aisle.url})")
            else:
                print(f"{len(new_products)} produits récupérés depuis {aisle.url}")
            dump_json_then_write_it_to_file(aisle.original_file_uri.replace(".json", ""), new_products)
    else:
        print("Incorrect number of arguments")
        sys.exit()




import os
import sys
import datetime

from src.utils.my_utils import dump_json_then_write_it_to_file
from src.model.my_model import ProductAisle, ProductCategory
from src.countries.france.picard.robots import picard_static_aisles, webdriverInstance
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List

poll_frequency = 10

class ScannerPicardBrands:
    def __init__(self):
        self.first_access = True

    def parse_brands(self, driver: webdriver, aisle_url: str) -> List[str]:
        try:
            print(f"*** Accès à L'URL: {aisle_url}")
            brands_names: List[str] = []
            driver.get(aisle_url)
            
            if self.first_access:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label*="Refuser"]'))
                    ).click()
                    print("Cookies refusés")
                except TimeoutException:
                    print("Pas de bannière cookies à gérer.")
                self.first_access = False
                
            # Ouvrir le filtre "marque"
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.pi-FacetGroup[data-facet="marque"] button'))
                ).click()
            
            # Extraire les noms de marques
            brand_els = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.pi-FacetGroup[data-facet="marque"] span.pi-FacetOption-label'))
            )

            for brand_el in brand_els:
                name = brand_el.get_attribute("innerHTML").strip()
                print(f"Marque trouvée : {name}")
                brands_names.append(name)
            return brands_names
        
        except Exception as e:
            print(f"Erreur lors de l'extraction des marques : {e}")
            return None
               
            
if __name__ == "__main__":
    sections: List[ProductCategory] = []
    scanner = ScannerPicardBrands()
    
    picard_sections = picard_static_aisles.picard_categories_with_uris
    all_brands = []
    
    for section in picard_sections:
        print(f"Section : {section.name}")
        updated_aisles = []
        for aisle in section.aisles:
            print(f"Aisle : {aisle.name}")
            brands = scanner.parse_brands(webdriverInstance, aisle.url)
            if not brands:
                print(f" Aucune marque trouvée pour {aisle.url}")
                continue
            aisle.brands = brands
            updated_aisles.append(aisle)
            all_brands.extend(brands)
        
        section.aisles = updated_aisles
        sections.append(section)
        
        
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'brands'))
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, "picard_brands.json")
    dump_json_then_write_it_to_file(file_path, sections)   

else:
    print("Ce fichier a été importé comme module :", __name__) 
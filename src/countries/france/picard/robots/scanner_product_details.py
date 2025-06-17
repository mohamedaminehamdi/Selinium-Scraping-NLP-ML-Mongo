# ... your imports and class definitions
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Jan 28, 2019

@author: marwen
"""
# standard imports

from utils.my_utils import write_output_to_file
from utils.GS1 import extract_all_countries
from utils.ean_country_checker import get_country_code_from_country_name_in_french_lang
from utils.appium_utils import get_attribute_from_element, wait_el, wait_el_click, wait_el_text, wait_els
from static_category_aisle import StaticRayon
from product import Desc, Evolution, Label, LangDesc, Market, Origin, ProductV2
from model.product_content import convert_format_product
from src.countries.france.picard.robots.picard_static_aisles import get_static_rayons_from_user_cmdargs
from countries.france.picard.model.picard_content import extract_rating, is_allergens
from countries.france.naturalia.robots.__init__ import webdriverInstance
from countries.france.naturalia.model.naturalia_content import split_ingredients
from countries.france.auchan.model.product_auchan import extract_price, extract_unit_of_mesure
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium import webdriver
import requests
import datetime
import json
import logging
import os
import sys
import time
from typing import Final, List

sys.path.append('src')
# third-party libraries


# checkpaths and modules
if './' not in sys.path:
    sys.path.append('./')
if os.getcwd() not in sys.path:  # sys.modules
    sys.path.append(os.getcwd())

# local imports


# ... your imports and class definitions

class ScannerProductDetails:
    def __init__(self):
        self.total_products_number = 0
        self.first_access = True

    def parse_product_details_only_if_no_available(self, driver: webdriver, product: dict) -> [ProductV2]:
        print("product title : ", product["lang_desc"]["fr"]["title"])
        product_link = product["lang_desc"]["fr"]["links"]["links_self"]

        # Call parse_product_details to get product details
        product_details = self.parse_product_details(driver, product_link)
        return product_details

    def parse_product_details(self, driver: webdriver, product_url: str) -> dict | None:
        try:
            print("***gonna parse product_url: " + product_url)
            driver.get(product_url)
            products: List[ProductV2] = []
            if self.first_access:

                # should click on cookies panel just the first time the driver is launched

                wait_el_click(driver, By.CLASS_NAME, 'ot-close-link', 3)
                self.first_access = False

            start_parsing_date = datetime.datetime.now()
            product_non_plus = wait_el(driver, By.CLASS_NAME, 'pi-ProductDetails-unavailable--red')
            if product_non_plus is None:
                url = None
                url_el = wait_el(driver, By.XPATH, '//*[@id="pdpMain"]/div/div[1]/div[3]/div/div[3]/meta[4]')
                if url_el is None:
                    url_el2 = wait_el(driver, By.XPATH, '//*[@id="pdpMain"]/div/div[1]/div[3]/div/div[3]/meta[3]')
                    url = get_attribute_from_element(url_el2, "content")
                else:
                    url = get_attribute_from_element(url_el, 'content')
                print("url : ", url)
                brand_url = wait_el(driver, By.XPATH, '//*[@id="pdpMain"]/div/div[1]/meta[1]')
                brand = get_attribute_from_element(brand_url, 'content')
                print("brand : ", brand)
                available = True
                availability = wait_el(driver, By.XPATH, '//*[@id="pdpMain"]/div/div[1]/div[3]/div/div[5]', 0.5)
                if availability is None:
                    available = False
                    print("available : ", available)

                # non_plus =  wait_el(driver,By.CLASS_NAME,"product-unavailable__message")
                img_el = wait_el(driver, By.CLASS_NAME, "pi-ProductImage-image", 0.5)
                img = get_attribute_from_element(img_el, 'src')
                print("image source: ", img)
                product_name = wait_el_text(driver, By.CLASS_NAME, "pi-ProductPage-title", 0.5)
                print("product name: ", product_name)

                price_el = wait_el_text(driver, By.CLASS_NAME, "pi-ProductDetails-salesPrice", 0.5)
                print(price_el)
                if "Prix soldé" in price_el:
                    price_el = price_el.replace("Prix soldé", "")
                if "\n" in price_el:
                    price_el = price_el.replace("\n", "")
                print("price el ba3ed el relpace: ", price_el)
                price = extract_price(price_el)
                print("price ba3ed el relpace: ", price)

                price_per_unit_el = wait_el_text(driver, By.CLASS_NAME, "pi-ProductDetails-kiloPrice", 0.5)

                price_per_unit_el = price_per_unit_el.lower()
                # matter:
                matter = "OTHER"
                if price_per_unit_el.find("kg") != -1:
                    matter = "SUBSTANCE"
                    print("matter state : ", matter)
                elif price_per_unit_el.find("l") != -1:
                    matter = "LIQUID"
                    print("matter state : ", matter)
                elif price_per_unit_el.find("pce") != -1 or price_per_unit_el.find("pièce") != -1:
                    matter = "PIECE"
                    print("matter state : ", matter)
                else:
                    matter = "OTHER"

                if "prix au kilo" in price_per_unit_el:
                    price_per_unit_el = price_per_unit_el.replace("prix au kilo", "")
                if "\n" in price_per_unit_el:
                    price_per_unit_el = price_per_unit_el.replace("\n", "")
                price_per_unit = extract_price(price_per_unit_el)
                print("price per unit:", price_per_unit)
                packaging_el = wait_el_text(driver, By.CLASS_NAME, "pi-ProductDetails-weight", 0.5)
                print("packaging : ", packaging_el)

                unit_of_mesure = extract_unit_of_mesure(price_per_unit_el)
                ref = wait_el_text(driver, By.CLASS_NAME, "pi-ProductDetails-ref", 0.5)
                print("ref : ", ref)

                ref_value = ""
                if packaging_el in ref:
                    ref = ref.replace(packaging_el, "")
                if "\n" in ref:
                    ref = ref.replace("\n", "")

                if "Ref: " in ref:
                    ref_value = ref.replace("Ref: ", "")
                    print("ref value : ", ref_value)

                packaging = convert_format_product(packaging_el)
                print("packaging converted :", packaging)

                # packaging_mesure_unit
                packaging_unit = packaging[0]
                print("packaging measure unit : ", packaging_unit)
                # packaging_mesure_value
                packaging_value = packaging[1]
                print("packaging measure value : ", packaging_value)
                format2 = wait_el_text(driver, By.CSS_SELECTOR, '#pdpMain > div > div.pi-ProductPage-top > div.pi-ProductPage-medias > div.pi-ProductPage-caracsAndLabels > ul.pi-ProductCaracs > li.pi-ProductCaracs-caracteristic', 0.5)
                print("format 2: ", format2)

                review = wait_el_text(driver, By.CSS_SELECTOR, "#pdpMain > div > div.pi-ProductPage-top > div.pi-ProductPage-details > div > div.pi-Reviews-links > div > span.sr-only", 0.5)

                print("review :", review)
                rating_value = extract_rating(review)
                print("rating :", rating_value)

                nutri_score_el = wait_el(driver, By.CSS_SELECTOR, "#pdpMain > div > div.pi-ProductPage-top > div.pi-ProductPage-medias > div.pi-ProductPage-caracsAndLabels > ul.pi-ProductLabel > li:nth-child(1) > svg > use", 0.5)
                nutri_score_href = get_attribute_from_element(nutri_score_el, "href", "nutri_score_href")
                print("nutri score href :", nutri_score_href)

                nutri_score = ""
                if nutri_score_href == "https://www.picard.fr/on/demandware.static/Sites-picard-Site/-/fr_FR/v1715615792915/assets/svg/sprite.symbol.svg#nutriscore-d":
                    nutri_score = "D"
                elif nutri_score_href == "https://www.picard.fr/on/demandware.static/Sites-picard-Site/-/fr_FR/v1715615792915/assets/svg/sprite.symbol.svg#nutriscore-a":
                    nutri_score = "A"
                elif nutri_score_href == "https://www.picard.fr/on/demandware.static/Sites-picard-Site/-/fr_FR/v1715615792915/assets/svg/sprite.symbol.svg#nutriscore-b":
                    nutri_score = "B"
                elif nutri_score_href == "https://www.picard.fr/on/demandware.static/Sites-picard-Site/-/fr_FR/v1715615792915/assets/svg/sprite.symbol.svg#nutriscore-c":
                    nutri_score = "C"
                elif nutri_score_href == "https://www.picard.fr/on/demandware.static/Sites-picard-Site/-/fr_FR/v1715615792915/assets/svg/sprite.symbol.svg#nutriscore-e":
                    nutri_score = "E"

                print("nutri score :", nutri_score)

                on_discount = None
                offer = None
                on_discount_el = wait_el(driver, By.CLASS_NAME, "pi-ProductOffer-description")
                if on_discount_el:
                    on_discount = True
                    offer = wait_el_text(driver, By.CLASS_NAME, "pi-ProductOffer-title")

                ingrediant_button = wait_el_click(driver, By.CSS_SELECTOR, "#tab2id", 1)
                desc = wait_el_text(driver, By.XPATH, '//*[@id="tab2"]/div/div[2]/div[1]/div', 0.5)

                print("desc: ", desc)
                ingrediants = None
                ingrediant = wait_el_text(driver, By.XPATH, '//*[@id="tab2"]/div/div[2]/div[2]/div', 0.5)
                if ingrediant is not None:
                    ingrediants = split_ingredients(ingrediant)
                    print("ingrediants : ", ingrediants)
                allergens = None
                allergens_el = wait_el_text(driver, By.XPATH, '//*[@id="tab2"]/div/div[2]/div[3]/div', 0.5)
                print("allergens : ", allergens_el)

                if allergens_el is not None:
                    allergens = is_allergens(allergens_el)

                    print("allergens :", allergens)

                nutrition_values_button = wait_el_click(driver, By.CSS_SELECTOR, "#tab3id", 0.5)
                nutrition_dict = {}
                nutritional_details_table = wait_el(driver, By.XPATH, '//*[@id="tableNutrition0"]/table/tbody', 0.5)
                if nutritional_details_table is not None:
                    nutritional_details_table_els = wait_els(nutritional_details_table, By.CLASS_NAME, 'pi-ProductTabsNutrition-tableRow', 0.5)
                    nutrition_name2 = None
                    nutrition_name1 = None
                    nutrition_value1 = None
                    nutrition_value2 = None
                    if nutritional_details_table_els is not None:
                        nutrition_dict = {}
                        for nutritional_details_table_row_els in nutritional_details_table_els:
                            nutrition_name1 = wait_el_text(nutritional_details_table_row_els, By.CSS_SELECTOR, "#tableNutrition0 > table > tbody > tr > td:nth-child(1)", 0.5)
                            # print("nutri name " +str(nutrition_name) )
                            # nutrition_name = nutrition_name.lower()
                            # nutrition_name=convert_nutrition_name(nutrition_name)
                            print("nutri name :" + str(nutrition_name1))

                            nutrition_value1 = wait_el_text(nutritional_details_table_row_els, By.CSS_SELECTOR, "#tableNutrition0 > table > tbody > tr > td:nth-child(2)", 0.5)
                            if "\n" in nutrition_name1:
                                nutrition_names = nutrition_name1.split('\n')
                                nutrition_name1 = nutrition_names[0]
                                print("nutrition name 1: ", nutrition_name1)

                                nutrition_name2 = nutrition_names[1]
                                print("nutrition name 2: ", nutrition_name2)
                                if "\n" in nutrition_value1:
                                    nutrition_values = nutrition_value1.split('\n')
                                    nutrition_value1 = nutrition_values[0]
                                    print("nutrition value 1: ", nutrition_value1)

                                    nutrition_value2 = nutrition_values[1]
                                    print("nutrition value 2: ", nutrition_value2)
                                nutrition_dict[nutrition_name1] = nutrition_value1
                                nutrition_dict[nutrition_name2] = nutrition_value2

                            else:
                                nutrition_dict[nutrition_name1] = nutrition_value1

                        print("nutritional_details_table_els: ", nutrition_dict)

                list_origin = []
                origin = wait_el_text(driver, By.ID, 'tab5id')
                time.sleep(2)
                driver.execute_script("window.scrollBy(0, 100)")
                origin_button = wait_el_click(driver, By.ID, 'tab5id', 2)

                print("oringin: ", origin)
                origin_el = wait_el(driver, By.ID, 'tab5id', 1)
                partial = None
                origin_text = wait_el_text(driver, By.CSS_SELECTOR, "#tab5 > div > div.pi-ProductTabsCms-container > div > div", 0.5)
                if origin_text is not None:
                    print("origin text :", origin_text)
                    list_origin1 = extract_all_countries(origin_text)
                    print("list des pays :", list_origin1)
                    list_origin = []
                    for pays in list_origin1:
                        print("pays:", pays)
                        origin_pay = get_country_code_from_country_name_in_french_lang(pays)
                        list_origin.append(origin_pay)
                    if partial == []:
                        partial = None
                    else:
                        partial = list_origin[1:]

                    print("list origin :", list_origin)
                    print("origin explicit :", list_origin[0])
                    print("origin implicit :", list_origin[1:])
                    origin = Origin(ean=None, explicit=list_origin[0], partial=partial)
                    print("ORIGIN:", origin)

                print("les icons :")
                icons_els = wait_els(driver, By.CLASS_NAME, "pi-ProductLabel-image")
                label = []
                if icons_els is not None:
                    for icon_el in icons_els:
                        icon_text = get_attribute_from_element(icon_el, "src", "icon_text")
                        print(icon_text)
                        if icon_text == "https://www.picard.fr/on/demandware.static/-/Sites-catalog-picard/default/dw3b146b97/label/bio-europeen.jpg":
                            label.append(Label(bio=True))
                        # if icon_text == "AB Agriculture biologique":
                        #     label.append( Label(bio = True))
                        if icon_text == "https://www.picard.fr/on/demandware.static/-/Sites-catalog-picard/default/dw0802e57e/label/vegetarien.jpg":
                            label.append(Label(vegetarian=True))

                        else:
                            print("no icons found")
                print("LES ICONS: ", label)

                created_at = datetime.datetime.now().isoformat(timespec="minutes")
                update_at = datetime.datetime.now().isoformat(timespec="minutes")

                lang_desc = LangDesc(fr=Desc(title=product_name, packaging=packaging_el, desc=desc, images=img, links=product_url))
                logging.info(lang_desc)
                evolution = Evolution(parsing_date=created_at, format=packaging_el, format2=format2, availability=available, price_per_unit=price_per_unit, price=price, packaging_measure_value=packaging_value, packaging_measure_unit=packaging_unit, nutriscore=nutri_score, nutrition=nutrition_dict, ingredients=ingrediants, allergens=allergens, customer_reviews=rating_value, on_discount=on_discount, offers=[offer])
                logging.info(evolution)
                market = Market(name="Picard", country="France")
                logging.info(market)
                product_details = ProductV2(ean=ref_value, brand=brand, categories="unique_categories", business_type="food", origin=origin, unit_of_mesure=unit_of_mesure, matter=matter, market=market, lang_desc=lang_desc, evolutions=[evolution], label=label, created_at=created_at, updated_at=update_at)

                logging.info(product_details)  # Log product details
                products.append(product_details)
                print("PRODUCTS: ", products)

            return products

        except requests.Timeout:
            print("Timeout occurred for request page : " + product_url)
            return products
        except:
            print("global except error: ", sys.exc_info())
            return products  # Indicate failure to parse details


if __name__ == "__main__":
    print("my main")
    # Get the arguments list
    cmdargs = sys.argv

    # Print it
    print("The total numbers of args passed to the script: " + str(len(cmdargs)) + ", Args list: " + str(cmdargs))
    # first arg section, second arg rayon
    if len(cmdargs) > 1:  # in (1, 2):
        scannerProductDetails = ScannerProductDetails()
        rayons: [StaticRayon] = get_static_rayons_from_user_cmdargs(cmdargs=cmdargs)
        print("rayons: " + str(len(rayons)))
        if rayons is None:
            print("empty rayons")
            sys.exit()

        # Initialize an empty list to store all products
        all_products = []

        for rayon1 in rayons:
            rayon: StaticRayon = rayon1
            print('section_name: ' + rayon.name)
            file_uri = rayon.mini_file_uri
            print("file uri ", file_uri)

            json_file = open(file_uri)
            products = json.load(json_file)

            # Extend the all_products list with the products from the current category
            all_products.extend(products)

        # Now, all_products contains a simple list of all products from all categories

        # Iterate through all products and parse product details
        products_details = []
        for product in all_products:
            product_link = product["lang_desc"]["fr"]["links"]["links_self"]
            print("product_link: " + product_link)

            if len(cmdargs) == 3 or cmdargs[2] == "parse_product_details_only_if_no_available":
                new_products_details = scannerProductDetails.parse_product_details_only_if_no_available(webdriverInstance, product)
            else:
                new_products_details = scannerProductDetails.parse_product_details(webdriverInstance, product_link)

            if new_products_details is not None:
                # Extend the products_details list with the details of the current product
                products_details.extend(new_products_details)

        json_object = json.dumps(products_details,
                                 default=lambda o: dict((key, value) for key, value in o.__dict__.items() if value),
                                 indent=4,
                                 allow_nan=False,
                                 ensure_ascii=False)
        rayon_uri = rayon.original_file_uri.replace(".json", "_details")
        write_output_to_file(data=json_object, file_name=rayon_uri, path_includes_in_file_name=True, include_seconds_in_date=False, extension='.json')

        # with open("src\\robots\\france\picard\products\\fake_products\details.csv", 'w') as f:
        #     # Create CSV writer object
        #     writer = csv.writer(f)

    else:
        print("wrong args number")
        sys.exit()


else:
    print(
        "this was imported by:" + __name__)

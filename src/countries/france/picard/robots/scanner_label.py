# ... your imports and class definitions
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Jan 28, 2019

@author: marwen
"""
# standard imports

import logging
import os
import sys
from typing import List
import datetime

# third-party libraries
from selenium.webdriver.common.by import By
from selenium import webdriver

from product import Desc, LangDesc, ProductV2
from static_category_aisle import StaticRayon


# checkpaths and modules
if './' not in sys.path:
    sys.path.append('./')
if os.getcwd() not in sys.path:  # sys.modules
    sys.path.append(os.getcwd())

# local imports
from robots.france.picard.static_data import get_static_rayons_from_user_cmdargs  # NOQA
from utils.appium_utils import wait_els, wait_el_text, wait_el_click, wait_el  # NOQA
from utils.my_utils import write_output_to_file  # NOQA
from robots.france.picard import webdriverInstance, json, requests  # NOQA
from utils.appium_utils import get_attribute_from_element


class ScannerProductDetails:
    def __init__(self):
        self.total_products_number = 0
        self.first_access = True

    def parse_product_details_only_if_no_available(self, driver: webdriver, product: dict) -> List[ProductV2]:
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

                print("les icons :")
                icons_els = wait_els(driver, By.CLASS_NAME, "pi-ProductLabel-image")
                label = []
                if icons_els is not None:
                    for icon_el in icons_els:
                        icon_text = get_attribute_from_element(icon_el, "src", "icon_text")
                        print(icon_text)

                        label = icon_text
                print("LES ICONS: ", label)

                lang_desc = LangDesc(fr=Desc(title=product_name, images=img, links=product_url))
                logging.info(lang_desc)

                product_details = ProductV2(lang_desc=lang_desc, label=label)

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
        rayons: List[StaticRayon] = get_static_rayons_from_user_cmdargs(cmdargs=cmdargs)
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

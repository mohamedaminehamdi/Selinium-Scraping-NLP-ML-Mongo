import json
import os
import sys
sys.path.append('src')
from countries.common_fonction import get_data_from_json, get_files_from_directory, save_checkpoint, send_email
from src.countries.france.picard.robots.picard_static_aisles import picard_categories_with_uris
from model.my_model import ProductCategory, ProductRayon
from product import ProductV2
from utils.my_utils import write_output_to_file

import requests
from countries.test_connection import test_connection_stability, visualize_results
from src.countries.france.picard.robots.picard_aisles_products_scanner import PicardV2
from countries.france.picard.robots.scanner_product_details import ScannerProductDetails
import time
from typing import List
from countries.france.naturalia.robots.__init__ import webdriverInstance



# # Désactiver la mise en veille
os.system("powercfg /change standby-timeout-ac 0")
try:
    print("Start Parsing Rayon Products")
    picard = PicardV2(driver="chrome")
    picard_sections = picard_categories_with_uris
    sections: List[ProductCategory] = []

    for picard_section in picard_sections:
        section_name = picard_section.name
        section_url = picard_section.url
        print("section name :", section_name)
        print("section url :", section_url)

        rayons: List[ProductRayon] = []

        for auchan_rayon in picard_section.rayons:
            rayon_name = auchan_rayon.name
            rayon_url_to_parse = auchan_rayon.url
            print("\tRayon name : ", rayon_name)
            print("\tRayon url : ", rayon_url_to_parse)

            if rayon_url_to_parse is None:
                print("rayon url is None")
                # Handle the missing rayon_url gracefully
                print(f"Error: Rayon URL for '{rayon_name}' is None. Skipping this rayon.")
                continue  # Continue to the next rayon

            rayon_uri = auchan_rayon.original_file_uri.replace(".json", "_smallest_from_robot")
            print("*************************************************************")
            print(f"rayon_uri : {rayon_uri}")

            while True:
                try:
                    new_products = picard.parse_products(webdriverInstance, rayon_url_to_parse)
                    if new_products is None:
                        break  # Exit the while loop and continue to the next rayon

                    json_object = json.dumps(new_products,
                                            default=lambda o: dict(
                                                (key, value) for key, value in o.__dict__.items() if value),
                                            indent=4,
                                            allow_nan=False,
                                            ensure_ascii=False)
                    write_output_to_file(data=json_object, file_name=rayon_uri,
                                        path_includes_in_file_name=True, include_seconds_in_date=False, extension='.json')
                    break  # Exit the while loop if successful
                    
                except requests.ConnectionError as e:
                    print("Network error:", e)
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                    continue  # Retry the while loop
                    
                except requests.Timeout as e:
                    print("Request timeout:", e)
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                    continue  # Retry the while loop
                
                except Exception as e:
                    print("An unexpected error occurred:", e)
                    # Log the error and continue with the next rayon
                    break  # Exit the while loop

            time.sleep(3)  # Allow the browser and system to breathe

    print("End Pasring Rayon Products")
    time.sleep(5)

    # print("Start Pasring Product Details")
    # num_requests = 20  # Adjust as needed
    # interval = 2  # Adjust as needed
    # scannerProductDetails = ScannerProductDetails()
    # parsed_products_details: List[ProductV2] = []
    # # products_details: List[ProductV2] = []
    # all_products = []
    # directory_path = r"src\\countries\\france\\naturalia\\robots\\products"
    # error_path = r"src\\countries\\france\\naturalia\\robots\\errors"
    # json_files = get_files_from_directory(directory_path)
    # for json_file in json_files:
    #     # Désactiver la mise en veille
    #     os.system("powercfg /change standby-timeout-ac 0")
    #     product_list = []
    #     print("JSON FILE : ",json_file)
    #     products = get_data_from_json(json_file)
    #     print("URLS /: ",products)
    #     for product in products:
    #         categories = product["categories"]
    #         while True:
    #             try:
    #                 url = product["lang_desc"]["fr"]["links"]["links_self"]
    #             except KeyError as e:
    #                 print(f"KeyError: {e} not found in product: {product}")
    #                 continue
    #             success_count, fail_count, response_times = test_connection_stability(url, num_requests, interval)
    #             print(f"Success: {success_count}, Failures: {fail_count}")

                
    #             if fail_count>3 :
    #                 print("Too many failures, skipping product")
                    
                
    #             product_details_list = scannerProductDetails.parse_product_details_only_if_no_available(webdriverInstance, product)
    #             print(product_details_list)
    #             if product_details_list is not None:
    #                 for product_details in product_details_list:
    #                     product_details.categories = categories
    #                     parsed_products_details.append(product_details)
    #                     print("PRODUCT DETAILS : ", product_details)
    #             else:
    #                 print("Failed to parse product details for product: ", product)
    #                 # Envoyer un e-mail après la fin du scraping
    #                 subject = "Failed to parse product details for product"
    #                 body = "The scraping process has been failed to parse this product : "+product
    #                 to_email = "benabdelghaniamal@gmail.com"
    #                 send_email(subject, body, to_email)
    #                 print("mail was sent")

    #                 # Save the current URL as the checkpoint after processing
    #                 save_checkpoint(error_path,url)
    #                 visualize_results(success_count, fail_count, response_times)
    #             time.sleep(2) #pour permettre au navigateur et au système de respirer

    #     json_object = json.dumps(parsed_products_details,
    #                                 default=lambda o: dict((key, value) for key, value in o.__dict__.items() if value),
    #                                 indent=4,
    #                                 allow_nan=False,
    #                                 ensure_ascii=False)
    #     rayon_uri = json_file.replace(".json", "_details")
    #     try:
    #         rayon_uri = json_file.replace(".json", "_details")
    #         write_output_to_file(data=json_object, file_name=rayon_uri, path_includes_in_file_name=True, include_seconds_in_date=False, extension='.json')
    #         print(f"Successfully wrote output to {rayon_uri}")
            
    #         # Delete the processed JSON file after successful parsing
    #         os.remove(json_file)
    #         print(f"Successfully deleted {json_file}")
    #     except Exception as e:
    #         print(f"Failed to write output or delete file: {e}")



    #     time.sleep(5) #pour permettre au navigateur et au système de respirer



    # # Envoyer un e-mail après la fin du scraping
    # subject = "Scraping Completed"
    # body = "The scraping process has been successfully completed."
    # to_email = "benabdelghaniamal0@gmail.com"
    # send_email(subject, body, to_email)


finally:
    # Réactiver la mise en veille (après l'exécution de votre code)
    os.system("powercfg /change standby-timeout-ac 30")  # 30 minutes, par exemple
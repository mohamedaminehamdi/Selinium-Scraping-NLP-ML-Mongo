import os , sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'utils'))
sys.path.append(parent_dir)
from src.utils.GS1 import GS1_list
from typing import Optional
import pycountry
import sys

from src.utils.countries2 import LangType, get_english_country_code
sys.path.append('./')

def get_country_from_ean_v2(ean, country_ranges):

    country_code = int(ean[:3])
    country_name = ''
    result_list = []
    formatted_results = []

    for range_dict in country_ranges:
        for key, value in range_dict.items():
            if '–' in key:
                start, end = map(int, key.split(' – '))
                if start <= country_code <= end:
                    country_name = value
                    break
            elif int(key) == country_code:
                country_name = value
                break
    if " and " in country_name:
        if country_name == 'Bosnia and Herzegovina':
            result = pycountry.countries.get(name=country_name)
            result_list.append({"alpha_2": result.alpha_2})
        else:
            country_names = country_name.split(" and ")
            for country in country_names:
                result = pycountry.countries.get(name=country)
                result_list.append({"alpha_2": result.alpha_2})

        for result_dict in result_list:
            formatted_results.append((result_dict['alpha_2']))

        return formatted_results
    else:
        try:
            result = pycountry.countries.get(name=country_name)
            formatted_results.append(result.alpha_2)
            return formatted_results
        except AttributeError:
            return ['']


def get_country_from_ean(ean, country_ranges):

    country_code = int(ean[:3])
    country_name = ''
    result_list = []
    formatted_results = []

    for range_dict in country_ranges:
        for key, value in range_dict.items():
            if '–' in key:
                start, end = map(int, key.split(' – '))
                if start <= country_code <= end:
                    country_name = value
                    break
            elif int(key) == country_code:
                country_name = value
                break
    if " and " in country_name:
        if country_name == 'Bosnia and Herzegovina':
            result = pycountry.countries.get(name=country_name)
            return result_list.append({"alpha_3": result.alpha_3, "numeric": result.numeric})

        country_names = country_name.split(" and ")

        for country in country_names:
            result = pycountry.countries.get(name=country)
            result_list.append({"alpha_3": result.alpha_3, "numeric": result.numeric})

        for result_dict in result_list:
            formatted_results.append(f"{result_dict['alpha_3']} ({result_dict['numeric']})")

        # Join the list of formatted strings into a single string
        return ", ".join(formatted_results)

    else:
        result = pycountry.countries.get(name=country_name)
        return result.alpha_3, result.numeric


def get_country_codes(country_name):
    if " and " in country_name:
        if country_name == 'Bosnia and Herzegovina':
            return pycountry.countries.get(name=country_name).alpha_2
        country_names = country_name.split(" and ")
        country_codes = [pycountry.countries.get(name=name).alpha_2 for name in country_names if pycountry.countries.get(name=name)]
        return ", ".join(country_codes)
    else:
        country_code = pycountry.countries.get(name=country_name)
        if country_code:
            return country_code.alpha_2
        else:
            return None


def get_country_code_from_ean(ean: str) -> str | None:
    # print("input Country ean: " + ean)
    if "-" in ean:
        return None
    result = get_country_from_ean_v2(ean, GS1_list)
    if result:
        # print("output Country, Code:" + str(result))
        return result
    print("Country not found in the barcode range.")
    return None


def get_country_code_from_country_name_in_french_lang(name_in_french_lang: str) -> Optional[str]:
    if isinstance(name_in_french_lang, str):
        name_in_french_lang = name_in_french_lang.lower()
    else:
        return None

    if "ORIGINE C.E.E." in name_in_french_lang or "c.e.e" in name_in_french_lang or "origin eu" in name_in_french_lang or "origine ue" in name_in_french_lang or "UNION EUROPEENNE".lower() in name_in_french_lang:
        return "EU"
    elif "origine pays tiers" in name_in_french_lang or "hors ue" in name_in_french_lang:
        return None
    elif "ue et hors ue" in name_in_french_lang or "ue ou hors ue" in name_in_french_lang:
        return "EU"

    country_code = get_english_country_code(country_name=name_in_french_lang, langType=LangType.FR)
    return country_code

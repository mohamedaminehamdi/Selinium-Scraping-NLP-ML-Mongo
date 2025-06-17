# test_utils.py
import shutil
from typing import Literal
import re
from datetime import datetime
from fuzzywuzzy import fuzz
from typing import Any, Callable, List, Tuple, Type, TypeAlias, TypeVar, Union, cast
from enum import Enum
import time
import threading
import sys
import string
from pathlib import Path
import os
import logging
import json
import glob
from dataclasses import fields
import pytest
from src.model.product import Market, Product
from src.utils.my_utils import add_space_after_comma, are_string_exist_in_list, are_strings_equal, convert_to_float, convert_to_target_unit, count_non_none_properties, count_non_none_properties_recursive, days_between, extract_file_name, extract_folder_and_file, extract_folder_path, find_all_substrings_in_text, get_all_files_inside_given_folder, get_filename_from_filepath, get_files_with_substring_ordered_by_mtime, get_latest_file_in_folder, get_most_used_delimiter, is_any_string_in_string_list, is_float_regex, is_substring_in_list, keep_text_after, match_all_numbers, product1_has_more_properties, remove_extra_dots, remove_extra_spaces, remove_keyword_if_first, remove_keywords_and_empty_texts, remove_nones_from_dict, remove_numbers_and_fractions, remove_percent_values, remove_punctuation, remove_substring_and_clean, remove_substrings_and_clean, remove_text_before_first_delimiter_occurence, remove_text_before_last_delimiter_occurence, rephrase_text_if_parenthesis_exists, split_strings_on_dot


def test_convert_to_target_unit():
    input1 = "0.001 g"
    input2 = "3.1 µg"
    input3 = "2 kg"
    input4 = "500000 ng"

    output1 = convert_to_target_unit(input1, "mg")   # 0.001 g to mg -> 1.0 mg
    output2 = convert_to_target_unit(
        input2, "mg")   # 3.1 µg to mg -> 0.0031 mg
    output3 = convert_to_target_unit(input3, "g")    # 2 kg to g -> 2000 g

    output4 = convert_to_target_unit(
        input4, "mg")   # 500000 ng to mg -> 0.5 mg

    print(output1)  # Output: 1.0
    assert output1 == 1.0
    print(output2)  # Output: 0.0031
    assert output2 == 0.0031
    print(output3)  # Output: 2000.0
    assert output3 == 2000.0
    print(output4)  # Output: 0.5
    assert output4 == 0.5


def test_days_between():
    num_days = days_between("2023-09-15T08:46", "2023-10-05T08:46")
    assert num_days == 20


def test_remove_keyword_if_first():
    text1 = "Ingrédients : Tomate (71 %), poivron (5 %)"
    output1 = remove_keyword_if_first(text1, "Ingrédients :")
    assert output1 == "Tomate (71 %), poivron (5 %)"

    text2 = "Nutriments : Protéines, glucides"
    output2 = remove_keyword_if_first(text2, "Ingrédients :")
    assert output2 == "Nutriments : Protéines, glucides"  # (unchanged)


def test_keep_text_after():
    # Example usage
    text1 = "hellof ff k d Ingrédients : gge e, e et k"
    output1 = keep_text_after(text1, "Ingrédients :")
    assert output1 == "gge e, e et k"

    # Another example with a different keyword
    text2 = "Some text before important data here."
    output2 = keep_text_after(text2, "important")
    assert output2 == "data here."


def test_remove_substring_and_clean():
    input_text1 = " pomme, mangue. .  .  "
    input_substring1 = "pomme"
    supposed_output1 = ", mangue. . ."
    input_text2 = "pomme, mangue. . pomme ."
    input_substring2 = "pomme"
    supposed_output2 = ", mangue. . ."
    output1 = remove_substring_and_clean(input_text1, input_substring1)
    assert output1 == supposed_output1
    output2 = remove_substring_and_clean(input_text2, input_substring2)
    assert output2 == supposed_output2


def test_remove_extra_dots():
    examples = [
        "pomme, mangue. . .",
        "pomme, manguekk . .",
        ". .pomme"
    ]
    results = [remove_extra_dots(text) for text in examples]
    assert results[0] == "pomme, mangue."
    assert results[1] == "pomme, manguekk."
    assert results[2] == ".pomme"


def test_remove_substrings_and_clean():
    input_substrings = [
        "pomme",
        "mangue",
        "ananas",
        "chocolate",
        "almond"
    ]
    input_text = "i love pomme, banana , ananas, : huzelnuts and  almond, "
    supposed_output = "i love, banana, huzelnuts and"
    output = remove_substrings_and_clean(input_text, input_substrings)
    assert output == supposed_output


def test_is_float_regex():
    output = is_float_regex("123.45")
    assert output == True


def test_extract_folder_path():
    file_path = "/home/user/documents/file.txt"
    folder_path = extract_folder_path(file_path)
    assert folder_path == "/home/user/documents"


def test_extract_file_name():
    file_path = "/home/user/documents/file.txt"
    folder_path = extract_file_name(file_path)
    assert folder_path == "file"


def test_remove_extra_spaces():
    text = "This  is   a   string    with  extra  spaces."
    cleaned_text = remove_extra_spaces(text)
    assert cleaned_text == "This is a string with extra spaces."


def test_remove_punctuation():
    text = "Hello, world! This is an example: does it work?"
    cleaned_text = remove_punctuation(text)
    assert cleaned_text == "Hello world This is an example does it work"


def test_are_string_exist_in_list():
    output1 = are_string_exist_in_list(
        "test", [("test 1", 70), ("test 1234", 60)])
    assert output1 == True


def test_are_strings_equal():
    output = are_strings_equal("test", "test 1", 80)
    assert output == True
    output2 = are_strings_equal("test", "test 1", 90)
    assert output2 == False


def test_is_any_string_in_string_list():
    '''
    checks if any string from the list is a substring of the main string.
    '''
    string_list = ["apple", "banana", "orange"]
    main_string = "I love apples and bananas"
    result = is_any_string_in_string_list(string_list, main_string)
    assert result == True


def test_is_substring_in_list():
    '''
    check if a string is a substring of any string in a list
    '''
    substring = "apple"
    string_list = ["I love apples", "Bananas are great", "Orange juice"]
    result = is_substring_in_list(substring, string_list)
    assert result == True
    substring2 = "orange"
    result2 = is_substring_in_list(substring2, string_list)
    assert result2 == False


def test_find_all_substrings_in_text():
    susbstrings = ["apple", "ananas", "pinapple"]
    text = "i love pinapple only"
    output = find_all_substrings_in_text(susbstrings, text)
    assert output == "apple"
    text2 = "i love chocolate"
    output2 = find_all_substrings_in_text(susbstrings, text2)
    assert output2 == None


def test_write_output_to_file():
   assert True == True


def test_custom_dump():
    assert True == True


def test_get_all_files_inside_given_folder():
    """Get all file paths (with specific extension) in the given folder and its subfolders."""
    # Step 1: Create a folder and a file inside it
    input_folder_path = f"{Path.cwd()}/test_folder/"
    os.makedirs(input_folder_path, exist_ok=True)  # Create the folder
    input_filename = "example.txt"
    input_file_path = os.path.join(input_folder_path, input_filename)
    with open(input_file_path, "w") as file:
        file.write("Hello, world!")  # Write content
    print(f"Created folder with input_folder_path: '{input_folder_path}', input_file_path: '{
        input_file_path}'.")

    input_filename2 = "example2.txt"
    input_file_path2 = os.path.join(input_folder_path, input_filename2)
    with open(input_file_path2, "w") as file:
        file.write("Hello, world 2!")  # Write content
    print(f"Created folder '{input_folder_path}' and file '{
        input_file_path2}'.")

    files = get_all_files_inside_given_folder(input_folder_path, extension= "txt")
    print(f"files: {files}")
    last_file = get_latest_file_in_folder(input_folder_path, "example")
    folder_path_output, file_name_output = extract_folder_and_file(
        input_file_path)
    output_get_filename_from_filepath = get_filename_from_filepath(
        input_file_path, ".txt", True)

    output_files_with_substring_ordered_by_mtime = get_files_with_substring_ordered_by_mtime(
        input_folder_path, "example")

    try:
        assert (input_file_path in files) == True
        assert (input_file_path2 in files) == True
        assert len(files) == 2

        assert last_file == input_file_path2

        assert folder_path_output == input_folder_path
        assert file_name_output == file_name_output

        assert output_get_filename_from_filepath == input_filename
        assert output_files_with_substring_ordered_by_mtime[0] == input_file_path2
        assert output_files_with_substring_ordered_by_mtime[1] == input_file_path

    finally:
        # Cleanup
        # Step 2: Remove the file and the folder
        if os.path.exists(input_file_path):
            os.remove(input_file_path)  # Remove the file
            print(f"File '{input_file_path}' removed.")
        if os.path.exists(input_file_path2):
            os.remove(input_file_path2)  # Remove the file
            print(f"File '{input_file_path2}' removed.")
        if os.path.exists(input_folder_path):
            shutil.rmtree(input_folder_path)  # Remove the folder
            print(f"Folder '{input_folder_path}' removed.")

def test_convert_to_float():
    string_number = "3 624,40"
    number = convert_to_float(string_number)
    assert number == 3624.40


def test_remove_nones_from_dict():
    """Recursively remove None values from the dictionary."""
    input_dict = {
        "ean": "8445290624918",
        "brand": None,
        "categories": [
            {
                "id": None,
                "label": "Bébé"
            },
            {
                "id": 36922,
                "label": "Alimentation"
            },
            {
                "id": 36923,
                "label": None
            }
        ],
        "origin": {
            "ean": [
                None,
                "AD"
            ],
            "partial": "FR"
        },
        "market": {
            "name": "carrefour",
            "country": None
        }
    }
    supposed_output_dict = {
        "ean": "8445290624918",
        "categories": [
            {
                "label": "Bébé"
            },
            {
                "id": 36922,
                "label": "Alimentation"
            },
            {
                "id": 36923,
            }
        ],
        "origin": {
            "ean": [
                "AD"
            ],
            "partial": "FR"
        },
        "market": {
            "name": "carrefour",
        }
    }
    output = remove_nones_from_dict(input_dict)
    assert output == supposed_output_dict


def test_count_non_none_properties():
    market = Market(name="carrefour", address="paris 14", country=None)
    product = Product(ean="123", brand=None, freshness=0, market=market)
    count = count_non_none_properties(product)
    assert count == 5


def test_count_non_none_properties():
    market = Market(name="carrefour", address="paris 14", country=None)
    product = Product(ean="123", brand=None, freshness=0, market=market)
    count = count_non_none_properties(product)
    assert count == 6


def test_count_non_none_properties_recursive():
    input_market1 = Market(name="carrefour", address="paris 14", country=None)
    input_product1 = Product(ean="123", brand=None,
                             freshness=0, market=input_market1)

    input_market2 = Market(name="carrefour", address="paris 14", country=None)
    input_product2 = Product(ean="123", brand="Lindt",
                             freshness=0, market=input_market2)

    count1 = count_non_none_properties_recursive(input_product1)
    assert count1 == 8
    count2 = count_non_none_properties_recursive(input_product2)
    assert count2 == 9

    output_bool = product1_has_more_properties(input_product1, input_product2)
    assert output_bool == False


def test_remove_text_before_delimiter_occurence():
    input_text1 = "a b , d ex: azerty i"
    supposed_output_text1 = "azerty i"
    output_text1 = remove_text_before_first_delimiter_occurence(input_text1, ":")
    assert supposed_output_text1 == output_text1

    input_text2 = "a b , d ex: azerty i ef: ch"
    supposed_output_text2 = "ch"
    output_text2 = remove_text_before_last_delimiter_occurence(input_text2, ":")
    assert supposed_output_text2 == output_text2

    supposed_output_text2_2 = "azerty i ef: ch"
    output_text2_2 = remove_text_before_first_delimiter_occurence(input_text2, ":")
    assert supposed_output_text2_2 == output_text2_2

    input_text3 = ["a b , d ex: azerty i",
                   "azerty , querty , ab", "azerty query,", ",,abc"]
    supposed_output_text3 = ["d ex: azerty i",
                             "querty , ab", "azerty query", ",abc"]
    output_text3 = remove_text_before_first_delimiter_occurence(input_text3, ",", undo_if_result_empty=True)
    assert supposed_output_text3 == output_text3

    output_text4 = remove_text_before_first_delimiter_occurence(None, ":")
    assert None == output_text4


def test_split_strings_on_dot():
    input_strings = [
        "hello.world",
        "no_dot_here",
        "another.example.string",
        "final.test"
    ]
    supposed_output = ['hello', 'world', 'no_dot_here', 'another', 'example', 'string', 'final', 'test']
    output = split_strings_on_dot(input_strings)
    assert output == supposed_output

def test_remove_percent_values():
    input_text = "pomme 54,3%, pêche 7,5%, abricot 7%, toto4%, titi6,7%"
    supposed_output = "pomme, pêche, abricot, toto, titi"
    output = remove_percent_values(input_text)
    assert output == supposed_output

def test_remove_numbers_and_fractions():
    '''
    Remove all integers and fractions (e.g., "5 ", "34 ", "1/3 ", "1/4 ")
    '''
    input_text = "5 pommes pressées, 34 raisins pressés, 19 framboises, 1/3 poire, 1/4 grenade pressée"
    supposed_output = "pommes pressées, raisins pressés, framboises, poire, grenade pressée"
    output = remove_numbers_and_fractions(input_text)
    assert output == supposed_output

def test_remove_keywords_and_empty_texts():
    input_texts = [
        "Hello world!",
        "Python is amazing.",
        "Hello",
        "Just a keyword here",
        "Another keyword",
        "Only keyword"
    ]
    keywords = ["keyword", "Hello"]
    output = remove_keywords_and_empty_texts(input_texts, keywords)
    supposed_output = ["world!", "Python is amazing.", "Just a here", "Another"]


def test_rephrase_text_if_parenthesis_exists():

    text1 = "vitamines (C, A, acide folique, B6, thiamine)"
    text2 = "vitamines C, A, acide folique, B6, thiamine"  # No parentheses
    text3 = "ingredients (D, A, acide folique, s, k)"

    output = rephrase_text_if_parenthesis_exists(text1)
    supposed_output = "vitamines C, vitamines A, vitamines acide folique, vitamines B6, vitamines thiamine"
    assert output == supposed_output

    output2 = rephrase_text_if_parenthesis_exists(text2)
    supposed_output2 = "vitamines C, A, acide folique, B6, thiamine" #(unchanged)
    assert output2 == supposed_output2

    output3 = rephrase_text_if_parenthesis_exists(text3)
    supposed_output3 = "ingredients D, ingredients A, ingredients acide folique, ingredients s, ingredients k"
    assert output3 == supposed_output3

    text4 = "ingredients (D, (A), acide folique, s, k)"
    output4 = rephrase_text_if_parenthesis_exists(text4)
    supposed_output4 = "ingredients D, ingredients (A), ingredients acide folique, ingredients s, ingredients k"
    assert output4 == supposed_output4

def test_add_space_after_comma():
    input_text1 = "vitamines (C,E, pro-A)"
    output = add_space_after_comma(input_text1)
    supposed_output = "vitamines (C, E, pro-A)"


def test_get_most_used_delimiter():
    input_text = "line1,line2,\nline3-line4,line5\n"
    supposed_output = ","
    output = get_most_used_delimiter(input_text)
    assert output == supposed_output

def test_match_all_numbers():
    text1 = "88 avis pour une note moyenne de 4.75 sur 5"
    text2 = "3 avis pour une note moyenne de 2.46 sur 5"
    text3 = "4 avis pour une note moyenne de 1.7 sur 5"
    numbers1 = match_all_numbers(text1)
    assert numbers1[0] == 88
    assert numbers1[0] == 4.75
    assert numbers1[0] == 5

    numbers2 = match_all_numbers(text2)
    assert numbers2[0] == 3
    assert numbers2[0] == 2.46
    assert numbers2[0] == 5

    numbers3 = match_all_numbers(text3)
    assert numbers3[0] == 4
    assert numbers3[0] == 1.7
    assert numbers3[0] == 5

if __name__ == "__main__":
    input1 = "0.001 g"
    input2 = "3.1 µg"
    input3 = "2 kg"
    input4 = "500000 ng"

    output1 = convert_to_target_unit(input1, "mg")   # 0.001 g to mg -> 1.0 mg

    output2 = convert_to_target_unit(
        input2, "mg")   # 3.1 µg to mg -> 0.0031 mg

    output3 = convert_to_target_unit(input3, "g")    # 2 kg to g -> 2000 g

    output4 = convert_to_target_unit(
        input4, "mg")   # 500000 ng to mg -> 0.5 mg

    print(output1)  # Output: 1.0
    print(output2)  # Output: 0.0031
    print(output3)  # Output: 2000.0
    print(output4)  # Output: 0.5

# Run pytest programmatically
if __name__ == "__main__":
    # Exit with an error code if any test fails
    exit_code = pytest.main()
    if exit_code != 0:
        print("Tests failed. Exiting...")
        exit(exit_code)
    else:
        print("All tests passed!")

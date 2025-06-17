import json
import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from src.utils.my_utils import get_most_used_delimiter, remove_text_before_delimiter, split_strings_on_dot

load_dotenv()  # Loads environment variables from .env file


# Api_Key
api_key = os.getenv('OPENAI_API_KEY')
print(f"api_key: {api_key}")
client = OpenAI(api_key=api_key)

# Load JSON file
"""with open('ingredient.json', 'r', encoding='utf-8') as f:
    data = json.load(f)"""

# Function to call OpenAI and clean ingredients


def clean_ingredients(ingredients_text):
    if not isinstance(ingredients_text, str):
        return None
    prompt = (
        f"From text, Extract all base ingredient names only"
        f" and translate them to english."
        # f"Translate any ingredient names into English."
        f". Remove all non-alphabetic characters except commas. "
        f"Retain herbs and vitamins as valid ingredients. "
        # f"Include ingredients mentioned in allergen warnings (e.g., 'May contain traces of milk') but only return the ingredient name without any explanation. "
        # f"Identify and include general ingredient categories (e.g., 'chicken') if no specific ingredients are present. "
        # f"Group similar ingredients under a single base name."
        f"remove redundancy, descriptions and explanation from response."
        f"do not regroup ingredients."
        f"Rephrase any text within parentheses into a more natural form instead of excluding it."
        f"translate response to english."
        f"text: {ingredients_text}."
    )
    print(f"prompt:{prompt}")

    response = client.chat.completions.create(model="gpt-4o-mini",  # Using gpt-4o-mini model
                                              messages=[
                                                  {"role": "user", "content": prompt}
                                              ],
                                              max_tokens=256)

    # Retrieve the response and clean up spaces or other unnecessary characters
    cleaned_text = response.choices[0].message.content.strip().lower()
    delimiter = get_most_used_delimiter(cleaned_text)
    print(f"cleaned text: {cleaned_text}")
    ingredients_list = [ingredient.strip() for ingredient in cleaned_text.split(delimiter) if ingredient.strip()]
    ingredients_list = remove_text_before_delimiter(ingredients_list, ":")
    ingredients_list = split_strings_on_dot(strings=ingredients_list)        
    return ingredients_list if isinstance(ingredients_list, list) else  [ingredients_list]

import re

# Loop through JSON elements and clean ingredients
# Function to process a single JSON file

def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Loop through JSON elements and clean ingredients
    for product in json_data:
        for evolution in product.get('evolutions', []):
            ingredients = evolution.get('ingredients')
            if ingredients:
                # Extract and clean the ingredients
                cleaned_ingredients_list = clean_ingredients(ingredients)
                # Assign the cleaned ingredients back to the 'ingredients' key as a list
                evolution['ingredients'] = cleaned_ingredients_list

                # Format the output as a string in the desired format
                formatted_ingredients = f"[{', '.join(cleaned_ingredients_list)}]"
                print(f"Ingredients for {product['ean']} : {formatted_ingredients}")

    # Save cleaned data back to a new JSON file with 'cleaning' appended
    base_name = os.path.splitext(file_path)[0]  # Get the file name without extension
    cleaned_file_path = f"{base_name}_cleaning.json"
    with open(cleaned_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def replace_text_with_first_matching_keyword(text: str, keywords: List[str]) -> str:
    if not isinstance(text, str) or not isinstance(keywords, list):
        return text
    # Loop through each keyword and check if it exists in the text
    for keyword in keywords:
        if keyword in text:
            # Return the first matching keyword found in the text
            return keyword
    # If no keywords are found, return the original text
    return text
    # Example usage
    text1 = "This is a sample text containing the word Python."
    keywords = ["Java", "Python", "JavaScript"]
    print(replace_text_with_first_matching_keyword(text1, keywords))  # Expected output: "Python"

    text2 = "This is a sample text without any matching keyword."
    print(replace_text_with_first_matching_keyword(text2, keywords))  # Expected output: "This is a sample text without any matching keyword."

# Function to process all JSON files in a directory


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('with_details.json'):
                file_path = os.path.join(root, file_name)
                process_json_file(file_path)


# Replace with the path to your directory containing the JSON files
directory_path = 'products'
process_directory(directory_path)

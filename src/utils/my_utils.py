#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Literal
import re
from datetime import datetime
from dataclasses import fields
import glob
import json
import logging
import os
from pathlib import Path
import string
import sys
import threading
import time
from enum import Enum
from typing import Any, Callable, List, Tuple, Type, TypeAlias, TypeVar, Union, cast

from fuzzywuzzy import fuzz

sys.path.append('./')


def all_attrs_are_none(obj) -> bool:
    '''
    # Check if all attributes are None
    '''
    if not obj:
        return True
    return all(value is None for value in vars(obj).values())


def all_attrs_are_none_or_zero(obj) -> bool:
    '''
    Check if all attributes of the object are either None or 0.
    '''
    # If obj is None itself, return True
    if obj is None:
        return True

    # Use vars() to get the dictionary of attributes
    return all(value is None or value == 0 for value in vars(obj).values())


def days_between(date_str1, date_str2, date_format="%Y-%m-%dT%H:%M") -> int | None:
    if not date_str1 or not date_str2:
        return None
    # Parse the date strings into datetime objects
    date1 = datetime.strptime(date_str1, date_format)
    date2 = datetime.strptime(date_str2, date_format)
    # Calculate the difference between the two dates, Get the number of days
    delta = (date2 - date1).days
    return delta
    # Example usage
    num_days = days_between("2022-01-15T08:46", "2023-09-10T08:46")
    print(num_days)  # Output: 20


def remove_keyword_if_first(text, keyword):
    # Check if the text starts with the keyword followed by a space or any non-word character
    if text.startswith(keyword):
        # Remove the keyword and strip any additional leading whitespace
        return text[len(keyword):].lstrip()
    return text
    # Example usage
    text1 = "Ingrédients : Tomate (71 %), poivron (5 %)"
    # Expected output: "Tomate (71 %), poivron (5 %)"
    print(remove_keyword_if_first(text1, "Ingrédients :"))

    text2 = "Nutriments : Protéines, glucides"
    # Expected output: "Nutriments : Protéines, glucides" (unchanged)
    print(remove_keyword_if_first(text2, "Ingrédients :"))


def keep_text_after(text, keyword):
    # Split the text on the keyword and return everything after the first occurrence of the keyword
    parts = text.split(keyword, 1)
    return parts[1].strip() if len(parts) > 1 else text

    # Example usage
    text1 = "hellof ff k d Ingrédients : gge e, e et k"
    print(keep_text_after(text1, "Ingrédients :"))  # Output: "gge e, e et k"

    # Another example with a different keyword
    text2 = "Some text before important data here."
    print(keep_text_after(text2, "important"))  # Output: "data here."


def remove_substring_and_clean(text: str, substring: str) -> str:
    if not isinstance(text, str) or not isinstance(substring, str):
        return text
    # Step 1: Remove the substring case-insensitively
    result = re.sub(re.escape(substring), '', text, flags=re.IGNORECASE)
    # Step 2: Remove extra spaces by splitting and joining
    result = remove_extra_spaces(result)
    return result


def remove_extra_dots(text):
    # Replace multiple dots (with or without spaces in between) with a single dot
    cleaned_text = re.sub(r'(\s*\.\s*)+', '.', text)
    # Strip any extra spaces around the result
    return cleaned_text.strip()
    # Example usage
    examples = [
        "pomme, mangue. . .",
        "pomme, manguekk . .",
        ". .pomme"
    ]

    # Applying the function to each example
    results = [remove_extra_dots(text) for text in examples]
    print(results)


def remove_substrings_and_clean(text: str, substrings: List[str]) -> str | None:
    if not isinstance(text, str) or not isinstance(substrings, list):
        return None
    # Sort the list by length in descending order
    substrings = sorted(substrings, key=len, reverse=True)
    for substring in substrings:
        text = re.sub(re.escape(substring), '', text, flags=re.IGNORECASE)
    text = text.replace(", : ", ", ").replace(
        " , ", ", ").replace(", ,", ",").replace(" ,", ",")
    text = remove_extra_spaces(text).rstrip(',')
    return text


def is_float_regex(value: str) -> bool:
    # Regular expression to match float numbers
    float_regex = r'^-?\d+(\.\d+)?$'
    return bool(re.match(float_regex, value))
    # Example usage
    print(is_float_regex("123.45"))  # Output: True


def extract_folder_path(file_path: str | None) -> str | None:
    if not isinstance(file_path, str):
        return None
    # Extract directory path using os.path.dirname()
    folder_path = os.path.dirname(file_path)
    return folder_path
    # Example usage:
    file_path = "/home/user/documents/file.txt"
    folder_path = extract_folder_path(file_path)
    print("Folder Path:", folder_path)


def extract_file_name(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    return file_name


def convert_to_target_unit(input_str: any, target_unit: Literal['kg', 'g', 'mg', 'µg', 'ng']) -> float | None:
    if not input_str:
        return None
    print(f'convert_to_target_unit text: {input_str}, type:{type(input_str)}')
    if isinstance(input_str, (int, float)):
        return input_str
    print(f'isdigit():{input_str.isdigit()}')
    if isinstance(input_str, str) and (input_str.isdigit() or is_float_regex(input_str)):
        value = round(float(input_str), 4)
        final_value = int(value) if value.is_integer() else value
        return final_value
    elif not isinstance(input_str, str):
        return None

    # Conversion factors to milligrams (mg)
    conversion_to_mg = {
        'kg': 1_000_000,  # kilograms to milligrams
        'g': 1000,        # grams to milligrams
        'mg': 1,          # milligrams to milligrams
        'µg': 0.001,      # micrograms to milligrams
        'ng': 0.000001,    # nanograms to milligrams
        'ml': 1000,       # milliliters treated as grams to milligrams
        'l': 1_000_000    # liters treated as kilograms to milligrams
    }

    # Conversion factors from milligrams (mg) to the target unit
    conversion_from_mg = {
        'kg': 1 / 1_000_000,  # milligrams to kilograms
        'g': 1 / 1000,        # milligrams to grams
        'mg': 1,              # milligrams to milligrams
        'µg': 1000,           # milligrams to micrograms
        'ng': 1_000_000,       # milligrams to nanograms
        'ml': 1 / 1000,       # milligrams to milliliters (same as grams)
        'l': 1 / 1_000_000    # milligrams to liters (same as kilograms)
    }

    # Split the input string into value and unit
    value_str, unit = input_str.split()

    # Convert the value to a float
    value = float(value_str)

    # Convert the input value to milligrams (mg)
    if unit in conversion_to_mg:
        value_in_mg = value * conversion_to_mg[unit]
    else:
        print(f"Unsupported unit in input: {unit}")
        return convert_to_float(input_str)
        raise ValueError(f"Unsupported unit in input: {unit}")

    # Convert from milligrams (mg) to the target unit
    final_value1 = value_in_mg * conversion_from_mg[target_unit]
    final_value2 = round(final_value1, 4)
    final_value = int(
        final_value2) if final_value2 and final_value2.is_integer() else final_value2
    print(f"input_str: {input_str}, value_str: {value_str}, current_unit: {unit}, target_unit: {
          target_unit}, value_in_mg: {value_in_mg}, final_value: {final_value}, final_value1: {final_value1}, final_value2: {final_value2}")
    return final_value

    # Test examples
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


def remove_extra_spaces(text) -> str:
    '''
    # Example usage
    text = "This  is   a   string    with  extra  spaces."
    cleaned_text = remove_extra_spaces(text)
    print(cleaned_text)
    '''
    # Split the string by whitespace and join it back with a single space
    return ' '.join(text.split())


def remove_punctuation(text):
    '''
    # Example usage
    text = "Hello, world! This is an example: does it work?"
    cleaned_text = remove_punctuation(text)
    print(cleaned_text)
    '''
    # Create a translation table that maps each punctuation character to None
    translator = str.maketrans('', '', string.punctuation)

    # Use the translation table to remove punctuation from the text
    return text.translate(translator)


def are_string_exist_in_list(str1: str, strings: List[Tuple[str, int]]) -> bool | None:
    if not isinstance(str1, str) or not isinstance(strings, list) or not all(isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str) and isinstance(item[1], int) for item in strings):
        # raise TypeError("Fatal error: parameters of are_strings_exist_in_list must be of correct types.")
        return None

    for str2, threshold in strings:
        res = are_strings_equal(str1, str2, threshold)
        if res:
            return True
    return False


def are_strings_equal(str1: str, str2: str, threshold=80) -> bool:
    # Calculate the similarity ratio between the two strings
    if not isinstance(str1, str) or not isinstance(str2, str):
        # raise TypeError("Fatal error: parameters of are_strings_equal must be of correct types.")
        return None
    str1 = remove_extra_spaces(str1.lower())
    str2 = remove_extra_spaces(str2.lower())

    str1 = remove_punctuation(str1)
    str2 = remove_punctuation(str2)

    similarity_ratio = fuzz.ratio(str1, str2)
    print(f"similarity_ratio: {similarity_ratio} for: ({str1}) VS ({str2})")

    # Check if the similarity ratio meets or exceeds the threshold
    return similarity_ratio >= threshold


try:
    from selenium import webdriver

    # The Keys class provide keys in the keyboard like RETURN, F1, ALT etc
    from selenium.webdriver import ActionChains, Keys
    from selenium.webdriver.chromium.options import ChromiumOptions
    from selenium.webdriver.support import expected_conditions
except ImportError:
    logging.critical("Selenium module is not installed2...Exiting program.")
    exit(1)


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def is_any_string_in_string_list(string_list: List[str], main_string: str) -> bool | None:
    '''
    checks if any string from the list is a substring of the main string.
    '''
    if isinstance(main_string, str):
        main_string = main_string.lower()
    else:
        return None

    return any(s.lower() in main_string for s in string_list)
    # Example usage:
    string_list = ["apple", "banana", "orange"]
    main_string = "I love apples and bananas"
    result = is_any_string_in_string(string_list, main_string)
    print(result)  # Output: True


def is_substring_in_list(substring, string_list):
    '''
    check if a string is a substring of any string in a list
    '''
    for s in string_list:
        if substring in s:
            return True
    return False
    # Example usage:
    substring = "apple"
    string_list = ["I love apples", "Bananas are great", "Orange juice"]
    result = is_substring_in_list(substring, string_list)
    print(result)  # Output: True


def find_all_substrings_in_text(substrings: List[str], text: str) -> str | None:
    if text is None:
        return None
    text_upper = text.upper()
    for substring in substrings:
        if substring.upper() in text_upper:
            return substring
    return None


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def xstr(s):
    NoneType = type(None)
    if s is None or not s or s is None or isinstance(s, NoneType):
        return ''
    if isinstance(s, list):
        # return ', '.join(s)
        return [xstr(x) for x in s]
    else:
        return str(s)


def check_if_url_exists(url):
    import httplib2
    try:
        h = httplib2.Http()
        resp = h.request(url, 'HEAD')
        if int(resp[0]['status']) < 400:
            return True
        return False
    except:
        return False


def write_output_to_file(data, folder_path='../market_logs', file_name=None, path_includes_in_file_name=False, add_file_date=True, include_seconds_in_date=True, extension=".log"):
    if not file_name:
        import inspect
        stack = inspect.stack()
        the_class = stack[1][0].f_locals["self"].__class__.__name__
        # the_method = stack[1][0].f_code.co_name
        file_name = "{}".format(the_class)
        # %y : Renvoie l'année sur deux chiffres (par exemple, 24 pour 2024).
        # %Y : Renvoie l'année sur quatre chiffres (par exemple, 2024).
    if add_file_date:
        timestr = ''
        timestr = time.strftime('%y_%m_%d_%H_%M_%S', time.localtime(time.time(
        ))) if include_seconds_in_date else time.strftime('%y_%m_%d_%H_%M', time.localtime(time.time()))
        file_name = file_name + "_" + timestr

    file_name = file_name + extension
    if not path_includes_in_file_name:
        path = folder_path

        def PATH(p):
            return os.path.abspath(os.path.join(os.path.dirname(__file__), p))

        if not (os.path.isdir(PATH(path))):
            os.mkdir(PATH(path))
            if not (os.access(PATH(path), os.W_OK)):
                # print('Path {0} cannot be written.'.format(PATH('../logs')))
                print('Path {' + path + '} cannot be written.')

        filename = PATH(os.path.join(path, file_name))
    else:
        filename = file_name

    # filemode = 'a'
    file = open(filename, "w+", encoding='utf-8')
    # file.write(data)
    # Check data type and write accordingly
    if isinstance(data, list):
        # Handle list (assuming elements can be converted to strings)
        for element in data:
            # Write each element with a newline
            file.write(str(element) + "\n")

    else:
        # Assuming data is the JSON string
        file.write(data)  # Write the JSON string
    file.close


starttime = time.time()


class repeatExecution:
    def __init__(self):
        while True:
            print("tick")
            time.sleep(5.0 - ((time.time() - starttime) % 5.0))


class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        repeat = self.function(*self.args, **self.kwargs)
        print("repeat:" + str(repeat))
        if not repeat or repeat is not None:
            print("Then end of running")
            self.stop()

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(
                self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class DriverConfig:
    class DriverType(Enum):
        CHROME = 'Tools/Drivers/chromedriver'
        FIREFOX = 'Tools/Drivers/geckodriver'

    @staticmethod
    def getDriver(driverType: DriverType):
        if driverType is DriverConfig.DriverType.CHROME:
            options = webdriver.ChromeOptions()
            prefs = {
                'profile.default_content_setting_values': {
                    # 'cookies': 2,
                    # 'javascript': 2,
                    'images': 2,
                    'plugins': 2,
                    'popups': 2,
                    'geolocation': 2,
                    'notifications': 2,
                    'auto_select_certificate': 2,
                    'fullscreen': 2,
                    'mouselock': 2,
                    'mixed_script': 2,
                    'media_stream': 2,
                    'media_stream_mic': 2,
                    'media_stream_camera': 2,
                    'protocol_handlers': 2,
                    'ppapi_broker': 2,
                    'automatic_downloads': 2,
                    'midi_sysex': 2,
                    'push_messaging': 2,
                    'ssl_cert_decisions': 2,
                    'metro_switch_to_desktop': 2,
                    'protected_media_identifier': 2,
                    'app_banner': 2,
                    'site_engagement': 2,
                    'durable_storage': 2
                }
            }
            options.add_argument(
                "--disable-blink-features=AutomationControlled")
            options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

            # keep_browser_open
            options.add_experimental_option("detach", False)
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--incognito")
            options.add_argument("--disable-search-engine-choice-screen")

            # options.add_experimental_option('excludeSwitches', ['enable-logging'])

            options.add_argument("--disable-gpu")

            # window setup:
            options.add_argument("start-maximized")
            # options.add_argument('--width=1500')
            # options.add_argument('--height=1500')
            # chromeOptions.add_argument("--start-fullscreen");
            # chromeOptions.add_argument("--window-size=1920,1080");#this will set the browser to the MAC maximum size

            # options.add_argument("disable-infobars")
            #options.add_argument('--headless')
            options.add_argument("--disable-default-apps")
            # options.add_argument("--enable-precise-memory-info")
            # options.add_argument('--log-level=3')

            # disable extension, popup blocking and notification
            options.add_argument("--disable-extensions")
            # options.add_argument("--disable-popup-blocking")
            # options.add_argument("--disable-notifications")

            # options.add_argument("--hide-scrollbars")
            # options.add_argument("--disable-application-cache")

            # chrome_options.add_argument('--kiosk')#kiosk mode
            # options.add_argument("--disable-webgl")
            options.add_argument("--disable-xss-auditor")
            # options.add_argument("--disable-web-security")
            # options.add_argument("--allow-running-insecure-content")
            # options.add_argument("--no-sandbox")
            # options.add_argument("--disable-setuid-sandbox")
            # options.add_argument('--disable-dev-shm-usage')
            # options.add_argument("no-first-run")
            # options.add_argument('mobileEmulation')

            # options.add_argument("--host-resolver-rules=MAP www.google-analytics.com 127.0.0.1")
            # options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
            driver = webdriver.Chrome(options=options)

            driver.execute_script("document.body.style.zoom='50%'")
            # options.add_argument('--width=1500')
            # options.add_argument('--height=1500')
            # driver.set_window_size(1024, 600)
            # chromeOptions.add_argument("--start-fullscreen");
            # chromeOptions.add_argument("--window-size=1920,1080");#this will set the browser to the MAC maximum size

            # driver.get('chrome://settings/')
            # driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.85);')
            # driver.set_window_position(-10000000, 0)#move chrome away from view

            # driver.execute_script("document.body.style.zoom='50%'")
            # driver.get('chrome://settings/')
            ActionChains(driver).key_down(
                Keys.ADD).key_down(Keys.ADD).perform()

        elif driverType is DriverConfig.DriverType.FIREFOX:
            options = webdriver.FirefoxOptions()

            # options.add_argument("--headless")
            options.add_argument('--width=1500')
            options.add_argument('--height=1500')
            options.set_preference('permissions.default.image', 2)

            # webdriver.Firefox(executable_path=DriverConfig.DriverType.FIREFOX.value)
            driver = webdriver.Firefox(options=options, keep_alive=False)
            driver.execute_script("document.body.style.zoom='30%'")
            driver.execute_script(
                'document.body.style.MozTransform = "scale(1.50)";')

        return driver

    @staticmethod
    def quitChromeIfChromeDriverIsKilled(options: ChromiumOptions, state: bool):
        # If false, Chrome will be quit when ChromeDriver is killed, regardless of whether the session is quit.
        # If true, Chrome will only be quit if the session is quit (or closed). Note, if true, and the session is not quit,
        # ChromeDriver cannot clean up the temporary user data directory that the running Chrome instance is using.
        options2 = options.add_experimental_option("detach", state)
        return options2

    @staticmethod
    def test_log_to_file(log_path):
        service = webdriver.ChromeService(log_output=log_path)

        driver = webdriver.Chrome(service=service)

        with open(log_path, 'r') as fp:
            assert "Starting ChromeDriver" in fp.readline()

        driver.quit()


def custom_dump(objs: any):
    json_object = json.dumps(objs,
                             default=lambda o: dict(
                                 (key, value) for key, value in o.__dict__.items() if value),
                             indent=4,
                             allow_nan=False,
                             ensure_ascii=False)
    return json_object


def get_all_files_inside_given_folder(folder_path: str, extension="json"):
    """Get all file paths (with specific extension) in the given folder and its subfolders."""
    pattern = os.path.join(folder_path, '**', '*.'+extension)
    json_files = glob.glob(pattern, recursive=True)
    return json_files
    # Example usage:
    folder_path = '/path/to/your/folder'  # Replace with your folder path
    json_files = get_all_files_inside_given_folder(folder_path)
    for file_path in json_files:
        print(file_path)


def get_latest_file_in_folder(folder_path: str | None, file_name_prefix: str | None, during_last_x_days: int = 10):
    '''
    # Example usage:
    folder_path = "/path/to/your/folder"

    latest_file = get_newest_file(folder_path)
    '''
    print("folder_path:" + str(folder_path) +
          ", file_name_suffix: " + str(file_name_prefix))
    if not isinstance(folder_path, str) or not isinstance(file_name_prefix, str):
        return None

    # Get the current time
    current_time = time.time()

    # Calculate the time limit in seconds (x days)
    time_limit = current_time - \
        (during_last_x_days * 86400)  # 86400 seconds in a day

    # Use glob to find all files in the folder that start with "abc"
    files = glob.glob(os.path.join(folder_path, file_name_prefix + "*"))
    print(f"all files in the folder: {files}")
    # Filter files based on the modification time within the last x days
    recent_files = [f for f in files if os.path.getmtime(f) >= time_limit]

    if not recent_files:
        print("no recent file found!")
        return None

    # Sort files by modification time (newest first)
    latest_file = max(recent_files, key=os.path.getmtime)
    print("latest file:", latest_file)
    return latest_file


def extract_folder_and_file(path: str | None) -> tuple | None:
    print("extract_folder_and_file from path: " + str(path))
    if not isinstance(path, str):
        return None, None
    # Get folder path and add the separator at the end
    folder_path = os.path.dirname(path) + os.path.sep
    file_name = os.path.basename(path)  # Get file name
    print("Folder path: " + str(folder_path) +
          ", File name: " + str(file_name))
    return folder_path, file_name
    # Example usage:
    path = "src/countries/france/carrefour/robots/products/viandes_poissons/boucherie_with_details_24_03_10_01_23.json"
    folder_path, file_name = extract_folder_and_file(path)


def convert_to_float(value) -> float | None:
    if value and not isinstance(value, str):
        return value
    elif not value:
        return None
    # Supprimer tout ce qui n'est pas un chiffre, une virgule ou un point
    cleaned_value = re.sub(r'[^\d,\.]', '', value)
    # Remplacer la virgule par un point pour le séparateur décimal
    if ',' in cleaned_value and '.' not in cleaned_value:
        cleaned_value = cleaned_value.replace(',', '.')
        res: float | None = None
    try:
        res = float(cleaned_value)
        print(f"res here:{res}")
        res = int(res) if res and res.is_integer() else res
        print(f"res here2:{res}")
        return res
    except ValueError:
        print("error while running convert_to_float: " + str(value))
        return None
    string_number = "3 624,40"
    number = convert_to_float(string_number)
    print(number)
    
def get_filename_from_filepath(filepath, extension=".json", return_filename_with_extension=False) -> str:
    file_path = Path(filepath)  # Example file path

    file_name = file_path.name  # Get the file name with extension
    file_stem = file_path.stem  # Get the file name without extension
    file_extension = file_path.suffix  # Get the file extension
    print(f"file_name: {file_name}, file_stem: {file_stem}, file_extension: {file_extension}")
    if return_filename_with_extension:
        return file_name
    else:
        return file_stem
    
def print_colored(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "black": "\033[90m",
        "reset": "\033[0m"  # Reset to default color
    }
    
    color_code = colors.get(color.lower(), colors["reset"])  # Default to reset if color not found
    print(f"{color_code}{text}{colors['reset']}")  # Print with color and reset

    # Example Usage:
    # print_colored("This is a red message!", "red")
    # print_colored("This is a blue message!", "blue")
    # print_colored("This is a yellow message!", "yellow")
    # print_colored("This is a green message!", "green")
    # print_colored("This is an invalid color!", "unknown")  # Defaults to normal text


def get_files_with_substring_ordered_by_mtime(folder_path, substring: str | None, return_full_path=True) -> List[str]:
    # List to hold tuples of (file_name, modification_time)
    matching_files = []

    # Loop through all files in the directory
    for file_name in os.listdir(folder_path):
        # Full path to the file
        full_path = os.path.join(folder_path, file_name)

        # Check if the current item is a file and if the substring is in the file name
        if os.path.isfile(full_path) and (substring in file_name if substring else True):
            # Append file name and its modification time to the list
            matching_files.append((file_name, os.path.getmtime(full_path)))

    # Sort the files by modification time (most recent first)
    matching_files.sort(key=lambda x: x[1], reverse=True)

    # Return only the file names, sorted
    return [file_name if not return_full_path else os.path.join(folder_path, file_name) for file_name, _ in matching_files]
    # Example usage:
    folder_path = "/path/to/your/folder"
    substring = "details"
    matching_files = get_files_with_substring_ordered_by_mtime(
        folder_path, substring)
    print("Matching files ordered by most recent:", matching_files)


def remove_nones_from_dict(data: any):
    """Recursively remove None values from the dictionary."""
    if isinstance(data, dict):
        # Recursively process the dictionary
        return {k: remove_nones_from_dict(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        # Recursively process lists if there are any (optional for dataclass scenarios)
        return [remove_nones_from_dict(item) for item in data if item is not None]
    else:
        # Return the value if it's not a dict or list
        return data


def count_non_none_properties(instance):
    return sum(1 for field in fields(instance) if getattr(instance, field.name) is not None)


def count_non_none_properties_recursive(instance):
    def count_fields(obj):
        if hasattr(obj, '__dataclass_fields__'):  # Check if it's a dataclass
            return sum(
                # Recur for nested objects
                1 + count_fields(getattr(obj, field.name))
                for field in fields(obj)
                if getattr(obj, field.name) is not None
            )
        return 0  # Non-dataclass or base case
    return count_fields(instance)


def product1_has_more_properties(product1: Any, product2: Any) -> bool:
    count1 = count_non_none_properties(product1)
    count2 = count_non_none_properties(product2)

    if count1 > count2:
        print(f"Product1 has more non-None properties: {count1}")
        return True
    elif count2 > count1:
        print(f"Product2 has more non-None properties: {count2}")
        return False
    else:
        print(
            f"Both Product instances have the same number of non-None properties: {count1}")
        return False

    # Example Usage:
    product1 = Product(name="Laptop", price=999.99, stock=50)
    product2 = Product(name="Phone", price=None, category="Electronics",
                       stock=100, description="Latest model")

    result = compare_products(product1, product2)
    print(result)


# Function to remove everything before and including a colon
StrOrArray: TypeAlias = Union[str, list, None]


def remove_text_before_last_delimiter_occurence(value: StrOrArray, delimiter: str, undo_if_result_empty=False) -> StrOrArray:
    def operation(item: str):
        # remove any trailing dot
        res = item.split(delimiter)[-1].strip().rstrip('.')
        if not res and undo_if_result_empty:
            return item.rstrip(delimiter)
        return res
    if isinstance(value, str):
        return operation(value)
    elif isinstance(value, list):
        return [operation(item) for item in value]
    else:
        return None


def remove_text_before_first_delimiter_occurence(value: StrOrArray, delimiter: str, undo_if_result_empty=False) -> StrOrArray:
    def operation(item: str):
        # Split only at the first occurrence of the delimiter
        parts = item.split(delimiter, 1)  # The '1' ensures it splits only once
        res = parts[-1].strip().rstrip('.') if len(parts) > 1 else item
        print(f"res: A{res}A")
        if not res and undo_if_result_empty:
            return item.rstrip(delimiter)
        return res
    if isinstance(value, str):
        return operation(value)
    elif isinstance(value, list):
        return [operation(item) for item in value]
    else:
        return None


def split_strings_on_dot(strings: List[str]) -> List[str]:
    result = []
    for s in strings:
        done = False
        s = s.replace("-", "").strip()
        if '(' in s and s.find('(') > 0:
            # Split the string by ( only if it is located between two string
            result.extend(part.strip() for part in s.split('('))
            done = True
        if ')' in s and s.find('(') == len(s) - 1:
            # remove ) only if it is located at the end of string
            s = s.replace(")", "").strip()
        if '.' in s:
            # Split the string by dots and extend the result list with the split parts
            result.extend(part.strip() for part in s.split('.'))
            done = True
        if '\n' in s:
            result.extend(part.strip() for part in s.split('\n'))
            done = True
        if not done and s:
            # If no dot, just append the original string
            result.append(s)
    return result
    # Example usage
    strings = [
        "hello.world",
        "no_dot_here",
        "another.example.string",
        "final.test"
    ]

    # Call the function
    result = split_strings_on_dot(strings)
    print(result)
    # Output: ['hello', 'world', 'no_dot_here', 'another', 'example', 'string', 'final', 'test']


def remove_percent_values(text):
    # Updated regex to handle cases with or without space before the percent symbol
    cleaned_text = re.sub(r'\s*\d+(?:[.,]\d+)?\s*%\s*', '', text)
    # Split the cleaned text by commas and strip any extra whitespace around each item
    items = [item.strip() for item in cleaned_text.split(',') if item.strip()]
    # Join items back into a single string, separated by commas
    result = ', '.join(items)
    return result
    # Example usage
    text = "pomme 54,3%, pêche 7,5%, abricot 7%, toto4%, titi6,7%"
    print(remove_percent_values(text))
    # Output: "pomme, pêche, abricot, toto, titi"


def remove_numbers_and_fractions(text):
    # Remove all integers and fractions (e.g., "5 ", "34 ", "1/3 ", "1/4 ")
    cleaned_text = re.sub(r'\b\d+(/\d+)?\s+', '', text)
    return cleaned_text
    # Example usage
    text = "5 pommes pressées, 34 raisins pressés, 19 framboises, 1/3 poire, 1/4 grenade pressée"
    print(remove_numbers_and_fractions(text))


def remove_keywords_and_empty_texts(texts: list, keywords: list):
    if not isinstance(texts, list) or not isinstance(keywords, list):
        return texts

    result = []
    for text in texts:
        # Remove each keyword in the list from the text
        for keyword in keywords:
            text = text.replace(keyword, "").strip()
        # Only add the text to the result if it is not empty
        if text:
            result.append(text.strip())
    # remove duplicates:
    return list(set(result))

    # Example usage
    texts = [
        "Hello world!",
        "Python is amazing.",
        "Hello",
        "Just a keyword here",
        "Another keyword",
        "Only keyword"
    ]
    keywords = ["keyword", "Hello"]

    print(remove_keywords_and_empty_texts(texts, keywords))
    # Expected output: ["world!", "Python is amazing.", "Just a here", "Another"]


def rephrase_text_if_parenthesis_exists(text):
    """
    Rephrases the text to handle content inside parentheses.
    Adds the prefix of the text before parentheses to each element inside.
    Leaves the text unchanged if there are no parentheses.
    """

    # some cleaning first:
    text = remove_percent_values(text)
    text = remove_numbers_and_fractions(text)
    text = add_space_after_comma(text=text)
    text = text.replace(" :(", " (")

    # Match the text before parentheses and the content inside them
    match = re.match(r"(.*)\((.*)\)", text)
    if not match:
        return text  # Return unchanged text if no parentheses are found

    prefix = match.group(1).strip()  # Text before parentheses
    inside_parentheses = match.group(2).strip()  # Text inside parentheses

    # Handle nested parentheses by splitting only on commas
    items = re.split(r",\s*(?![^(]*\))", inside_parentheses)

    # Construct the rephrased text
    transformed_items = [f"{prefix} {item.strip()}" for item in items]
    return ", ".join(transformed_items)

# def rephrase_text_if_parenthesis_exists(text):
#     text = remove_percent_values(text)
#     text = remove_numbers_and_fractions(text)
#     text = add_space_after_comma(text=text)
#     text = text.replace(" :(", " (")
#     print(f"add_space_after_comma: {text}")
#     # Use a while loop to find and replace all occurrences that match the pattern
#     pattern = r"(\w+)\s*\(([^)]+)\)"
#     while True:
#         match = re.search(pattern, text)
#         if not match:
#             break  # Exit loop if no more matches are found

#         prefix = match.group(1)  # Extract the prefix (e.g., "vitamines" or "base")
#         # remove the S if exists in the end of the selected prefix
#             # Use rstrip to remove only the specified character if it is at the end
#         prefix = prefix.rstrip("s")

#         items = match.group(2).split(', ')  # Split items by ", "

#         # Build the transformed text by adding the prefix before each item
#         transformed_text = ', '.join(f"{prefix} {item.strip()}" for item in items)

#         # Replace the matched part in the original text with the transformed text
#         text = text[:match.start()] + transformed_text + text[match.end():]
#     # if parenthesis still exist but in another format that does not apply on previous match
#     text = text.replace("()", "").strip()
#     print(f"rephrase_text_if_parenthesis_exists: {text}")
#     return text
#     # Example usage
#     text1 = "vitamines (C, A, acide folique, B6, thiamine)"
#     text2 = "vitamines C, A, acide folique, B6, thiamine"  # No parentheses
#     text3 = "ingredients (D, A, acide folique, s, k)"

#     print(transform_text(text1))
#     # Output: "vitamines C, vitamines A, vitamines acide folique, vitamines B6, vitamines thiamine"

#     print(transform_text(text2))
#     # Output: "vitamines C, A, acide folique, B6, thiamine" (unchanged)

#     print(transform_text(text3))
#     # Output: "ingredients D, ingredients A, ingredients acide folique, ingredients s, ingredients k"


def add_space_after_comma(text):
    # Use regex to match commas not followed by a space and replace them with a comma and space
    return re.sub(r',(?=\S)', ', ', text)
    # Example usage
    text1 = "vitamines (C,E, pro-A)"
    text2 = "abede, rr,r"
    print(add_space_after_comma(text1))
    # Output: "vitamines (C, E, pro-A)"


def get_most_used_delimiter(text: str) -> str:
    # Define possible delimiters
    delimiters = {
        ',': text.count(','),
        '-': text.count('-'),
        '\n': text.count('\n')
    }

    # Find the delimiter with the maximum count
    most_used_delimiter = max(delimiters, key=delimiters.get)

    return most_used_delimiter
    # Example usage:
    cleaned_text = "line1,line2\nline3-line4,line5\n"
    result = detect_most_used_delimiter(cleaned_text)
    print(f"The most used delimiter is: '{result}'")

import re

def match_all_numbers(text):
    pattern = r"\d+\.\d+|\d+"  # This will match both integer and decimal numbers.
    numbers = re.findall(pattern, text)
    # Convert to float if it's a decimal number and int if it's an integer.
    numbers = [float(num) if '.' in num else int(num) for num in numbers]
    return numbers

def dump_json_then_write_it_to_file(file_uri, new_products):
    if not new_products or len(new_products) == 0:
        return
    json_object = json.dumps(new_products,
                                     default=lambda o: dict(
                                         (key, value) for key, value in o.__dict__.items() if value is not None),
                                     indent=4,
                                     allow_nan=False,
                                     ensure_ascii=False,
                                     skipkeys=True)
    write_output_to_file(data=json_object, file_name=file_uri,
                                 path_includes_in_file_name=True, include_seconds_in_date=False, extension='.json')
    print(f"number of objects: {len(new_products)}, file saved in: {file_uri}")



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

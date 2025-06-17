'''
  Appium Webdriver utils.
  Easy to use appium webdriver method.
'''

import logging
import os
import sys
import time
from typing import List

try:
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, WebDriverException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    logging.critical("Selenium module is not installed1...Exiting program.")
    exit(1)


def PATH(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)


def setup_logging(path: str, filename=None, force_override_existing_setup=False):
    # Ensure the directory exists and is writable
    if not os.path.isdir(path):
        os.mkdir(path)
    if not os.access(path, os.W_OK):
        raise PermissionError(f"Path {path} cannot be written.")

    # Generate the log filename with timestamp
    timestr = time.strftime('%Y_%m_%d_%H.%M.%S', time.localtime(time.time()))
    filename2 = os.path.join(path, f"{timestr}.log")
    if isinstance(filename, str):
        filename2 = os.path.join(path, f"{filename}_{timestr}.log")

    print(f"Filename for logging: {filename2}")

    # Set up logging to a file
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s - %(message)s",
        filename=filename2,
        filemode='a',
        force=force_override_existing_setup
    )

    # Create a console handler for printing logs to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s"))

    # Add the console handler to the root logger
    logging.getLogger().addHandler(console_handler)


# if not (os.path.isdir(PATH('../logs'))):
#     os.mkdir(PATH('../logs'))
#     if not (os.access(PATH('../logs'), os.W_OK)):
#         msg = ('Path %s cannot be written.', PATH('../logs'))

# timestr = time.strftime('%Y_%m_%d_%H.%M.%S', time.localtime(time.time()))
# logging.basicConfig(
#     level=logging.INFO,
#     format="[%(asctime)s] %(levelname)s- %(message)s",
#     filename=PATH("../logs/" + timestr + ".log"),
#     filemode='a',
#     force=True
# )


def write_log_to_file(log):
    print_and_log(log)


def wait_el_class(driver, element, timeout=8, poll_frequency=0.5):
    print(3)
    if driver is None:
        return None
    try:
        return WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions, poll_frequency=poll_frequency).until(lambda x: x.find_element_by_class_name(element))
    except TimeoutException:
        logging.info(
            "TIMEOUT, Please confirm if the class name ({0}) is exist.".format(element))
        return None
    except WebDriverException:
        logging.info(
            "WebDriverException, Please confirm if the class name ({0}) is correct.".format(element))
        return None


def wait_els_class(driver, element, timeout=8, poll_frequency=0.5):
    if driver is None:
        return None
    try:
        return WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions, poll_frequency=poll_frequency).until(lambda x: x.find_elements_by_class_name(element))
    except TimeoutException:
        logging.info(
            "TIMEOUT, Please confirm if the class name ({0}) is exist.".format(element))
        return None
    except WebDriverException:
        logging.info(
            "WebDriverException, Please confirm if the class name ({0}) is correct.".format(element))
        return None


def wait_el_class_click(driver, element, timeout=8, poll_frequency=0.5):
    if driver is None:
        return None
    try:
        WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions, poll_frequency=poll_frequency).until(
            lambda x: x.find_element_by_class_name(element)).click()
        return True
    except TimeoutException:
        logging.info(
            "TIMEOUT, Please confirm if the class name ({0}) is exist.".format(element))
        return False
    except WebDriverException:
        logging.info(
            "WebDriverException, Please confirm if the class name ({0}) is correct.".format(element))
        return False


def wait_el_id(driver, element, timeout=8, poll_frequency=0.5):
    if driver is None:
        return None
    try:
        return WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions, poll_frequency=poll_frequency).until(lambda x: x.find_element_by_id(element))
    except TimeoutException:
        logging.info(
            "TIMEOUT, Please confirm if the id({0}) is exist.".format(element))
        return None
    except WebDriverException:
        logging.info(
            "WebDriverException, Please confirm if the xPath({0}) is correct.".format(element))
        return None


def wait_els_selector(driver, elements, timeout=8, poll_frequency=0.5):
    if driver is None:
        return None
    try:
        return WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions, poll_frequency=poll_frequency).until(lambda x: x.find_elements_by_css_selector(elements))
    except TimeoutException:
        logging.info(
            "TIMEOUT, Please confirm if the selector({0}) is exist.".format(elements))
        return None
    except WebDriverException:
        logging.info(
            "WebDriverException, Please confirm if the selector({0}) is correct.".format(elements))
        return None


def wait_el_xpath(driver, element, timeout=8, poll_frequency=0.5):
    if driver is None:
        return None
    try:
        return WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions, poll_frequency=poll_frequency).until(lambda x: x.find_element_by_xpath(element))
    except TimeoutException:
        logging.info(
            "TIMEOUT, Please confirm if the xPath({0}) is exist.".format(element))
        return None
    except WebDriverException:
        logging.info(
            "WebDriverException, Please confirm if the xPath({0}) is correct.".format(element))
        return None


def wait_els_xpath(driver, elements, timeout=8, poll_frequency=0.5):
    if driver is None:
        return None
    try:
        return WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions, poll_frequency=poll_frequency).until(lambda x: x.find_elements_by_xpath(elements))
    except TimeoutException:
        logging.info(
            "TIMEOUT, Please confirm if the xPath({0}) is exist.".format(elements))
        return None
    except WebDriverException:
        logging.info(
            "WebDriverException, Please confirm if the xPath({0}) is correct.".format(elements))
        return None


def wait_el_xpath_click(driver, element, timeout=8, poll_frequency=0.5):
    if driver is None:
        return None
    try:
        (WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions,
         poll_frequency=poll_frequency).until(lambda x: x.find_element_by_xpath(element))).click()
        return True
    except TimeoutException as te:
        logging.info(
            "TIMEOUT: {0}; Please confirm if the xPath({1}) is exist.".format(te, element))
        return False
    except WebDriverException as wde:
        logging.info(
            "WebDriverException: {0}; Please confirm if the xPath({1}) is correct.".format(wde, element))
        return False

# retrieving an HTML element based on its class attribute may not be a good strategy.
# This is because CSS classes are attributes that can easily change over time.


def wait_els(driver: webdriver, by: By, element: str, should_print: bool = True, timeout=0.5, poll_frequency=0.5) -> List[WebElement] | None:
    if driver is None:
        return None
    try:
        return WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions, poll_frequency=poll_frequency).until(lambda x: x.find_elements(by, element))
    except StaleElementReferenceException as e:
        msg = ("wait_els; Please confirm if the %s:(%s) exists. StaleElementReferenceException: %s; ", by, element, e)
        print_and_log(msg, should_print)
        return None
    except NoSuchElementException as e:
        msg = ("wait_els; Please confirm if the %s:(%s) exists. NoSuchElementException: %s; ", by, element, e)
        print_and_log(msg, should_print)
        return None
    except TimeoutException:
        msg = (
            "wait_els: Please confirm if the %s:(%s) is exist. TIMEOUT", by, element)
        print_and_log(msg, should_print)
        return None
    except WebDriverException as e:
        msg = ("wait_els: Please confirm if the %s:(%s) is correct. WebDriverException:%s.", by, element, e)
        print_and_log(msg, should_print)
        return None


def wait_el(driver: webdriver, by: By, element: str, should_print: bool = True, timeout=0.5, poll_frequency=0.5) -> WebElement | None:
    if driver is None:
        return None
    try:
        return WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions, poll_frequency=poll_frequency).until(lambda x: x.find_element(by, element))
    except StaleElementReferenceException as e:
        msg = ("wait_el; Please confirm if the %s:(%s) exists. StaleElementReferenceException: %s; ", by, element, e)
        print_and_log(msg, should_print)
        return None
    except NoSuchElementException as e:
        msg = ("wait_el; Please confirm if the %s:(%s) exists. NoSuchElementException: %s; ", by, element, e)
        print_and_log(msg, should_print)
        return None
    except TimeoutException:
        msg = ("wait_el: Please confirm if the %s:(%s) is exist. TIMEOUT", by, element)
        print_and_log(msg, should_print)
        return None
    except WebDriverException as e:
        msg = ("wait_el: Please confirm if the %s:(%s) is correct. WebDriverException:%s.", by, element, e)
        print_and_log(msg, should_print)
        return None


def wait_el_click(driver: webdriver, by: By, element: str, should_print: bool = True, timeout=0.5, poll_frequency=0.5) -> bool:
    if driver is None:
        return None
    try:
        el = wait_el(driver, by, element, timeout, poll_frequency)
        if el is not None:
            el.click()
            return True
        return False
    except StaleElementReferenceException as e:
        msg = ("wait_el_click; Please confirm if the %s:(%s) exists. StaleElementReferenceException: %s; ", by, element, e)
        print_and_log(msg, should_print)
        return None
    except NoSuchElementException as e:
        msg = ("wait_el_click; Please confirm if the %s:(%s) exists. NoSuchElementException: %s; ", by, element, e)
        print_and_log(msg, should_print)
        return False
    except TimeoutException:
        msg = (
            "wait_el_click: Please confirm if the %s:(%s) exists. TIMEOUT", by, element)
        print_and_log(msg, should_print)
        return False
    except WebDriverException as e:
        msg = ("wait_el_click: Please confirm if the %s:(%s) is correct. WebDriverException:%s.", by, element, e)
        print_and_log(msg, should_print)
        return False

# getText() is used to get the visible inner text of a web element and the sub elements.
# By visible, we mean that the text which is not hidden by CSS.


def wait_el_text(driver: webdriver, by: By, element: str, should_print: bool = True, timeout=0.5, poll_frequency=0.5) -> str | None:
    if driver is None:
        return None
    try:
        el = wait_el(driver, by, element, timeout, poll_frequency)
        return el.text if el is not None else None
    except StaleElementReferenceException as e:
        msg = ("wait_el_text; Please confirm if the %s:(%s) exists. StaleElementReferenceException: %s; ", by, element, e)
        print_and_log(msg, should_print)
        return None
    except NoSuchElementException as e:
        msg = ("NoSuchElementException: %s; wait_el_xpath_text: Please confirm if the class name:(%s) exists.", e, element)
        print_and_log(msg, should_print)
        return None
    except TimeoutException as te:
        msg = (
            "TIMEOUT: %s; wait_el_xpath_text: Please confirm if the xPath(%s) exists.", te, element)
        # msg = ("TIMEOUT: %s; Please confirm if the xPath(%s) is exist.", te, element))
        print_and_log(msg, should_print)
        return None
    except WebDriverException as wde:
        msg = ("WebDriverException: %s; wait_el_xpath_text: Please confirm if the xPath(%s) is correct", wde, element)
        # msg = ("WebDriverException: %s; Please confirm if the xPath(%s) is correct.", wde, element))
        print_and_log(msg, should_print)
        return None


def wait_el_Attribute(driver: webdriver, by: By, element: str, attribute: str, should_print: bool = True, timeout=0.5, poll_frequency=0.5) -> str | None:
    if driver is None:
        return None
    try:
        el = wait_el(driver, by, element, timeout, poll_frequency)
        return el.get_attribute(attribute) if el is not None else None
    except StaleElementReferenceException as e:
        msg = ("wait_el_Attribute; Please confirm if the %s:(%s) exists. StaleElementReferenceException: %s; ", by, element, e)
        print_and_log(msg, should_print)
        return None
    except NoSuchElementException as e:
        msg = ("wait_el_xpath_Attribute: Please confirm if the %s:(%s) exists. NoSuchElementException: %s; ", by, e, element)
        print_and_log(msg, should_print)
        return None
    except TimeoutException as te:
        msg = (
            "wait_el_Attribute: Please confirm if the %s:(%s) exists. TIMEOUT: %s; ", by, te, element)
        print_and_log(msg, should_print)
        return None
    except WebDriverException as wde:
        msg = (
            "wait_el_Attribute; Please confirm if the %s:(%s) is correct. WebDriverException: %s;", by, element, wde)
        print_and_log(msg, should_print)
        return None


def get_attribute_from_element(element: WebElement, attribute: str, element_name: str = '', should_print: bool = True) -> str | StaleElementReferenceException:
    if element is None:
        return None
    try:
        text = element.get_attribute(
            attribute) if element is not None else None
        return text
    except StaleElementReferenceException as e:
        msg = ("get_attribute_from_element; Please confirm if the %s:(%s) exists. StaleElementReferenceException: %s; ", attribute, element_name)
        print_and_log(msg, should_print)
        return e
    except NoSuchElementException as e:
        msg = ("NoSuchElementException; get_attribute_from_element: Please confirm if the attribute:(%s) exists. element_name: %s, error: %s", attribute, element_name, e)
        print_and_log(msg, should_print)
        return None
    except TimeoutException:
        msg = ("TIMEOUT; get_attribute_from_element: Please confirm if the attribute:(%s) exists.element_name: %s, ",
               element_name, attribute)
        print_and_log(msg, should_print)
        return None
    except WebDriverException as e:
        msg = ("WebDriverException; get_attribute_from_element: Please confirm if the attribute(%s) is correct. element_name: %s, error:%s", attribute, element_name, e)
        print_and_log(msg, should_print)
        return None
    except:
        msg = ("WebDriverException; get_attribute_from_element: Please confirm if the attribute(%s) is correct. element_name: %s", element_name, attribute)
        print_and_log(msg, should_print)
        return None


def get_text_from_element(element: WebElement, should_print: bool = True) -> str | None:
    if element is None:
        return None
    try:
        text = element.text if element else ''
        return text
    except StaleElementReferenceException as e:
        msg = ("get_text_from_element; Please confirm if the attribute(text) exists. StaleElementReferenceException: %s;", e)
        print_and_log(msg, should_print)
        return None
    except NoSuchElementException as e:
        msg = ("etTextFromElement; Please confirm if the attribute(text) exists. StaleElementReferenceException: %s;", e)
        print_and_log(msg, should_print)
        return None
    except TimeoutException:
        msg = (
            "etTextFromElement; Please confirm if the attribute(text) exists. TimeoutException;")
        print_and_log(msg, should_print)
        return None
    except WebDriverException as e:
        msg = (
            "etTextFromElement; Please confirm if the attribute(text) exists. StaleElementReferenceException :%s", e)
        print_and_log(msg, should_print)
        return None
    # except:
    #    msg = (
    #        "WebDriverException, Please confirm if the xPath(%s) is correct.", element))
    #    return None


def check_exists_by_id(webdriver, id):
    try:
        webdriver.find_element(By.ID, id)
    except NoSuchElementException:
        return False
    return True


# def check_exists_by_xpath(webdriver, xpath):
#     try:
#         webdriver.find_element(By.XPATH, xpath)
#     except NoSuchElementException:
#         return False
#     return True


def check_exists_by_class_name(webdriver, class_name):
    try:
        webdriver.find_element(By.CLASS_NAME, class_name)
    except NoSuchElementException:
        return False
    return True


def print_and_log(msg: str, should_print=True):
    if should_print:
        print(msg)
    logging.info(msg)


def wait_time(func):
    def inner(*args):
        time.sleep(0.5)
        f = func(*args)
        time.sleep(0.5)
        return f
    return inner


@wait_time
def screenshot(driver):
    filename = ''.join(PATH("../logs/" + str(time.time()) + ".png"))
    return driver.get_screenshot_as_file(filename)

# Swipe: Left Right Up Down


class MobileSwipe():
    def __init__(self):
        pass

    def swipe_up(self, driver, time=500):
        width = driver.get_window_size()['width']
        height = driver.get_window_size()['height']
        driver.swipe(width / 2, height * 2 / 3,
                     width / 2, height * 1 / 3, time)

    def swipe_down(self, driver, time=500):
        width = driver.get_window_size()['width']
        height = driver.get_window_size()['height']
        driver.swipe(width / 2, height * 1 / 3,
                     width / 2, height * 2 / 3, time)

    def swipe_left(self, driver, time=500):
        width = driver.get_window_size()['width']
        height = driver.get_window_size()['height']
        driver.swipe(width * 3 / 4, height / 2,
                     width * 1 / 4, height / 2, time)

    def swipe_right(self, driver, time=500):
        width = driver.get_window_size()['width']
        height = driver.get_window_size()['height']
        driver.swipe(width * 1 / 4, height / 2,
                     width * 3 / 4, height / 2, time)


if __name__ == "__main__":
    MobileSwipe()

# custom expected condition


class wait_for_element_to_beLocated_andVisible:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element = driver.find_element(driver, self.locator)
            if element.is_enabled() is True and element.is_displayed() is True:
                return True
            else:
                return False
        except:
            return False

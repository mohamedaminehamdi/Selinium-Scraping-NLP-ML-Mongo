# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from typing import Final
from utils.my_utils import DriverConfig, write_output_to_file
from utils import appium_utils

from model.my_model import ProductBrand, ProductAisle, ProductType, ProductCategory, obj_dict
webdriverInstance = DriverConfig.getDriver(DriverConfig.DriverType.CHROME)
URL_BASE_PICARD: Final[str] = "https://www.picard.fr"


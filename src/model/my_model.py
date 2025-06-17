#!/usr/bin/env python
# coding: utf-8
from __future__ import annotations

import os
import inspect
from pydantic.dataclasses import dataclass
#from dataclasses import dataclass
from enum import Enum
import sys
from typing import Optional, List, TypeVar, Type
# sys.path.append('./')

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils'))
sys.path.append(parent_dir)

from utils.my_utils import xstr

T = TypeVar('T')

def from_dict_to_objects(key: T, dicts: Optional[List[dict]]) -> List[T]:
    if isinstance(dicts, list):
        items: List[dict] = []
        for item in dicts:
            item_result = key.from_dict_to_object(item)
            items.append(item_result)
        return items
    return []

# Article type enumeration


class ProductType(Enum):
    SUBSTANCE = 1
    LIQUID = 2
    PIECE = 3
    OTHER = 4

# create a class ProductAisle
@dataclass
class ProductAisle:
    aisle_id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    image: Optional[str] = None
    products_count_in_aisle: Optional[int] = None
    parsing_duration: Optional[int] = None
    products: Optional[List[ProductAisle]] = None
    create_at: Optional[str] = None
    update_at: Optional[str] = None
    brands: Optional[List[str]] = None

    def __str__(self):
        my_dict = self.to_dict()
        return str(my_dict)

    def to_dict(self) -> dict:
        return {"aisle_id": self.aisle_id, "name1": self.name, "url": self.url,
                "products_count_in_aisle": self.products_count_in_aisle, "parsing_duration": self.parsing_duration,
                "products": [product.to_dict() for product in self.products],
                "brands": self.brands, "create_at": self.create_at, "update_at": self.update_at, "image": self.image}


@dataclass
class ProductCategory():

    category_id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    products_count_in_all_categories: Optional[int] = None
    parsing_duration: Optional[int] = None
    aisles: Optional[List[ProductAisle]] = None
    create_at: Optional[str] = None
    update_at: Optional[str] = None

    def __str__(self):
        my_dict = self.to_dict()
        return str(my_dict)

    def to_dict(self) -> dict:
        return {"category_id": self.category_id, "name": self.name, "url": self.url,
                "products_count_in_all_categories": self.products_count_in_all_categories,
                "parsing_duration": self.parsing_duration, "aisles": [aisle.to_dict() for aisle in self.aisles],
                "create_at": self.create_at, "update_at": self.update_at}


@dataclass
class ProductBrand:
    name: Optional[str] = None
    brand_id: Optional[str] = None
  
    
    def __str__(self):
        my_dict = self.to_dict()
        return str(my_dict)
        # return ("brand_id: " + self.brand_id + ", brand_name: " + self.name)

    def to_dict(self) -> dict:
        return {"name": self.name,
                "brand_id": self.brand_id
                }

    @staticmethod  # @classmethod    def to_dict(cls) -> dict:
    def getAllKnownBrands()-> List[str]:
        return ["BONNE MAMAN", "Bordeaux", "MADERN", "TANOSHI", "DOVE",
                "SOPALIN", "KNORR", "BRIDELICE", "LU", "FITNESS","Picard", "Cuisine Evasion", "Picard Gourmet", "Picard Bio",
        "Sélection Picard", "Collection Picard"
        ]


class CasinoMockingData():
    def __init__(self):
        pass

    def getDummyData(self):
        print(os.getcwd())
        file = open("../Model/CasinoDummyData.txt")
        content = file.read()
        file.close()
        return content


def obj_dict(obj):
    return obj.__dict__


@dataclass
class AislesSub:
    id: Optional[str] = None
    label: Optional[str] = None
    subs: Optional[List[AislesSub]] = None

    def __eq__(self, other):
        return (self.id == other.id)  # and (self.g == other.g)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.id < other.id)  # and (self.g < other.g)

    def __gt__(self, other):
        return (self.id > other.id)  # and (self.g > other.g)

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)

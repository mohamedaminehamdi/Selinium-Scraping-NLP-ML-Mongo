from __future__ import annotations

# from dataclasses import dataclass
from typing import List, Optional

from pydantic.dataclasses import dataclass


# create a class containing Static Aisles to parse
@dataclass
class StaticAisle:
    name: Optional[str] = None
    url: Optional[str] = None
    uri: Optional[str] = None
    original_file_uri: Optional[str] = None
    mini_file_uri: Optional[str] = None
    mini_file_detailed_uri: Optional[str] = None
    file_with_allergens: Optional[str] = None
    aisle_id: Optional[str] = None
    image: Optional[str] = None
    brands: Optional[List[str]] = None
    aisles: Optional[List[StaticAisle]] = None

    def __str__(self):
        my_dict = self.to_dict()
        return str(my_dict)

    def to_dict(self) -> dict:
        return {"aisle_id": self.aisle_id, "name": self.name, "url": self.url,
                "uri": self.uri, "image": self.image, "brands": self.brands}

@dataclass
class StaticCategory():
    aisles: List[StaticAisle]
    name: Optional[str] = None
    url: Optional[str] = None
    uri: Optional[str] = None
    category_id: Optional[str] = None

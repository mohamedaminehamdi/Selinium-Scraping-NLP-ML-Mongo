from typing import Optional, List, Dict, Any

from src.model.product import Category

class ProductFilter:
    def __init__(self):
        self.filters: Dict[str, Any] = {}

    def add_brand(self, brand: Optional[str]) -> "ProductFilter":
        if brand is not None:
            self.filters['brand'] = brand
        return self

    def add_category_ids(self, categories: Optional[List[Category]]) -> "ProductFilter":
        if categories is not None:
            self.filters['categories.id'] = {
                '$in': [category.id for category in categories]
            }
        return self

    def with_or_without_ia_ingredients(self, without: bool) -> "ProductFilter":
        self.filters['evolutions.ingredients_ia'] = {
            '$exists': not without
        }
        return self

    def build(self) -> Dict[str, Any]:
        return self.filters

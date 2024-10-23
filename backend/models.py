from pydantic import BaseModel
from typing import Optional

class GroceryItem(BaseModel):
    name: str
    qty: int | None = None

    # def __eq__(self,other):
    #     return self.name == other.name

class Recipe(BaseModel):
    name: str
    ingredients: list[GroceryItem]
    instruction: str

    def validate_grocery(self, items: list[GroceryItem]):
        item_names = [item.name for item in items]
        ingredient_names = [ingredient.name for ingredient in self.ingredients]
        for ingredient in ingredient_names:
            if ingredient not in item_names:
                return False
        return True



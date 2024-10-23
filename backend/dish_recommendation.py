from models import GroceryItem, Recipe
import database_models as db
from sqlalchemy import Connection, select

# dishes = [
#     {    
#         "name": "Fries",
#         "recipe": Recipe(
#             ingredients=[
#                 GroceryItem(name="potato",qty=2)
#             ],
#             instruction="Cut the potato and deep fry them"
#         )
#     },
#     {
#         "name": "Banana Karaage",
#         "recipe": Recipe(
#             ingredients=[
#                 GroceryItem(name="banana",qty=1),
#                 GroceryItem(name="chicken thigh",qty=3)
#             ],
#             instruction="Mash the banana into paste,then cover the thigh in banana paste and deep fry it."
#         )
#     }
# ]

# recipes = [
#     Recipe(
#         name="Fries",
#         ingredients=[
#             GroceryItem(name="potato", qty=2)
#         ],
#         instruction = "Cut potato and fry."
#     ),
#     Recipe(
#         name="Banana Karaage",
#         ingredients=[
#             GroceryItem(name="banada", qty=1),
#             GroceryItem(name="chicekn", qty=3)
#         ],
#         instruction = "Coat chicken with banana and fry."
#     )
# ]

# def recommend_dishes(items: list[GroceryItem]):
#     result = []

    # for dish in dishes:
    #     dish = Dish.model_validate(dish)
    
    #     is_valid = dish.recipe.validate_grocery(items)
    #     if is_valid:
    #         result.append(dish)
    # return result
    # for recipe in recipes:
    #     recipe = Recipe.model_validate(recipe)
    #     is_valid = recipe.validate_grocery(items)
    #     if is_valid: result.append(recipe)
    # return result

class DishRecommender:
    conn: Connection
    
    def __init__(self,conn):
        self.conn = conn
    
    def retrieve_recipes(self) -> list[Recipe]:
        result_recipes = []
        recipes = self.conn.execute(select(db.Recipe)).mappings().all()

        for recipe in recipes:
            recipe = dict(recipe)
            name = recipe["name"]
            ingredients = self.conn.execute(select(db.RecipeDetail).where(db.RecipeDetail.name == name)).mappings().all()
            recipe["ingredients"] = [{"name":ing["ingredient"],"qty": ing["qty"]} for ing in ingredients]

            recipe = Recipe.model_validate(recipe)
            result_recipes.append(recipe)
        return result_recipes

    def query(self, items: list[GroceryItem]):
        result = []

        recipes = self.retrieve_recipes()
        for recipe in recipes:
            is_valid = recipe.validate_grocery(items)
            if is_valid:
                result.append(recipe)

        return result 
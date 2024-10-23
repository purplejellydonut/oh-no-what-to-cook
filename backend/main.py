from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import GroceryItem, Recipe
from dish_recommendation import DishRecommender
from sqlalchemy import create_engine, select
from fastapi.middleware.cors import CORSMiddleware

import database_models as db

app = FastAPI()
engine = create_engine('sqlite:///grocery.db', echo=True)
conn = engine.connect()
dr = DishRecommender(conn)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/grocery-items")
def get_grocery_items():
    items = conn.execute(select(db.GroceryItem)).mappings().all()
    items = [GroceryItem.model_validate(item) for item in items]
    return items

@app.get("/recipes")
def get_recipes():
    return dr.retrieve_recipes()

@app.post("/recommend")
def get_dish_recommendations(items: list[GroceryItem]):
    return dr.query(items)


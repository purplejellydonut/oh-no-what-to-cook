from database_models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import sys
sys.path.insert(0, 'C:/Users/tiffa/OneDrive/Desktop/Python works/what-to-eat/backend/database_models/base.py')

class Recipe(Base):
    __tablename__ = 'recipe'
    
    name: Mapped[str] = mapped_column(primary_key = True)
    instruction: Mapped[str]


class RecipeDetail(Base):
    __tablename__ = 'recipe_detail'
    
    name: Mapped[str] = mapped_column(primary_key = True)
    line_no: Mapped[int] = mapped_column(primary_key = True)
    ingredient: Mapped[str]
    qty: Mapped[int]
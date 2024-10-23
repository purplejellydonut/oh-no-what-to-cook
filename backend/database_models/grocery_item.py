
from database_models.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import sys
sys.path.insert(0, 'C:/Users/tiffa/OneDrive/Desktop/Python works/what-to-eat/backend/database_models/base.py')

class GroceryItem(Base):
    __tablename__ = 'grocery_item'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


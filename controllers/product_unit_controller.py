import uuid

from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, desc, Float

from database import Base

class Product_Units(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    product_id = Column('product_id', String)
    ratio = Column('ratio', Float)
    weight = Column('weight', Float)
    volume = Column("volume", Float)

class Product_UnitsJson(BaseModel):
    name:str
    product_id:str
    ratio:float
    weight:float
    volume :float
#TODO

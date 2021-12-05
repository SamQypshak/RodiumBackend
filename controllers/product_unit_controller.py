import uuid

from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, desc, Float

from database import Base

class Product_Unit(Base):
    __tablename__ = 'products_units'
    id = Column(String, primary_key=True)
    name = Column('name', String)
    product_id = Column('product_id', String)
    ratio = Column('ratio', Float)
    weight = Column('weight', Float)
    volume = Column("volume", Float)

class Product_UnitJson(BaseModel):
    id:str
    name:str
    product_id:str
    ratio:float
    weight:float
    volume :float

def post_item(session,items):

    for item in items:
         recs=session.query(Product_Unit).filter(Product_Unit.id==item.id).all()


         if len(recs)>0: #if records by id found update

             rec=recs[0];
             rec.name=item.name
             rec.product_id = item.product_id
             rec.ratio = item.ratio
             rec.weight= item.weight
             rec.volume = item.volume

         else: #if records by id not found create new
            new_uid = str(uuid.uuid1())
            rec = Product_Unit(
                       id=new_uid,
                       name=item.name,
                       product_id=item.product_id,
                       ratio=item.ratio,
                       weight = item.weight,
                       volume=item.volume

                              )
            item.id=new_uid
         session.add(rec)
    session.commit()

def get_units(session,product_id):
  if len(product_id)>0:
    return session.query(Product_Unit).where(Product_Unit.product_id==product_id).all()
  else:
    return  session.query(Product_Unit).all()
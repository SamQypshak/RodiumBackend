from typing import Optional, List

from fastapi import APIRouter

from controllers import product_controller,product_unit_controller
from controllers.product_controller import ProductJson
from controllers.product_unit_controller import Product_UnitJson
from database import session


product_router =APIRouter()

@product_router.get("/products")
async def getclients(group_id:Optional[str] = None ):
    return  product_controller.get_all(session,group_id)

@product_router.post("/products/add")
async def post_clients(items:List[ProductJson]):
    product_controller.post_item(session, items)

@product_router.get("/products/group_path")
def get_group_path(id:str):
    return product_controller.get_group_path(session,id)

@product_router.get("/products/groups")
def products_groups():
    return  product_controller.get_groups(session)

@product_router.get("/product/units")
def products_units(product_id:Optional[str] ="" ):
    return  product_unit_controller.get_units(session,product_id)

@product_router.post("/product/units/add")
def products_units(items:List[Product_UnitJson]):
    return  product_unit_controller.post_item(session,items)
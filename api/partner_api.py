from typing import Optional, List

from fastapi import APIRouter

from controllers import client_controller
from controllers.client_controller import ClientJson
from database import session

partner_router =APIRouter()

@partner_router.get("/partners")
async def getclients(group_id:Optional[str] = None ):
    return  client_controller.getclients(session,group_id)

@partner_router.post("/partners/add")
async def post_clients(clients:List[ClientJson]):
    client_controller.post_clients(session, clients)

@partner_router.get("/partners/group_path")
def get_group_path(id:str):
    return client_controller.get_group_path(session,id)

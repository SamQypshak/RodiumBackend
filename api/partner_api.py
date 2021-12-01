from typing import Optional, List

from fastapi import APIRouter

from controllers import client_controller
from controllers.client_controller import ClientJson,PartnerContacts_Json
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

@partner_router.get("/partners/groups")
def get_group_path():
    return client_controller.get_groups(session)

@partner_router.post("/partner/contacts/add")
async def post_partner_contacts(items:List[PartnerContacts_Json]):
    client_controller.post_partner_contacts(session, items)


@partner_router.get("/partner/contacts")
async def post_partner_contacts(partner_id:Optional[str] ="" ):
    return  client_controller.get_partner_contacts(session,partner_id)
import uuid
from typing import List

from fastapi import FastAPI
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, String, create_engine, desc
from sqlalchemy.orm import declarative_base, Session

import client_controller
from client_controller import *



app = FastAPI()

engine = create_engine(
    "postgresql+psycopg2://postgres:123456@localhost/testrodium",
    echo=True, pool_size=6, max_overflow=10, encoding='latin1'
 )
engine.connect()


client_controller.initTables(engine)
session = Session(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/clients")
async def getclients():
    rows = session.query(Client).all()
    mass=[]
    for row in rows:
        mass.append({"id": row.id,
                     "code":row.code,
                     "name":row.name,
                     "bin":row.bin,
                     "main_phone":row.main_phone,
                     "main_adres":row.main_adres
                     })
    return mass

@app.post("/clients/add")
async def post_clients(clients:List[ClientJson]):

    for client in clients:
         items=session.query(Client).filter(Client.id==client.id).all()
         new_uid = str(uuid.uuid1())

         if len(items)>0: #if records by id found update

             item=items[0];
             item.name=client.name
             item.bin = client.bin
             item.main_phone = client.main_phone
             item.main_adres = client.main_adres

         else: #if records by id not found create new

            items = session.query(client_controller.Client).order_by(desc(Client.code)).all()
            newcode=""

            #new code
            if len(items) == 0:
                newcode="00001"
            else: #create next code
                code=items[0].code
                int_code=int(items[0].code)
                next_code_index = int_code + 1
                nils_len= len(code)-len(str(next_code_index))
                nills= nils_len *"0"
                newcode=nills+str(next_code_index)

            item = Client(id=new_uid,
                       code=newcode,
                       name=client.name,
                       bin=client.bin,
                       main_phone=client.main_phone,
                       main_adres=client.main_adres
                        )
         session.add(item)
         session.commit()


@app.get("/client_groups")
async def get_client_groups():
   rows= session.query(ClientGroup).all();
   mass = []
   for row in rows:
       mass.append({"id": row.id, "name": row.name, "parent_id": row.parent_id})
   return  mass


if __name__ == '__main__':
  uvicorn.run(app,port=8112)

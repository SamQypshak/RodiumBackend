import datetime, threading, time
from typing import Optional

import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from controllers import client_controller
from controllers.client_controller import *
import database



app = FastAPI()

engine = create_engine(
    "postgresql+psycopg2://postgres:123456@localhost/testrodium",
    echo=True, pool_size=6, max_overflow=10, encoding='latin1'
 )
engine.connect()
database.initTables(engine)

session = Session(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/partners")
async def getclients(group_id:Optional[str] = None ):
    return  client_controller.getclients(session,group_id)

@app.post("/partners/add")
async def post_clients(clients:List[ClientJson]):
    client_controller.post_clients(session, clients)

@app.get("/partners/group_path")
def get_group_path(id:str):
    return client_controller.get_group_path(session,id)

def foo():
    print(datetime.datetime.now())
    threading.Timer(1, foo).start()

def periodic_setGroupLevel():
    client_controller.setGroupLevel(session)
    threading.Timer(1, periodic_setGroupLevel).start()

if __name__ == '__main__':
  #foo()
  #periodic_setGroupLevel()
  uvicorn.run(app,port=8112)

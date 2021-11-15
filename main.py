import datetime, threading, time
from typing import Optional

import uvicorn
from fastapi import FastAPI
from api.partner_api import partner_router
from api.product_api import product_router
import database

app = FastAPI()

app.include_router(partner_router)
app.include_router(product_router)
database.initTables()

if __name__ == '__main__':

  uvicorn.run(app,port=8112)

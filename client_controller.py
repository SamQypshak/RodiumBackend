from pydantic.main import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Client(Base):
    __tablename__ = 'clients'
    id=Column(String,primary_key=True)
    code=Column('code', String(32))
    name=Column('name', String)
    bin=Column('bin', String)
    main_phone=Column('main_phone', String)
    main_adres = Column('main_adres', String)

class ClientJson(BaseModel):
    id :str
    code : str
    name : str
    bin : str
    main_phone : str
    main_adres : str

class ClientGroup(Base):
    __tablename__ = 'client_groups'
    id=Column(String,primary_key=True)
    name=Column('name', String)
    parent_id = Column('parent_id', String)

def initTables(engine):
  Base.metadata.create_all(engine)
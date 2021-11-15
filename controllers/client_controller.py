import uuid
from pydantic.main import BaseModel
from sqlalchemy import Column, String, desc, Boolean, Integer
from database import Base


class Partner(Base):
    __tablename__ = 'partners'
    id=Column(String,primary_key=True)
    code=Column('code', String(32))
    name=Column('name', String)
    bin=Column('bin', String)
    main_phone=Column('main_phone', String)
    main_adres = Column('main_adres', String)
    is_group=Column("is_group",Boolean)
    parent_id = Column("parent_id", String)
    is_supplier = Column("is_supplier", Boolean)
    is_customer = Column("is_customer", Boolean)
    group_level=Column("group_level", Integer)

class ClientJson(BaseModel):
    id :str
    code : str
    name : str
    bin : str
    main_phone : str
    main_adres : str
    is_group:bool
    parent_id : str
    is_supplier:bool
    is_customer:bool



def getclients(session,group_id):
    if group_id==None:
      rows = session.query(Partner).where(Partner.group_level==1).all()
    else:
      rows = session.query(Partner).where(Partner.parent_id==group_id).all()
    mass=[]
    for row in rows:
        parentrow=session.query(Partner).where(row.parent_id==Partner.id).all()
        parent_name=""
        if len(parentrow)>0:
            parent_name=parentrow[0].name
        mass.append({"id": row.id,
                     "code":row.code,
                     "name":row.name,
                     "bin":row.bin,
                     "main_phone":row.main_phone,
                     "main_adres":row.main_adres,
                     "is_group": row.is_group,
                     "parent_id": row.parent_id,
                     "is_supplier": row.is_supplier,
                     "is_customer": row.is_customer,
                     "parent_name": parent_name
                     })
    return mass

def post_clients(session,clients):

    for client in clients:
         items=session.query(Partner).filter(Partner.id==client.id).all()
         new_uid = str(uuid.uuid1())

         if len(items)>0: #if records by id found update

             item=items[0];
             item.name=client.name
             item.bin = client.bin
             item.main_phone = client.main_phone
             item.main_adres = client.main_adres
             item.is_group = client.is_group
             item.parent_id = client.parent_id
             item.is_supplier= client.is_supplier
             item.is_customer = client.is_customer

         else: #if records by id not found create new

            items = session.query(Partner).order_by(desc(Partner.code)).all()
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

            item = Partner(id=new_uid,
                       code=newcode,
                       name=client.name,
                       bin=client.bin,
                       main_phone=client.main_phone,
                       main_adres=client.main_adres,
                       is_group = client.is_group,
                       parent_id = client.parent_id,
                       is_supplier = client.is_supplier,
                       is_customer = client.is_customer
                        )
            client.id=new_uid
         session.add(item)
         session.commit()

    for client in clients:
       setGroupLevel(session, client.id)



def get_group_path(session,id):
    res=session.query(Partner).where(Partner.id==id).all()
    a='635550f5-4173-11ec-8a1e-244bfe8d08b5'
    groups=[]
    for row in res:
        groups.append({"name":row.name,"id":row.id})
        rec_getNextParent(session,groups,row.parent_id)
    groups.reverse()
    return groups

def rec_getNextParent(session,groups,id):
    res = session.query(Partner).where(Partner.id == id).all()
    for row in res:
        groups.append({"name":row.name,"id":row.id})
        rec_getNextParent(session,groups,row.parent_id)

def setGroupLevel(session,id=None):
    if id!=None:
        res = session.query(Partner).where(Partner.id==id).all()
    else:
        res = session.query(Partner).where(Partner.is_group == True).all()
    group_level=[]
    for row in res:
        groups = []
        groups.append({"name":row.name,"id":row.id})
        rec_getNextParent(session,groups,row.parent_id)
        group_level.append({"rec":row,"groups":groups})

    for group in group_level:
        rec=group.get("rec")
        glen=len(group.get("groups"))
        rec.group_level=glen
        session.add(rec)
    session.commit()



def rec_getNextParent(session,groups,id):
    res = session.query(Partner).where(Partner.id == id).all()
    for row in res:
        groups.append({"name":row.name,"id":row.id})
        rec_getNextParent(session,groups,row.parent_id)
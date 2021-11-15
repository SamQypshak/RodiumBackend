import uuid

from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, desc

from database import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(String, primary_key=True)
    code = Column('code', String(32))
    name = Column('name', String)
    parent_id = Column('parent_id', String)
    article = Column('article', String)
    main_unit_id = Column('main_unit', String)
    is_group = Column("is_group", Boolean)
    group_level = Column("group_level", Integer)

class ProductJson(BaseModel):
    id:str
    code:str
    name:str
    parent_id:str
    article:str
    main_unit_id:str
    is_group :bool





def get_all(session,group_id):
    if group_id==None:
      rows = session.query(Product).where(Product.group_level==1).all()
    else:
      rows = session.query(Product).where(Product.parent_id==group_id).all()
    mass=[]
    for row in rows:
        parentrow=session.query(Product).where(row.parent_id==Product.id).all()
        parent_name=""
        if len(parentrow)>0:
            parent_name=parentrow[0].name
        mass.append({"id": row.id,
                     "code": row.code,
                     "name": row.name,
                     "article": row.article,
                     "main_unit_id": row.main_unit_id,
                     "is_group": row.is_group,
                     "parent_id": row.parent_id,
                     "parent_name": parent_name
                     })
    return mass

def post_item(session,items):

    for item in items:
         recs=session.query(Product).filter(Product.id==item.id).all()
         new_uid = str(uuid.uuid1())

         if len(recs)>0: #if records by id found update

             rec=recs[0];
             rec.name=item.name
             rec.is_group = item.is_group
             rec.parent_id = item.parent_id
             rec.article= item.article
             rec.main_unit_id = item.main_unit_id
             rec.is_group = item.is_group


         else: #if records by id not found create new

            newcode=_new_code(session)

            rec = Product(id=new_uid,
                       code=newcode,
                       name=item.name,
                       article=item.article,
                       main_unit_id=item.main_unit_id,
                       is_group = item.is_group,
                       parent_id=item.parent_id

                              )
            item.id=new_uid
         session.add(rec)
    session.commit()

    for item in items:
       setGroupLevel(session, item.id)


def _new_code(session):
    items = session.query(Product).order_by(desc(Product.code)).all()
    newcode = ""

    # new code
    if len(items) == 0:
        newcode = "00001"
    else:  # create next code
        code = items[0].code
        int_code = int(items[0].code)
        next_code_index = int_code + 1
        nils_len = len(code) - len(str(next_code_index))
        nills = nils_len * "0"
        newcode = nills + str(next_code_index)
    return  newcode

def get_group_path(session,id):
    res=session.query(Product).where(Product.id==id).all()
    a='635550f5-4173-11ec-8a1e-244bfe8d08b5'
    groups=[]
    for row in res:
        groups.append({"name":row.name,"id":row.id})
        rec_getNextParent(session,groups,row.parent_id)
    groups.reverse()
    return groups

def rec_getNextParent(session,groups,id):
    res = session.query(Product).where(Product.id == id).all()
    for row in res:
        groups.append({"name":row.name,"id":row.id})
        rec_getNextParent(session,groups,row.parent_id)

def setGroupLevel(session,id=None):
    if id!=None:
        res = session.query(Product).where(Product.id==id).all()
    else:
        res = session.query(Product).where(Product.is_group == True).all()
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
    res = session.query(Product).where(Product.id == id).all()
    for row in res:
        groups.append({"name":row.name,"id":row.id})
        rec_getNextParent(session,groups,row.parent_id)
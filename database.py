from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()
engine = create_engine(
    "postgresql+psycopg2://postgres:123456@localhost/testrodium",
    echo=True, pool_size=6, max_overflow=10, encoding='latin1'
 )
engine.connect()


session = Session(bind=engine)

def initTables():
  Base.metadata.create_all(engine)


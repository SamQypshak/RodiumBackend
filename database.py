from sqlalchemy.orm import declarative_base

Base = declarative_base()

def initTables(engine):
  Base.metadata.create_all(engine)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy. ext.declarative import declarative_base

Base=declarative_base()
SQLALCHEMY = "sqlite:///./transport.db"
engine=create_engine(SQLALCHEMY,connect_args = {"check_same_thread": False} ) 
SessionLocal = sessionmaker (bind=engine,autocommit=False, autoflush=False,) 

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.data.data_base import Base
from app.data.data_base import write_sessionlocal,read_sessionlocal, write_engine,read_engine

def init_db():
    Base.metadata.create_all(bind=write_engine)

def get_write_db():
    db=write_sessionlocal()
    try:
        yield db
    finally:
        db.close()

def get_read_db():
    db=read_sessionlocal()
    try:
        yield db
    finally:
        db.close()
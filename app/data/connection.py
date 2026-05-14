from app.models import product
from app.data.data_base import sessionlocal, engine

def init_db():
    product.Base.metadata.create_all(bind=engine)

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()
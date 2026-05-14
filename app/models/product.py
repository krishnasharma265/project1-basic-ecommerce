from pydantic import ConfigDict
from sqlalchemy import Boolean, Column ,Integer,String,Float,ForeignKey

from sqlalchemy.orm import Mapped,relationship
from app.data.data_base import Base
# Base=declarative_base()

class Product(Base):
    __tablename__="product"
    __allow_unmapped__ = True
     
    id = Column(Integer, primary_key=True ,index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    category = Column(String)
    brand = Column(String)
    rating = Column(Float)
    is_available = Column(Boolean)


    user_id = Column(Integer, ForeignKey("user.id",ondelete="CASCADE"))
    model_config = ConfigDict(from_attributes=True)
    owner = relationship("User", back_populates="products")
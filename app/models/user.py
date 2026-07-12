
from sqlalchemy.orm import Mapped,relationship
from sqlalchemy import Boolean, Column ,Integer,String,Float
from app.data.data_base import Base
class User(Base):
    __tablename__="user"
    __allow_unmapped__=True

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)
    password=Column(String)
    #ownership
    products = relationship("Product", back_populates="owner")

    #roles
    role=Column(String,default="Customer")


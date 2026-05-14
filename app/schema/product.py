from pydantic import BaseModel,Field,ConfigDict,field_validator,model_validator
from typing import Optional,List
from fastapi import HTTPException
class ProductSchema(BaseModel):
    id:int
    name:str=Field(min_length=1,max_length=80)
    description:str
    price:float=Field(gt=0)
    stock:int=Field(ge=0)
    category:str
    brand:str
    rating:float
    is_available:bool

    model_config = ConfigDict(from_attributes=True)

    @field_validator("name",mode="after")
    @classmethod
    def validate_name(cls,value):
        if value.strip()=="":
            raise ValueError("name cannot be empty")
        return value
        
    @field_validator("price",mode="after")
    @classmethod
    def validate_price(cls,value):
        if value<0:
            raise ValueError("price cannot be -ve")
        elif isinstance(value,str):
            raise ValueError("price cannot be string")
        return value
    @model_validator(mode="after")
    @classmethod
    def validate_stock_is_available(cls,model:"ProductSchema"):
        if model.stock==0 and model.is_available==True:
            raise ValueError("if stock is 0 then is_available is must be False")
        elif model.stock!=0 and model.is_available==False:
            raise ValueError("if stock is not 0 then is_available is must be True")
        return model
        

    

class ProductCreate(BaseModel):
    name:str=Field(min_length=1,max_length=80)
    description:str
    price:float=Field(gt=0)
    stock:int=Field(ge=0)
    category: str
    brand: str
    rating:float=Field(ge=0,le=10)
    is_available:bool

    @field_validator("name",mode="after")
    @classmethod
    def validate_name(cls,value):
        if value.strip()=="":
            raise ValueError("name cannot be empty")
        return value
        
    @field_validator("price",mode="after")
    @classmethod
    def validate_price(cls,value):
        if value<0:
            raise ValueError("price cannot be -ve")
        elif isinstance(value,str):
            raise ValueError("price cannot be string")
        return value
    @model_validator(mode="after")
    @classmethod
    def validate_stock_is_available(cls,model:"ProductCreate"):
        if model.stock==0 and model.is_available==True:
            raise ValueError("if stock is 0 then is_available is must be False")
        elif model.stock!=0 and model.is_available==False:
            raise ValueError("if stock is not 0 then is_available is must be True")
        return model
        


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None,min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(default=None,gt=0)
    stock: Optional[int] = Field(default=None,ge=0)
    category: Optional[str] = None
    brand: Optional[str] = None
    rating:Optional[float] = Field(default=None,ge=0,le=10)
    is_available:Optional[bool] = None

    @field_validator("name",mode="after")
    @classmethod
    def validate_name(cls,value):
        if value.strip()=="":
            raise ValueError("name cannot be empty")
        return value
        
    @field_validator("price",mode="after")
    @classmethod
    def validate_price(cls,value):
        if value<0:
            raise ValueError("price cannot be -ve")
        elif isinstance(value,str):
            raise ValueError("price cannot be string")
        return value
    @model_validator(mode="after")
    @classmethod
    def validate_stock_is_available(cls,model:"ProductUpdate"):
        if model.stock==0 and model.is_available==True:
            raise ValueError("if stock is 0 then is_available is must be False")
        elif model.stock!=0 and model.is_available==False:
            raise ValueError("if stock is not 0 then is_available is must be True")
        return model
        

class ProductResponse(BaseModel):
    total:int
    limit:int
    offset:int
    items:List[ProductSchema]
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schema.product import ProductCreate,ProductUpdate
from app.models import product
from app.models.user import User
from sqlalchemy import asc,desc
from fastapi import HTTPException
from app.schema.response import APIResponse
from app.core.logging import logger

def get_product_list(db:Session,
                     name=None,
                     offset=None,
                     sort_by_price=False,
                     order="asc",
                     limit=10
                     ):
    products=db.query(product.Product)
    if name:
        products=products.filter(product.Product.name.ilike(f"%{name}%"))
    result=products.all()
       # ilike is for string
    if not result:
        # raise HTTPException(status_code=404,detail="product not found")
        return []
    
    if sort_by_price:
        if order=="asc":
            products=products.order_by(asc(product.Product.price))
        else:
            products=products.order_by(desc(product.Product.price))
    total=products.count()
    products=products.offset(offset).limit(limit)
    return {
        "total":total,
        "limit":limit,
        "offset":offset,
        "items":products.all()

    }
    # return APIResponse(
    #     success=True,
    #     message="Product fetched successfully",
    #     data={
    #     "total":total,
    #     "limit":limit,
    #     "offset":offset,
    #     "items":products.all()

    # }
    # )

def add_product(product:ProductCreate,db=Session,user=User):

    
    power=user.role
    if power=="seller":
        new_product=Product(**product.model_dump(),user_id=user.id)
    elif power=="admin":
        new_product=Product(**product.model_dump(),user_id=user.id)
    
    else:
        
        return APIResponse(
            success=False,
            message="you have no access to add products",
            data=None
        )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    logger.info(f"Product created with id {new_product.id}")
    # return new_product
    return APIResponse(
        success=True,
        message="Product fetched successfully",
        data=new_product
    )

def delete_product(id:int ,db:Session,user=User):
    power=user.role
    if power=="seller":
        dlt_prd=db.query(product.Product).filter(product.Product.id==id,
                                                product.Product.user_id==user.id).first()
    elif power=="admin":
        dlt_prd=db.query(product.Product).filter(product.Product.id==id).first()
    
    else:
        return APIResponse(
            success=False,
            message="you have no access to delete products",
            data=None
        )
    
    if not dlt_prd :
        
        if product.Product.user_id!=user.id:
            raise HTTPException(status_code=404,detail="You have no access to delete other's product")
        raise HTTPException(status_code=404,detail="Product not found")
        
        
    db.delete(dlt_prd)
    db.commit()
    logger.warning(f"Product deleted: {id}")
    # return {"Product deleted sucess-fully"}
    return APIResponse(
        success=True,
        message="Product fetched successfully",
        data=None
    )

def update_pdt(upd_product:ProductUpdate,id:int,db:Session,user=User):
    prod=db.query(product.Product).filter(product.Product.id==id,
                                          product.Product.user_id==user.id).first()
    power=user.role
    if power=="seller":
        prod=db.query(product.Product).filter(product.Product.id==id,
                                          product.Product.user_id==user.id).first()
    elif power=="admin":
        prod=db.query(product.Product).filter(product.Product.id==id).first()
    
    else:
        return APIResponse(
            success=False,
            message="you have no access to update products",
            data=None
        )

    if not prod :
        if product.Product.user_id!=user.id:
            raise HTTPException(status_code=404,detail="You have no access to update others product")
        raise HTTPException(status_code=404,detail="product not found")
   
    update_data=upd_product.model_dump(exclude_unset=True)

    for key , value in update_data.items():
        setattr(prod,key,value)

    db.commit()
    db.refresh(prod)
    logger.info(f"Product updated with id {id}")
    # return prod
    return APIResponse(
        success=True,
        message="Product fetched successfully",
        data=prod
    )
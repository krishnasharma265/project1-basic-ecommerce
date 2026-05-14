from fastapi import APIRouter,Depends,Query,HTTPException
# from data.data_base import sessionlocal,engine
from sqlalchemy.orm import Session
from app.models import product
from app.models.product import Product
from app.schema.product import ProductSchema,ProductCreate,ProductUpdate,ProductResponse
from app.data.connection import get_db
from app.services.auth import get_current_user
from app.services.product_services import get_product_list,add_product,delete_product,update_pdt
from app.schema.response import APIResponse
router=APIRouter()

#initiate database
# def get_db():
#     db=sessionlocal()
#     try:
#         yield db
#     finally:
#         db.close()
    
#home page
@router.get("/")
def home():
    return "hello"

@router.get("/my-products")
def get_my_products(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    products = db.query(product.Product).filter(
        product.Product.user_id == user.id
    ).all()
    return products

#show all products
# @app.get("/products",response_model=List[ProductSchema])
# def show_products(db:Session=Depends(get_db)):
#     products=db.query(product.Product).all()

#     return products


#products by name
@router.get("/products")
def list_products(user=Depends(get_current_user),
    db:Session=Depends(get_db),
    name:str=Query(default=None,min_length=1,max_length=50,description="search product by name"),
    sort_by_price:bool=Query(default=False,description="sort by price"),
    order:str=Query(default="asc",description="sort_by_price(asc,desc)"),
    limit:int=Query(default=10,description="no. of products shown"),
    offset:int=Query(default=0,description="pagination")

    ):
    return get_product_list(db=db,name=name,order=order,limit=limit,sort_by_price=sort_by_price,offset=offset)
    

#add new product
@router.post("/product",response_model=APIResponse[ProductSchema])
def add_new_product( 
    product:ProductCreate ,user = Depends(get_current_user), db:Session=Depends(get_db)):
    return add_product(product=product,user=user,db=db)

#delete by id
@router.delete("/product/{id}",response_model=APIResponse[ProductSchema])
def dlt_product(id:int, user = Depends(get_current_user),db:Session=Depends(get_db)):
    return delete_product(id=id,user=user,db=db)


@router.patch("/product/{id}",response_model=APIResponse[ProductSchema])
def update_product( id:int,upd_product:ProductUpdate ,user = Depends(get_current_user),db:Session=Depends(get_db)):
    return update_pdt(db=db,upd_product=upd_product,id=id,user=user)




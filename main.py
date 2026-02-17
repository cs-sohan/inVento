from fastapi import FastAPI, HTTPException, Query
from models import Product,ProductCreate,ProductUpdate,ProductListResponse
from uuid import UUID
from typing import Optional, Literal
from dummy_data import generate_dummy_data

app = FastAPI()

# Get initial products list
products : dict[UUID,Product] = {}
for product in generate_dummy_data():
    products[product.id] = product

@app.get("/")
def home():
    return {"message":"Hello, Welcome to the application!"}

@app.get("/products",response_model=ProductListResponse,tags=["Products"])
def get_all_products(
    skip: int = Query(0,ge=0),
    limit: int = Query(10,ge=1),
    min_price: Optional[float] = Query(None,gt=0),
    max_price: Optional[float] = Query(None,gt=0),
    search_filter: Optional[str] = None,
    sort_by: Optional[Literal['name','price','quantity']] = None,
    order: Literal['asc','desc'] = 'asc'
):
    product_list = list(products.values())
    # price filtering
    if min_price is not None:
        product_list = [p for p in product_list if p.price >= min_price]
    if max_price is not None:
        product_list = [p for p in product_list if p.price <= max_price]
    # search filter
    search_fields = ['name','description']
    if search_filter:
        search = search_filter.lower()
        product_list = [
            p for p in product_list 
            if any(
                search in (getattr(p,search_field) or "").lower()
                            for search_field in search_fields
                    )
                ]
    # sorting
    if sort_by:
        reverse = order == 'desc'
        product_list.sort(key=lambda p: getattr(p,sort_by), reverse=reverse)
    return {
        "total": len(product_list),
        "skip": skip,
        "limit": limit,
        "data": product_list[skip:skip+limit]
    }

@app.get("/products/{product_id}",response_model=Product,tags=["Products"])
def get_product_by_id(product_id: UUID):
    product = products.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product Not Found!")
    return product

@app.post("/products",response_model=Product,status_code=201,tags=["Products"])
def add_product(product:ProductCreate):
    new_product = Product(**product.model_dump())
    products[new_product.id] = new_product
    return new_product

@app.patch("/products/{product_id}",response_model=Product,tags=["Products"])
def update_product(product_id:UUID, product_update:ProductUpdate):
    existing_product = products.get(product_id)
    if existing_product is None:
        raise HTTPException(status_code=404,detail='Product Not Found!')
    product_changes = product_update.model_dump(exclude_unset=True)
    for key,value in product_changes.items():
        setattr(existing_product,key,value)
    return existing_product

@app.delete("/products/{product_id}",status_code=204,tags=["Products"])
def delete_product(product_id:UUID):
    deleted_product = products.pop(product_id,None)
    if deleted_product is None:
        raise HTTPException(status_code=404,detail='Product Not Found!')    
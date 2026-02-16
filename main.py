from fastapi import FastAPI, HTTPException
from models import Product,ProductCreate,ProductUpdate
from uuid import UUID

app = FastAPI()

products = [
    Product(name='IPhone',description="Apple Iphone",price=999,quantity=10),
    Product(name='Laptop',description="Good Quality laptop",price=1098,quantity=7),
    Product(name='Chair',description="Good Chair",price=36,quantity=58),
    Product(name='Chocolate',description="Tasty chocolate",price=5,quantity=98),
    Product(name='Gun',description="",price=999,quantity=1),
]

@app.get("/")
def greet():
    return {"message":"Hello, Welcome to the application!"}

@app.get("/products",response_model=list[Product],tags=["Products"])
def get_all_products():
    return products

@app.get("/products/{product_id}",response_model=Product,tags=["Products"])
def get_product_by_id(product_id: UUID):
    product = next((p for p in products if p.id == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product Not found!")
    return product

@app.post("/products",response_model=Product,status_code=201,tags=["Products"])
def add_product(product:ProductCreate):
    new_product = Product(**product.model_dump())
    products.append(new_product)
    return new_product

@app.patch("/products/{product_id}",response_model=Product,tags=["Products"])
def update_product(product_id:UUID, product_update:ProductUpdate):
    existing_product = next((p for p in products if p.id == product_id),None)
    if existing_product is None:
        raise HTTPException(status_code=404,detail='Product Not Found!')
    product_changes = product_update.model_dump(exclude_unset=True)
    for key,value in product_changes.items():
        setattr(existing_product,key,value)
    return existing_product

@app.delete("/products/{product_id}",status_code=204,tags=["Products"])
def delete_product(product_id:UUID):
    for index,product in enumerate(products):
        if product.id == product_id:
            del products[index]
            return
    raise HTTPException(status_code=404,detail='Product Not Found!')
    
from fastapi import FastAPI, HTTPException, Query, Depends
from models import Product, ProductCreate, ProductUpdate, ProductListResponse
from uuid import UUID
from typing import Optional, Literal
from dummy_data import generate_dummy_data
from services.product_service import ProductService

app = FastAPI()

# Get initial products list
products: dict[UUID, Product] = {}
for product in generate_dummy_data():
    products[product.id] = product


def get_product_service() -> ProductService:
    return ProductService(products)


@app.get("/")
def home():
    return {"message": "Hello, Welcome to the application!"}


@app.get("/products", response_model=ProductListResponse, tags=["Products"])
def get_all_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    min_price: Optional[float] = Query(None, gt=0),
    max_price: Optional[float] = Query(None, gt=0),
    search_filter: Optional[str] = None,
    sort_by: Optional[Literal["name", "price", "quantity"]] = None,
    order: Literal["asc", "desc"] = "asc",
    service: ProductService = Depends(get_product_service),
):
    return service.get_all(
        skip, limit, min_price, max_price, search_filter, sort_by, order
    )


@app.get("/products/{product_id}", response_model=Product, tags=["Products"])
def get_product_by_id(
    product_id: UUID, service: ProductService = Depends(get_product_service)
):
    product = service.get_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product Not Found!")
    return product


@app.post("/products", response_model=Product, status_code=201, tags=["Products"])
def add_product(
    product: ProductCreate, service: ProductService = Depends(get_product_service)
):
    return service.create(product)


@app.patch("/products/{product_id}", response_model=Product, tags=["Products"])
def update_product(
    product_id: UUID,
    product_update: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    updated_product = service.update(product_id, product_update)
    if not update_product:
        raise HTTPException(status_code=404, detail="Product Not Found!")
    return updated_product


@app.delete("/products/{product_id}", status_code=204, tags=["Products"])
def delete_product(
    product_id: UUID, service: ProductService = Depends(get_product_service)
):
    deleted = service.delete(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product Not Found!")

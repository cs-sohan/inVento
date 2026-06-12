from uuid import UUID
from schemas import Product
from services.product_service import ProductService
from dummy_data import generate_dummy_data

products: dict[UUID, Product] = {}
for product in generate_dummy_data():
    products[product.id] = product


def get_product_service() -> ProductService:
    return ProductService(products)

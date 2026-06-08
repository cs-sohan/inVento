from uuid import UUID
from models import Product, ProductCreate, ProductUpdate
from typing import Optional, Literal, Any


class ProductService:
    def __init__(self, products: dict[UUID, Product]):
        self.products = products

    def get_all(
        self,
        skip: int,
        limit: int,
        min_price: Optional[float],
        max_price: Optional[float],
        search_filter: Optional[str],
        sort_by: Optional[Literal["name", "price", "quantity"]],
        order: Literal["asc", "desc"],
    ) -> dict[str, Any]:
        product_list = list(self.products.values())
        # price filtering
        if min_price is not None:
            product_list = [p for p in product_list if p.price >= min_price]
        if max_price is not None:
            product_list = [p for p in product_list if p.price <= max_price]
        # search filter
        search_fields = ["name", "description"]
        if search_filter:
            search = search_filter.lower()
            product_list = [
                p
                for p in product_list
                if any(
                    search in (getattr(p, search_field) or "").lower()
                    for search_field in search_fields
                )
            ]
        # sorting
        if sort_by:
            reverse = order == "desc"
            product_list.sort(key=lambda p: getattr(p, sort_by), reverse=reverse)
        return {
            "total": len(product_list),
            "skip": skip,
            "limit": limit,
            "data": product_list[skip : skip + limit],
        }

    def get_by_id(self, product_id: UUID):
        return self.products.get(product_id)

    def create(self, product: ProductCreate):
        new_product = Product(**product.model_dump())
        self.products[new_product.id] = new_product
        return new_product

    def update(self, product_id: UUID, product_update: ProductUpdate):
        existing_product = self.get_by_id(product_id)
        if not existing_product:
            return None
        product_changes = product_update.model_dump(exclude_unset=True)
        for key, value in product_changes.items():
            setattr(existing_product, key, value)
        return existing_product

    def delete(self, product_id: UUID):
        return self.products.pop(product_id, None)

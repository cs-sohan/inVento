from pydantic import BaseModel,Field
from typing import Optional
from uuid import UUID, uuid4

class ProductBase(BaseModel):
    """
    Product Base Model
    """
    name: str = Field(...,min_length=3,max_length=100,description="Name of the product",examples=['car','bike','scooter'])
    description: Optional[str] = Field(None,max_length=1000,description="Description of the product")
    price: float = Field(...,gt=0,description="Product price should be greater than 0", examples=[102,399,105.50])
    quantity: int = Field(...,ge=0,description="Quantity of the product should be greater than or equal to 0", examples=[10,1,0])

class ProductCreate(ProductBase):
    """
    Model to create a new product
    """
    pass

class ProductUpdate(BaseModel):
    """
    Model to update existing product
    """
    name: Optional[str] = Field(None,min_length=3,max_length=100,description="Name of the product",examples=['car','bike','scooter'])
    description: Optional[str] = Field(None,max_length=1000,description="Description of the product")
    price: Optional[float] = Field(None,gt=0,description="Product price should be greater than 0", examples=[102,399,105.50])
    quantity: Optional[int] = Field(None,ge=0,description="Quantity of the product should be greater than or equal to 0", examples=[10,1,0])

class Product(ProductBase):
    """
    Full product model with product id
    """
    id: UUID = Field(default_factory=uuid4)

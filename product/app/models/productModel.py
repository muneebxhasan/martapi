from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class ProductBase(SQLModel):
    name: str
    description: str
    brand: Optional[str] = None
    category: str  
    model_config = {
        "arbitrary_types_allowed": True,
    } # type: ignore

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ratings: List["ProductRating"] = Relationship(back_populates="product")
    images: list["ProductImage"] = Relationship(back_populates="product")
    variation : List["ProductOption"] = Relationship(back_populates="product") 

class ProductImage(SQLModel, table = True):
    id:Optional[int] = Field(default=None,primary_key=True)
    product_id:int = Field(foreign_key="product.id")
    product : Product = Relationship(back_populates="images")
    url : str 

class ProductOption(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    product_id:int = Field(foreign_key="product.id")
    product : Product = Relationship(back_populates="variation")
    expiry: Optional[str] = None
    weight: Optional[float] = None
    price: float
    colour : str
    size : int


class ProductRating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    rating: int
    review: Optional[str] = None
    product: Product = Relationship(back_populates="ratings")
    user_id: int

    model_config = {
        "arbitrary_types_allowed": True,
    } # type: ignore



class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    expiry: Optional[str] = None
    brand: Optional[str] = None
    weight: Optional[float] = None
    category: Optional[str] = None

    model_config = {
        "arbitrary_types_allowed": True,
    } # type: ignore

class ProductList(SQLModel):
    products: List[Product]
    
    model_config = {
        "arbitrary_types_allowed": True,
    } # type: ignore

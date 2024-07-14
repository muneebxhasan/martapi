from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class ProductBase(SQLModel):
    name: str
    description: str
    brand: Optional[str] = None
    category: str

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    options: List["ProductOption"] = Relationship(back_populates="product")

class ProductImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_option_id: int = Field(foreign_key="productoption.id")
    product_option: "ProductOption" = Relationship(back_populates="images")
    url: str

class ProductOption(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="options")
    ratings: List["ProductRating"] = Relationship(back_populates="product_option")
    images: List[ProductImage] = Relationship(back_populates="product_option")
    expiry: Optional[str] = None
    weight: Optional[float] = None
    price: float
    colour: str
    size: int


class ProductRating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_option_id: int = Field(foreign_key="productoption.id")
    product_option: ProductOption = Relationship(back_populates="ratings")
    rating: int
    user_id: int

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    expiry: Optional[str] = None
    brand: Optional[str] = None
    weight: Optional[float] = None
    category: Optional[str] = None

class ProductRatingList(SQLModel):
    ratings: List[ProductRating]

class ProductList(SQLModel):
    products: List[Product]

# -----------------Product Create Models-----------------

class ProductImageCreate(SQLModel):
    product_option_id: int = Field(foreign_key="productoption.id")
    url: str

class ProductOptionCreate(SQLModel):
    
    product_id: int = Field(foreign_key="product.id")
    expiry: Optional[str] = None
    weight: Optional[float] = None
    price: float
    colour: str
    size: int
    stock: Optional[int]
    images: list[ProductImageCreate]


class ProductCreate(SQLModel):
    name: str
    description: str
    brand: Optional[str] = None
    category: str
    options : list[ProductOptionCreate]

# -----------------Product Response Models-----------------

class ProductImageRead(SQLModel):
    product_option_id: int
    url: str    
class ProductOptionRead(SQLModel):
    product_id: int
    expiry: Optional[str] = None
    weight: Optional[float] = None
    price: float
    colour: str
    size: int
   
    images: list[ProductImageRead]    

class ProductRead(SQLModel):
    name: str
    description: str
    brand: Optional[str] = None
    category: str
    options : list[ProductOptionRead]

#------------------------------------------------------------------



    


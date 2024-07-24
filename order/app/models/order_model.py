from sqlmodel import SQLModel , Field , Relationship
from datetime import datetime
from typing import List, Optional
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Orderr(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    creation_date: datetime = Field(default_factory=datetime.now)
    expected_delivery_date: datetime
    items : list["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    id: int = Field(primary_key=True)
    order_id: int = Field(foreign_key="orderr.id")
    order : Orderr = Relationship(back_populates="items")
    product_id: int
    option_id : int
    quantity: int
    price: float
    # seller_id: int

class OrderCreate(SQLModel):
    creation_date: datetime = Field(default_factory=datetime.now)
    expected_delivery_date: datetime


class OrderItemCreate(SQLModel):
   
    product_id: int
    option_id: int
    quantity: int
    price: float

class UserInfo(SQLModel):
    username: str
    id: int
    email: str
    full_name: str
    disabled: bool



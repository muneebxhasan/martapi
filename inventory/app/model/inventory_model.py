from typing import List
from sqlmodel import SQLModel, Field

class InventoryBase(SQLModel):
    product_id: int  
    variant_id: int
    quantity: int
    model_config = {
        "arbitrary_types_allowed": True,
    }

class Inventory(InventoryBase, table=True):
    id : int = Field(default=None, primary_key=True)
    model_config = {
        "arbitrary_types_allowed": True,
    }

class InventoryCreate(SQLModel):
    product_id: int
    variant_id: int
    quantity: int
    model_config = {
        "arbitrary_types_allowed": True,
    }

class InventoryList(SQLModel):
    inventory: List[Inventory]
    model_config = {
        "arbitrary_types_allowed": True,
    }

class InventoryUpdate(SQLModel):
    quantity: int
    variant_id: int
    model_config = {
        "arbitrary_types_allowed": True,
    }
from typing import List, Optional
from sqlmodel import SQLModel, Field

class InventoryBase(SQLModel):
    product_id: int  
    option_id: int
    quantity: int
    model_config = {
        "arbitrary_types_allowed": True,
    } # type: ignore

class Inventory(InventoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model_config = {
        "arbitrary_types_allowed": True,
    }# type: ignore


class InventoryList(SQLModel):
    inventory: List[Inventory]
    model_config = {
        "arbitrary_types_allowed": True,
    }# type: ignore

class InventoryUpdate(SQLModel):
    quantity: int
    model_config = {
        "arbitrary_types_allowed": True,
    }# type: ignore
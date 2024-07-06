from fastapi import APIRouter , HTTPException
from app.crud import inventory_crud
from app.model.inventory_model import Inventory , InventoryUpdate , InventoryList
from app.api.deps import DB_session
router = APIRouter()

@router.post("/add_inventoryItem", response_model=Inventory)
def add_inventoryItem(inventory_data: Inventory,session:DB_session):
    try:
        return inventory_crud.add_new_inventoryItem(inventory_data,session)
    except HTTPException as e:
        raise e
    #,response_model=InventoryList 
@router.get("/get_all_inventoryItems")
def get_all_inventoryItems(session:DB_session):
    try:
        return inventory_crud.get_all_inventoryItems(session)
    except HTTPException as e:
        raise e
    
@router.get("/get_inventoryItem_by_id/{inventory_id}",response_model=Inventory) 
def get_inventoryItem_by_id(inventory_id:int,session:DB_session):
    try:
        return inventory_crud.get_inventoryItem_by_id(inventory_id,session)
    except HTTPException as e:
        raise e
    

@router.put("/update_inventoryItem_by_id/{inventory_id}", response_model=InventoryUpdate)
def update_inventoryItem_by_id(inventory_id:int, to_update_inventory_data:InventoryUpdate,session:DB_session):
    try:
        return inventory_crud.update_inventoryItem_by_id(inventory_id,to_update_inventory_data,session)
    except HTTPException as e:
        raise e

@router.delete("/delete_inventoryItem_by_id/{inventory_id}")
def delete_inventoryItem_by_id(inventory_id:int,session:DB_session):
    try:
        return inventory_crud.delete_inventoryItem_by_id(inventory_id,session)
    except HTTPException as e:
        raise e        

    
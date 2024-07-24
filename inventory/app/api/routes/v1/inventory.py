from fastapi import APIRouter , HTTPException
from app.crud import inventory_crud
from app.model.inventory_model import Inventory , InventoryUpdate , InventoryList
from app.api.deps import DB_session
from app.api.deps import GetCurrentUserDep

router = APIRouter()

@router.post("/add_inventoryItem", response_model=Inventory)
def add_inventoryItem(inventory_data: Inventory,db:DB_session,current_user:GetCurrentUserDep):
    try:
        return inventory_crud.add_new_inventoryItem(inventory_data,db)
    except HTTPException as e:
        raise e
    #,response_model=InventoryList 
@router.get("/get_all_inventoryItems")
def get_all_inventoryItems(db:DB_session):
    try:
        return inventory_crud.get_all_inventoryItems(db)
    except HTTPException as e:
        raise e
    
@router.get("/get_inventoryItem_by_id/{inventory_id}",response_model=Inventory) 
def get_inventoryItem_by_id(inventory_id:int,db:DB_session):
    try:
        return inventory_crud.get_inventoryItem_by_id(inventory_id,db)
    except HTTPException as e:
        raise e
    

@router.put("/add_stock_by_product_id/{product_id}/{option_id}/{new_stock}", response_model=Inventory)
def add_stock_by_product_id(product_id:int,option_id:int,new_stock:int,db:DB_session):
    try:
        return inventory_crud.add_stock_by_product_id(product_id,option_id,new_stock,db)
    except HTTPException as e:
        raise e


@router.put("/update_inventoryItem_by_id/{inventory_id}", response_model=InventoryUpdate)
def update_inventoryItem_by_id(inventory_id:int, to_update_inventory_data:InventoryUpdate,db:DB_session):
    try:
        return inventory_crud.update_inventoryItem_by_id(inventory_id,to_update_inventory_data,db)
    except HTTPException as e:
        raise e

@router.delete("/delete_inventoryItem_by_id/{inventory_id}")
def delete_inventoryItem_by_id(inventory_id:int,db:DB_session):
    try:
        return inventory_crud.delete_inventoryItem_by_id(inventory_id,db)
    except HTTPException as e:
        raise e        

    
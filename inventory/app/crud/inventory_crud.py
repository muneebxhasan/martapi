from sqlmodel import  Session, select
from app.model.inventory_model import Inventory ,InventoryUpdate
from fastapi import HTTPException

def add_new_inventoryItem(inventory_data: Inventory, db:Session):
    try:
        db.add(inventory_data)        
        db.commit()
        db.refresh(inventory_data)
        return inventory_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add Inventory to database") from e



def get_all_inventoryItems(db:Session):
    inventory = db.exec(select(Inventory)).all()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found!!!")
    return inventory


def get_inventoryItem_by_id(inventory_id:int , db:Session):
    inventory = db.exec(select(Inventory).where(Inventory.id == inventory_id)).one_or_none()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found!!!")
    return inventory
    

def update_stock_by_product_id(product_id:int,option_id:int, new_stock:int, db:Session):
    inventory = db.exec(select(Inventory).where(Inventory.product_id == product_id, Inventory.option_id == option_id)).one_or_none()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found!!!")
    

    if inventory.quantity >= new_stock:
        inventory.quantity -= new_stock
    else:
        raise HTTPException(status_code=500, detail="Insufficient Stock!!!")

    db.add(inventory)
    db.commit()
    return inventory

def add_stock_by_product_id(product_id:int,option_id:int, new_stock:int, db:Session):
    inventory = db.exec(select(Inventory).where(Inventory.product_id == product_id, Inventory.option_id == option_id)).one_or_none()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found!!!")
    
    inventory.quantity += new_stock
    db.add(inventory)
    db.commit()
    return inventory

def update_inventoryItem_by_id(inventory_id:int, to_update_inventory_data:InventoryUpdate, db:Session):
    # Step 1: Get the Inventory by ID
    inventory = db.exec(select(Inventory).where(Inventory.id == inventory_id)).one_or_none()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found!!!")
    # Step 2: Update the Inventory
    inventory_data = to_update_inventory_data.model_dump(exclude_unset=True)
    inventory.quantity = inventory_data.get("quantity")
    db.add(inventory)
    db.commit()
    return inventory    


def delete_inventoryItem_by_id(inventory_id:int, db:Session):
    # Step 1: Get the Inventory by ID
    inventory = db.exec(select(Inventory).where(Inventory.id == inventory_id)).one_or_none()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found!!!")
    # Step 2: Delete the Inventory
    db.delete(inventory)
    db.commit()
    return {"message": "Inventory Deleted Successfully"}
from sqlmodel import  Session, select
from app.model.inventory_model import Inventory 
from fastapi import HTTPException

def add_new_inventoryItem(inventory_data: Inventory, session:Session):
    try:
        session.add(inventory_data)        
        session.commit()
        session.refresh(inventory_data)
        return inventory_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add Inventory to database") from e



def get_all_inventoryItems(session:Session):
    inventory = session.exec(select(Inventory)).all()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found!!!")
    return inventory


def get_inventoryItem_by_id(inventory_id:int , session:Session):
    inventory = session.exec(select(Inventory).where(Inventory.id == inventory_id)).one_or_none()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found!!!")
    return inventory
    

def update_inventoryItem_by_id(inventory_id:int, to_update_inventory_data:Inventory, session:Session):
    # Step 1: Get the Inventory by ID
    inventory = session.exec(select(Inventory).where(Inventory.id == inventory_id)).one_or_none()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found!!!")
    # Step 2: Update the Inventory
    inventory_data = to_update_inventory_data.model_dump(exclude_unset=True)
    inventory.sqlmodel_update(inventory_data)
    session.add(inventory)
    session.commit()
    return inventory    


def delete_inventoryItem_by_id(inventory_id:int, session:Session):
    # Step 1: Get the Inventory by ID
    inventory = session.exec(select(Inventory).where(Inventory.id == inventory_id)).one_or_none()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found!!!")
    # Step 2: Delete the Inventory
    session.delete(inventory)
    session.commit()
    return {"message": "Inventory Deleted Successfully"}
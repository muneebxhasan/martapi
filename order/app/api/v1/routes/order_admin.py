from fastapi import APIRouter, HTTPException,status,Depends
from app.crud import order_crud
from app.models.order_model import Orderr,OrderItem,OrderStatus
from app.api.dep import DB_session
router = APIRouter()
from enum import Enum

class Order_Status(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@router.delete("/user/{user_id}")
def delete_order_by_user_id(user_id:int,db:DB_session):
    return order_crud.delete_order_by_userid(user_id,db)

@router.delete("/{order_id}")
def delete_order_by_order_id(order_id:int,db:DB_session):
    return order_crud.delete_order_by_orderid(order_id,db)

@router.get("/status/{order_id}")
def get_status_by_order_id(order_id:int,db:DB_session):
    return order_crud.get_status_by_order_id(order_id,db)

@router.put("/status/{order_id}/{status}")
def update_status(order_id:int,status:OrderStatus,db:DB_session):
    current_status = order_crud.get_status_by_order_id(order_id, db)
    
    # Check if trying to change from "processing" to "pending"
    if current_status == Order_Status.PROCESSING and status == Order_Status.PENDING:
        raise HTTPException(status_code=400, detail="Cannot change status from processing to pending")
    # Allow changing status from "completed" to "processing"
    if current_status == Order_Status.COMPLETED and status == Order_Status.PROCESSING:
        order_crud.update_status(order_id, status, db)
        return {"status": "updated"}
    # Check if trying to cancel an order that is "shipped" or "delivered"
    if current_status in [Order_Status.SHIPPED, Order_Status.DELIVERED] and status == Order_Status.CANCELED:
        raise HTTPException(status_code=400, detail="Cannot cancel an order that is shipped or delivered")


    order_crud.update_status(order_id,status,db)
    return {"status":"updated"}

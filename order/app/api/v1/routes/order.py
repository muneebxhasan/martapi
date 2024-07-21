from fastapi import APIRouter, HTTPException
from app.crud import order_crud
from app.models.order_model import Orderr,OrderItem,OrderStatus
from app.api.dep import DB_session
from app.core.dep_kafka import Producer
from app.api.dep import GetCurrentAdminDep
router = APIRouter()


@router.post("/")
async def add_order(order:Orderr,order_item:list[OrderItem],db:DB_session,producer:Producer):
    try:
    
        order = await order_crud.add_order_details(order,order_item,db,producer)
        return order
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e
    
@router.get("/{user_id}")
def get_order_by_user_id(user_id:int,db:DB_session):
    try:
        return order_crud.get_all_orders_by_userid(user_id,db)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
       return e    

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
    order_crud.update_status(order_id,status,db)


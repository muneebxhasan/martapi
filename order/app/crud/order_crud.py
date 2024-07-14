from typing import List
from fastapi import HTTPException
from sqlmodel import Session,select
from app.models.order_model import Orderr,OrderItem,OrderStatus

def add_order_details(order:Orderr,order_item:list[OrderItem],session:Session):
    try:
        for item in order_item:
            order.items.append(item)
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
    except Exception as e:
        raise e
    
def get_all_orders_by_userid(user_id: int, session: Session) :
    result = session.exec(select(Orderr).where(Orderr.user_id == user_id))
    orders = result.all()  # Fetch all matching orders

    # List to store orders and their items
    orders_with_items = []

    for order in orders:
        order_data = {
            'order': order,
            'items': order.items  # Add the items of the order
        }
        orders_with_items.append(order_data)  # Add the order data to the list

    return orders_with_items


    # try:
    # result = session.exec(select(Orderr).where(Orderr.user_id == user_id))
    # orders = result.all()  # Fetch all matching orders
    # all_items = []
    # for order in orders:
    #     all_items.extend(order.items)  # Collect items from each order
    # all_items.sort(key=lambda x: x.expected_delivery_date)  # Sort items by expected delivery date
    # return all_items 
    # except Exception as e:

def delete_order_by_userid(user_id:int,session:Session):
    try:
        orders = session.exec(select(Orderr).where(Orderr.user_id == user_id)).all()
        for order in orders:
            session.delete(order)
        session.commit()
        return {"message":"Orders deleted successfully"}
    except Exception as e:
        raise e


def delete_order_by_orderid(order_id:int,session:Session):
    try:
        order = session.exec(select(Orderr).where(Orderr.id == order_id)).one_or_none()
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        session.delete(order)
        session.commit()
        return {"message":"Order deleted successfully"}
    except Exception as e:
        raise e

def get_status_by_order_id(order_id:int,session:Session):
    order = session.exec(select(Orderr).where(Orderr.id == order_id)).one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.status



def update_status(order_id:int,status:OrderStatus,session:Session):
   
        to_update = session.exec(select(Orderr).where(Orderr.id==order_id)).one()

        to_update.status = status
        session.add(to_update)
        session.commit()
        session.refresh(to_update)
    
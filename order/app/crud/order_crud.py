from fastapi import HTTPException
from sqlmodel import Session,select
from app.models.order_model import Orderr,OrderItem,OrderStatus
from app.core.dep_kafka import Producer
import json
from app import stock_pb2
# from app.api.dep import UserDep
 # Get user details
async def add_order_details(order:Orderr,order_item:list[OrderItem],db:Session,producer:Producer):
    # try:

        for item in order_item:
            order.items.append(item)
            # update_stock = {
            #     "product_id": item.product_id,
            #     "option_id": item.option_id,
            #     "quantity": item.quantity
            # }
            # update_stock = json.dumps(update_stock).encode("utf-8")
            protobuf_stock = stock_pb2.Stock(product_id=item.product_id,option_id=item.option_id,quantity=item.quantity)
            print("protobuf_stock",protobuf_stock)
            serialized_stock =protobuf_stock.SerializeToString()
            await producer.send_and_wait("update_stock",serialized_stock)


        db.add(order)
        db.commit()
        db.refresh(order)
         # Get user details
        notification = {
            "order_id": order.id,
            "user_id": order.user_id,
            "notification_id": "order_confirmation"
        }


        notification = json.dumps(notification).encode("utf-8")
        await producer.send_and_wait("order_conformation_notification",notification)
        return order
    # except Exception as e:
    #     raise e
    
def get_all_orders_by_userid(user_id: int, db: Session) :
    result = db.exec(select(Orderr).where(Orderr.user_id == user_id))
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
    # result = db.exec(select(Orderr).where(Orderr.user_id == user_id))
    # orders = result.all()  # Fetch all matching orders
    # all_items = []
    # for order in orders:
    #     all_items.extend(order.items)  # Collect items from each order
    # all_items.sort(key=lambda x: x.expected_delivery_date)  # Sort items by expected delivery date
    # return all_items 
    # except Exception as e:

def delete_order_by_userid(user_id: int, db: Session):
    try:
        # Step 1: Get all Orders by User ID
        orders = db.exec(select(Orderr).where(Orderr.user_id == user_id)).all()
        
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for this user")

        # Step 2: Delete all associated OrderItems for each Order
        for order in orders:
            for item in order.items:
                db.delete(item)
            db.delete(order)
        
        # Step 3: Commit the transaction
        db.commit()
        return {"message": "Orders deleted successfully"}
    
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of any error
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def delete_order_by_orderid(order_id:int,db:Session):
    try:
        order = db.exec(select(Orderr).where(Orderr.id == order_id)).one_or_none()
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        db.delete(order)
        db.commit()
        return {"message":"Order deleted successfully"}
    except Exception as e:
        raise e

def get_status_by_order_id(order_id:int,db:Session):
    order = db.exec(select(Orderr).where(Orderr.id == order_id)).one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.status



def update_status(order_id:int,status:OrderStatus,db:Session):
   
        to_update = db.exec(select(Orderr).where(Orderr.id==order_id)).one()

        to_update.status = status
        db.add(to_update)
        db.commit()
        db.refresh(to_update)
    
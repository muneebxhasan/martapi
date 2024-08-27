from fastapi import APIRouter, HTTPException,status,Depends
from app.crud import order_crud
from app.models.order_model import Orderr,OrderItem,OrderCreate,OrderItemCreate
from app.api.dep import DB_session
from app.core.dep_kafka import Producer
from app.api.dep import GetCurrentUserDep
import requests

router = APIRouter()


@router.post("/")
async def add_order(order: OrderCreate, order_item: list[OrderItemCreate], db: DB_session, producer: Producer, current_user: GetCurrentUserDep):
    try:
        total_price = sum(item.price * item.quantity for item in order_item)
        order = Orderr(**order.model_dump())
        order.user_id = current_user.get("id")
        order_item = [OrderItem(**item.model_dump()) for item in order_item]
        order = await order_crud.add_order_details(order, order_item, db, producer)

        # Prepare the data to send to the payment service
        checkout_payload = {
            "order_id": order.id,
            "user_id": order.user_id,
            "total_price": total_price,
        }

        # Call the payment service with the payload
        response = requests.post("http://payment_service:8090/create-checkout-session", json=checkout_payload)
        response_data = response.json()
        url = response_data.get("url")

        return {"order": order, "payment_url": url}
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
@router.get("/me")
def get_order_by_user_id(db:DB_session,current_user:GetCurrentUserDep):
    try:
        # print(user_id)
        # print(current_user)
        # print("here")
        user_id = current_user.get("id") 
        print("user_id",user_id)
        order = order_crud.get_all_orders_by_userid(user_id,db)
        return order  
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))    



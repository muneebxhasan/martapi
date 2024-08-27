
from app import setting
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import stripe
from fastapi.responses import FileResponse
from app.core.dep_kafka import Producer
import json
from fastapi.templating import Jinja2Templates

# This is your test secret API key.
stripe.api_key = str(setting.STRIPE_SECRET_KEY)
app = FastAPI(root_path="/payment-service",root_path_in_servers=True)

YOUR_DOMAIN = setting.YOUR_DOMAIN

# Mount the static files directory
app.mount("/app", StaticFiles(directory="public", html=True), name="static")
templates = Jinja2Templates(directory="public")



@app.get("/payment")
def serve_index():
    return FileResponse('public/checkout.html')


@app.get("/success")
async def success(request: Request, session_id: str, producer: Producer):
    try:
        # Retrieve the session from Stripe using the session_id
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Extract the order_id from the session's metadata
        order_id = session.metadata.get("order_id")
        user_id = session.metadata.get("user_id")
        to_send = {"order_id": order_id, "user_id": user_id}
        to_send = json.dumps(to_send).encode("utf-8")
        await producer.send_and_wait("payment", to_send)
        notification = {
            "order_id": order_id,
            "user_id": user_id,
            "notification_id": "payment_confirmation"
        }

        notification = json.dumps(notification).encode("utf-8")
        await producer.send_and_wait("order_conformation_notification",notification)

        # Pass order_id to the template
        return templates.TemplateResponse("success.html", {"request": request, "order_id": order_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve the session details")


@app.get("/cancel")
def cancel():
    return FileResponse('public/cancel.html')



@app.post('/create-checkout-session')
async def create_checkout_session(data: dict):
    order_id = data.get("order_id")
    user_id = data.get("user_id")
    total_price = data.get("total_price")
    
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # You can create a dynamic price or use a predefined price ID
                    'price': 'price_1PeIlzKm0VUH0UzjzsHyTHur',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"{YOUR_DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=YOUR_DOMAIN + '/cancel',
            metadata={
                "order_id": order_id,
                "user_id": user_id,
            },
        )
    except Exception as e:
        return str(e)
    # print(checkout_session.url)
    return {'url': checkout_session.url}


# @app.post('/create-checkout-session')
# async def create_checkout_session(data: dict):
#     order_id = data.get("order_id")
#     user_id = data.get("user_id")
#     total_price = data.get("total_price")
#     # # Create a Product
#     # product = stripe.Product.create(
#     #     name="Custom Product Name",
#     #     description="This is a custom product",
#     # )

#     # # Create a Price for the Product
#     # price = stripe.Price.create(
#     #     unit_amount=2000,  # Amount in cents (e.g., 2000 cents = $20.00)
#     #     currency="usd",
#     #     product=product.id,
#     # )
#     # price = stripe.Price.create(
#     #     unit_amount=2000,  # Amount in cents (e.g., 2000 cents = $20.00)
#     #     currency="usd",
#     #     recurring={"interval": "month"},
#     #     product=product.id,
#     # )
#     try:
#         checkout_session = stripe.checkout.Session.create(
#             line_items=[
#                 {
#                     # the exact Price ID (for example, pr_1234) of the product 
#                     'price': 'price_1PeIlzKm0VUH0UzjzsHyTHur',
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success',
#             cancel_url=YOUR_DOMAIN + '/cancel',
#         )
#     except Exception as e:
#         return str(e)
#     print(checkout_session.url)
#     # return RedirectResponse(url=checkout_session.url, status_code=303)
#     return {'url': checkout_session.url}

    
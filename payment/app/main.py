
from app import setting
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import stripe
from fastapi.responses import FileResponse


# This is your test secret API key.
stripe.api_key = str(setting.STRIPE_SECRET_KEY)
app = FastAPI()

YOUR_DOMAIN = setting.YOUR_DOMAIN

# Mount the static files directory
app.mount("/app", StaticFiles(directory="public", html=True), name="static")


@app.get("/payment")
def serve_index():
    return FileResponse('public/checkout.html')

@app.get("/success")
def success():
    return FileResponse('public/success.html')

@app.get("/cancel")
def cancel():
    return FileResponse('public/cancel.html')


@app.post('/create-checkout-session')
async def create_checkout_session(request: Request):
    # # Create a Product
    # product = stripe.Product.create(
    #     name="Custom Product Name",
    #     description="This is a custom product",
    # )

    # # Create a Price for the Product
    # price = stripe.Price.create(
    #     unit_amount=2000,  # Amount in cents (e.g., 2000 cents = $20.00)
    #     currency="usd",
    #     product=product.id,
    # )
    # price = stripe.Price.create(
    #     unit_amount=2000,  # Amount in cents (e.g., 2000 cents = $20.00)
    #     currency="usd",
    #     recurring={"interval": "month"},
    #     product=product.id,
    # )
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # the exact Price ID (for example, pr_1234) of the product 
                    'price': 'price_1PeIlzKm0VUH0UzjzsHyTHur',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
    except Exception as e:
        return str(e)

    return RedirectResponse(url=checkout_session.url, status_code=303)

    
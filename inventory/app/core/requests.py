from requests import get,post
from fastapi import HTTPException
from app.core.utils import load_error_json
from app import settings
import requests
from fastapi import HTTPException

def get_current_user(token: str):
    url = f"{settings.USER_SERVICE_URL}/v1/auth/user/me"
    headers = {
    "Authorization": f"Bearer {token}"
    # "Accept": "application/json"  # Ensure the server knows you want a JSON response
    }
    response = requests.get(url, headers=headers)
    
    
    if response.status_code == 200:
        return response.json()
    
    raise HTTPException(status_code=response.status_code, detail="Invalid token or authentication failed")


def login_for_access_token(form_data):
    url = f"{settings.USER_SERVICE_URL}/v1/auth/login/token"
    data = {
        "username": form_data.username,
        "password": form_data.password
    }
    response = post(url, data=data)
    print("RESPONSE STATUS CODE", response.status_code)
    if response.status_code == 200:
        return response.json()
    
    raise HTTPException(status_code=response.status_code, detail=load_error_json(response))


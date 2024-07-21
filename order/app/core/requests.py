from requests import get,post
from fastapi import HTTPException
from app.core.utils import load_error_json
from app import setting

def get_current_user(token: str):
    url = f"{setting.USER_SERVICE_URL}/v1/auth/user/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = get(url, headers=headers)

    print( "AUTHENTICATED_USER_DATA" ,response.json())

    if response.status_code == 200:
        return response.json()
    
    raise HTTPException(status_code=response.status_code, detail=load_error_json(response))


def login_for_access_token(form_data):
    url = f"{setting.USER_SERVICE_URL}/api/v1/login/access-token"
    data = {
        "username": form_data.username,
        "password": form_data.password
    }
    response = post(url, data=data)

    if response.status_code == 200:
        return response.json()
    
    raise HTTPException(status_code=response.status_code, detail=load_error_json(response))


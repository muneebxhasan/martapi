from requests import get


def get_user():
    user = get('http://user_api:8004/v1/user/1')
    
    return user.json()



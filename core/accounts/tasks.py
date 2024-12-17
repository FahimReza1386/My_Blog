from core.celery import app
from time import sleep
import requests


@app.task
def send_email():
    sleep(10)
    print("Email Sended.")

@app.task
def get_posts():
    login_url = "http://172.17.0.1:8000/accounts/api/v1/jwt/login/" 
    data={
        "email":"Fahim@gmail.com",
        "password":"Fahim2684"
    }
    login_response = requests.post(login_url, data=data)
    # بررسی وضعیت پاسخ ورود
    if login_response.status_code == 200:
        token = login_response.json().get('access')
        if token:
            headers = {
                'Authorization': f'Bearer {token}'
            }
            posts_url = "http://172.17.0.1:8000/api/v1/Blog/"
            
            # ارسال درخواست برای دریافت پست‌ها
            response2 = requests.get(posts_url, headers=headers)
            return response2.json()
        else:
            raise Exception("Token not found in the login response")
    else:
        raise Exception(f"Login failed with status code {login_response.status_code}")

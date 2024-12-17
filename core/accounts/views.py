from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .tasks import *
import requests
# Create your views here.

def sendEmail(request):
    send_email.delay()
    return HttpResponse("<h1> email sended .</h1>")


#  روش به صورت دستی

def Login_jwt(request):
    if cache.get("access_jwt") is None:
        sleep(5)
        data={
            "email":"Fahim@gmail.com",
            "password":"Fahim2684"
        }
        response= requests.post("http://172.17.0.1:8000/accounts/api/v1/jwt/login/" , data=data)
        cache.set("access_jwt" , response.json(),60)
    return JsonResponse({"detail":cache.get("access_jwt")})



#  روش دوم به صورت دکوراتور
cache_page(60)
def Login_jwt2(request):
    sleep(5)
    data={
            "email":"Fahim@gmail.com",
            "password":"Fahim2684"
    }
    response= requests.post("http://172.17.0.1:8000/accounts/api/v1/jwt/login/" , data=data)
    return JsonResponse({"detail":response.json()})
from django.shortcuts import render
from django.http import HttpResponse
from .tasks import *
# Create your views here.

def sendEmail(request):
    send_email.delay()
    return HttpResponse("<h1> email sended .</h1>")
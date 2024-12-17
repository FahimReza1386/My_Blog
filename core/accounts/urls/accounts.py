from django.urls import path , include
from .. import views

urlpatterns = [
    path("" , include("django.contrib.auth.urls")),
    path("send_Email/" , views.sendEmail),
    path("login_cache/" , views.Login_jwt),
    path("login_cache2/" , views.Login_jwt2),
    path("api/v1/" , include("accounts.api.v1.urls")),
]
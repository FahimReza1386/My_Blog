from django.urls import path , include
from .. import views

urlpatterns = [
    path("" , include("django.contrib.auth.urls")),
    path("send_Email/" , views.sendEmail),
    path("api/v1/" , include("accounts.api.v1.urls")),
]
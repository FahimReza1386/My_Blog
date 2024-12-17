from django.urls import path
from .. import views


urlpatterns = [
    path("", views.ProfileApi.as_view(), name="ProfileApi"),
]

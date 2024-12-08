from django.urls import path, include
from .. import views


urlpatterns =[ 
    path('' , views.ProfileApi.as_view() , name="ProfileApi"),
]
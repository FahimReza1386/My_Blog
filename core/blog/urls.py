from . import views 
from django.urls import path,include

urlpatterns =[
    path('' , views.IndexPage.as_view() , name="IndexPage"),
    path('api/v1' , include('blog.api.v1.urls')),
]
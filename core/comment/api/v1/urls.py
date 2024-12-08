from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register("Comment" , views.CommentApiView , basename="Comments")
urlpatterns=router.urls
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter # type: ignore


app_name = 'api-v1'

router = DefaultRouter()
router.register('Blog' , views.BlogModelView , basename='Blogs')

urlpatterns = router.urls
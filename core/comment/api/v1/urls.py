from . import views
from rest_framework.routers import DefaultRouter

app_name = "comment-api-v1"

router = DefaultRouter()
router.register("Comment", views.CommentApiView, basename="Comments")
urlpatterns = router.urls

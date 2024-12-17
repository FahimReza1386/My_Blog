from django.urls import path, include
from . import views

urlpatterns = [
    path("like-comment/", views.LikeComments.as_view(), name="LikeComment"),
    path("add_comment/<int:pk>/", views.AddComment.as_view(), name="AddComment"),
    path("del_comment/<int:pk>/", views.DeleteComment.as_view(), name="DeleteComment"),
    path("api/v1/", include("comment.api.v1.urls")),
]

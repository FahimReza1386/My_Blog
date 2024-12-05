from . import views 
from django.urls import path,include

urlpatterns =[
    path('' , views.IndexPage.as_view() , name="IndexPage"),
    path('create_post/' , views.CreatePost.as_view() , name="CreatePost"),
    path('my_blogs/' , views.MyBlogs.as_view() , name="MyBlogs"),
    path('details_post/<int:pk>/' , views.DetailsPost.as_view() , name="DetailsPost"),
    path('checkLike_post/', views.CheckLikePost.as_view(), name='CheckLikePost'),
    path('like-comment/', views.LikeComments.as_view(), name='LikeComment'),
    path('add_comment/<int:pk>/', views.AddComment.as_view(), name='AddComment'),
    path('del_comment/<int:pk>/', views.DeleteComment.as_view(), name='DeleteComment'),
    path('api/v1' , include('blog.api.v1.urls')),
]
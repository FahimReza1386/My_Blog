from . import views 
from django.urls import path,include

urlpatterns =[
    path('' , views.IndexPage.as_view() , name="IndexPage"),
    path('view_api/' , views.PostViewApi.as_view() , name="PostViewApi"),
    path('create_post/' , views.CreatePost.as_view() , name="CreatePost"),
    path('delete_post/<int:pk>/' , views.DeletePost.as_view() , name="DeletePost"),
    path('edit_post/<int:pk>/' , views.EditPost.as_view() , name="EditPost"),
    path('my_blogs/' , views.MyBlogs.as_view() , name="MyBlogs"),
    path('details_post/<int:pk>/' , views.DetailsPost.as_view() , name="DetailsPost"),
    path('checkLike_post/', views.CheckLikePost.as_view(), name='CheckLikePost'),
    path('api/v1/' , include('blog.api.v1.urls')),
]
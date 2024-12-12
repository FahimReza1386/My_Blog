from accounts.models import User, Profile
from blog.models import Post, Category
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentApiSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter , SearchFilter
from comment.models import Comments, Comment_Like
from accounts.models import User, Profile
from blog.models import Post, Category
from .pagination import CustomPagination
from .permissons import IsOwnerChanged

class CommentApiView(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated , IsOwnerChanged]
    serializer_class = CommentApiSerializer
    queryset=Comments.objects.all()
    filter_backends=[DjangoFilterBackend, SearchFilter , OrderingFilter]
    # pagination_class=CustomPagination
    filterset_fields={
        "user":["exact"],
        "post":["exact"],
    }
    search_fields=["text"]
    ordering_fields=["star"]

    http_method_names = ['get', 'post' , "delete"]

    
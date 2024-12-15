from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter , OrderingFilter 
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ...models import Post
from .serializers import *
from .paginations import My_Paginations
from rest_framework.pagination import PageNumberPagination


class BlogModelView(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class = BlogModelSerializer
    queryset=Post.objects.all()
    filter_backends=[DjangoFilterBackend, SearchFilter , OrderingFilter]
    pagination_class=My_Paginations
    filterset_fields={
        "category": ["exact"],
        "owner": ["exact"],
        "status": ["exact"],
    }
    search_fields=["title", "content"]
    ordering_fields=["id"]

          

    @action(methods=["GET"], detail=False)
    def get_email(self, request):
        if request.user.is_authenticated:
            obj=get_object_or_404(User , email=request.user)
            return Response({'detail':obj.email})
        else:
            return Response({'details':"You must login to your account.."})


class CategoryModelView(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class=CategorySerializer
    queryset=Category.objects.all()
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    pagination_class=My_Paginations
    filterset_fields={
        "name":["exact"],
    }
    search_fields=["name"]
    ordering_fields=["id"]

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

class BlogModelView(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class = BlogModelSerializer
    queryset=Post.objects.all()
    filter_backends=[DjangoFilterBackend, SearchFilter , OrderingFilter]
    filterset_fields={
        "category": ["exact", "in"],
        "owner": ["exact"],
        "status": ["exact"],
    }
    search_fields=["title", "content"]
    ordering_fields=["category"]
          

    @action(methods=["GET"], detail=False)
    def get_email(self, request):
        if request.user.is_authenticated:
            obj=get_object_or_404(User , email=request.user)
            return Response({'detail':obj.email})
        else:
            return Response({'details':"You must login to your account.."})

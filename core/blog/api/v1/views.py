from rest_framework import viewsets # type: ignore
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly # type: ignore
from rest_framework.filters import SearchFilter , OrderingFilter # type: ignore
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore


class BlogModelView(viewsets.ModelViewSet):
    pass
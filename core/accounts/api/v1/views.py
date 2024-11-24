from django.contrib.auth import get_user_model
from django.http import HttpResponse 
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import generics, status # type: ignore
from rest_framework.response import Response # type: ignore

User = get_user_model()


class RegistrationApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer= self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {'email':email}
            
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

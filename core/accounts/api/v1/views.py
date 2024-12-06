from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, ChangePasswordSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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



class CustomChangePasswordApi(generics.GenericAPIView):
    serializer_class =  ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self):
        obj = self.request.user
        return obj
    

    def put(self , request, *args, **kwargs):
        self.object = self.get_object()
        serializer=self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password':'Wrong Password.'},status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()

            return Response({'details':'password changed success .'} , status=status.HTTP_200_OK)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
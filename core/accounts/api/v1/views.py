from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import generics, status 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from mail_templated import send_mail  # type: ignore
from mail_templated import EmailMessage  # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView  # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError  # type: ignore
import jwt
from .utils import EmailThread


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
    

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = ObtainAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer= self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user= serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token":token.key , "user_id":user.pk ,"email":user.email})

            

class CustomObtainDiscardAuthToken(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class CustomObtainTokenPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairViewSerializer

class CustomTokenRefreshView(TokenRefreshView):
    pass

class CustomTokenVerifyView(TokenVerifyView):
    pass


class AccountActivation(APIView):
    def get(self , request , token , *args , **kwargs):
        try:
            token = jwt.decode(token , settings.SECRET_KEY , algorithms=["HS256"])
            user_id = token.get('user_id')
        except ExpiredSignatureError:
            return Response(
                {"details": "Token Has Been Expired . "},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "Token Is Not Valid . "},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Get Object
        users=get_object_or_404(User , id=user_id)
        if users.is_verified:
            return Response({"details": "your account is verified ."})
        else:
            users.is_verified = True
            users.save()

            return Response({"details": "your account have been verified and activated successfully ."})



class ResentAccountActivation(generics.GenericAPIView):
    serializer_class=ResentActivationSerializer

    def post(self , request , *args, **kwargs):
        serializer =self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user']
        token = self.get_tokens_for_user(user_obj)
        email_obj=EmailMessage("email/activation_email.tpl" , {"token":token},"fahimreza20200@gmail.com" , to=[user_obj.email])
        EmailThread(email_obj).start()
        return Response(
            {"details": "user activation resent successfully ."},
            status=status.HTTP_200_OK,
        )
    

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

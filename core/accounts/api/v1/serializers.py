from rest_framework import serializers # type: ignore
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from ...models import User,Profile
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # type: ignore


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length = 255 , write_only=True)


    class Meta:
        model=User
        fields = ["email" , "password" , "password1"]

    def validation(self,attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({'detail':'passwords doe`s not matched .'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages) })
        return super().validation(attrs=attrs)
    
    def create(self , validated_data):
        validated_data.pop("password1" , None)
        return User.objects.create_user(**validated_data)
        

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True) 
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)


    def validate(self , attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "passwords dose`nt match"})
        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password':list(e.messages)})
        return super().validate(attrs=attrs)




class ObtainAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"),write_only=True) 
    password= serializers.CharField(label = _("Password") , style={"input_type":'password'},trim_whitespace=False , write_only=True)
    token=serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username=attrs.get("email")
        password=attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),username=username,password=password
            )

            if not user:
                msg= _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg , code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError({"detail": "user is not verified ."})
            
        else:
            msg=_('Must include "username" and "password".')
            raise serializers.ValidationError(msg , code="authorization")
        
        attrs["user"]=user
        return attrs
    

class TokenObtainPairViewSerializer(TokenObtainPairSerializer):
    def validate(self , attrs):
        validated_date = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"detail": "user is not verified ."})
        validated_date['email']=self.user.email
        validated_date['user_id']=self.user.id
        return validated_date
    


class ResentActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user_obj = get_object_or_404(User , email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"details": "user does not exist"})
        
        if user_obj.is_verified:
            raise serializers.ValidationError(
                {"details": "user is already activated and verified ."}
            )

        attrs["user"] = user_obj
        return super().validate(attrs)









# ------------------------Profile Api Serializer------------------------ #

class ProfileApiSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="User.email" , read_only=True)
    class Meta:
        model=Profile
        fields=['id',"email","first_name","last_name","image"]
        
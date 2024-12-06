from rest_framework import serializers # type: ignore
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from ...models import User
from django.core import exceptions
from django.utils.translation import gettext_lazy as _

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
    
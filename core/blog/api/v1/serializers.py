from rest_framework import serializers # type: ignore
from django.contrib.auth.password_validation import validate_password
from accounts.models import User
from django.core import exceptions


class TaskSerializer(serializers.ModelSerializer):

    absolute_url = serializers.SerializerMethodField()

    def get_absolute_url(self , obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self , instance):
        reps = super().to_representation(instance)

        request = self.context.get('request')
        if request.parser_context.get('kwargs').get('pk'):
            reps.pop('absolute_url')

        return reps

            
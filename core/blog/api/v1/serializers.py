from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from accounts.models import User,Profile
from blog.models import Post, Category

class BlogModelSerializer(serializers.ModelSerializer):
    snipped = serializers.ReadOnlyField(source="get_snipped")
    absolute_url=serializers.SerializerMethodField()
    relative_url = serializers.URLField(source="get_absolute_api_url" , read_only=True)
    category=serializers.SlugRelatedField(many=False, slug_field="name", queryset=Category.objects.all())

    class Meta:
        model=Post
        fields=["id","image","title","snipped","content","status","category","published_date","absolute_url","relative_url"]

    def create(self, validated_data):
        prf=Profile.objects.get(user__id=self.context.get('request').user.id)
        validated_data['owner']=prf
        return super().create(validated_data)
    

    def get_absolute_url(self , obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        tx = super().to_representation(instance)

        request = self.context.get('request')
        if request.parser_context.get("kwargs").get('pk'):
            tx.pop('absolute_url')
            tx.pop('relative_url')
            tx.pop('snipped')

            tx["state"]="single"

        else:
            tx.pop('content')
            tx["state"]="list"


        tx["category"]= CategorySerializer(instance.category , context={"request":request}).data

        return tx
    


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=["id","name"]
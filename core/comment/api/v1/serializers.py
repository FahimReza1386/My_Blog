from rest_framework import serializers
from comment.models import Comments
from accounts.models import Profile
from blog.models import Post
from blog.api.v1.serializers import BlogModelSerializer


class CommentApiSerializer(serializers.ModelSerializer):

    absolute_url = serializers.SerializerMethodField()
    post = serializers.SlugRelatedField(
        many=False, slug_field="title", queryset=Post.objects.all()
    )

    class Meta:
        model = Comments
        fields = ["id", "text", "post", "star", "created_date", "absolute_url"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        prf = Profile.objects.get(user__id=self.context.get("request").user.id)
        validated_data["user"] = prf
        return super().create(validated_data)

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        reps = super().to_representation(instance)

        request = self.context.get("request")

        if request.parser_context.get("kwargs").get("pk"):
            reps.pop("absolute_url")
            reps["state"] = "single"

        else:
            reps["state"] = "list"

            reps["post"] = BlogModelSerializer(
                instance.post, context={"request": request}
            ).data
            reps["post"].pop("image")
            reps["post"].pop("category")
            reps["post"].pop("status")
            reps["post"].pop("published_date")
            reps["post"].pop("absolute_url")
            reps["post"].pop("relative_url")
        return reps

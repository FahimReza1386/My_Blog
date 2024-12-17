from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Comments, Comment_Like
from django.contrib.auth import get_user_model
from django.views import View
from blog.models import Post
from accounts.models import Profile

# Create your views here.

User = get_user_model()


class LikeComments(View):
    def post(self, request):
        if request.method == "POST":
            user = User.objects.get(id=request.POST["user"])
            comment = Comments.objects.get(id=request.POST["comment"])

            like, created = Comment_Like.objects.get_or_create(
                user=user, comment=comment
            )

            if created:
                return JsonResponse({"isLiked": True})
            else:
                like.delete()
                return JsonResponse({"isLiked": False})
        else:
            return JsonResponse({"error": "Invalid request"}, status=400)


class AddComment(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            post = get_object_or_404(Post, id=kwargs["pk"])

            comment_text = request.POST["comment"]
            star = request.POST["star"]

            if comment_text and star:
                try:
                    star = int(star)
                    prf = Profile.objects.get(user=request.user)
                    Comments.objects.create(
                        user=prf, text=comment_text, post=post, star=star
                    )
                    messages.success(request, "کامنت شما با موفقیت اضافه شد ...")
                    return redirect(f"/details_post/{kwargs['pk']}/")
                except ValueError:
                    return JsonResponse({"error": "Invalid star value"}, status=400)
            else:
                return JsonResponse(
                    {"error": "Comment text and star are required"}, status=400
                )

        else:
            return JsonResponse({"error": "User is not authenticated"}, status=401)


class DeleteComment(View):
    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            comment = get_object_or_404(Comments, id=kwargs["pk"])
            comment.delete()
            return redirect(f"/details_post/{comment.post.id}/")
        else:
            messages.error(request, "لطفا اول به حساب خود وارد شوید ...")
            return redirect(f"/details_post/{comment.post.id}/")

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import CreateView,UpdateView,DeleteView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .models import Post, Category
from accounts.models import Profile
from .forms import CreatePostForm
from comment.models import Comment_Like, Comments
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class IndexPage(TemplateView):
    template_name = 'Blog/index.html'

    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        post=Post.objects.all()
        category=Category.objects.all()
        context["posts"] = post
        context["categories"] = category
        return context
    
class CreatePost(LoginRequiredMixin,CreateView):
    model = Post
    template_name = "Blog/AddPost.html"
    success_url = "/"
    form_class = CreatePostForm

    def form_valid(self, form):
        prf = Profile.objects.get(user=self.request.user)
        form.instance.owner = prf
        return super().form_valid(form)
    


class DetailsPost(DetailView):
    template_name = 'Blog/post_detail.html'
    model = Post

    def get(self, request, *args, **kwargs):
        self.object=self.get_object()
        context = self.get_context_data(object=self.object)
        context['posts']=Post.objects.filter(id=self.object.id)
        context['comments']=Comments.objects.filter(post=self.object.id)
        print(context['comments'])
        return self.render_to_response(context)
    
class CheckLikePost(View):
    def get(self, request):
        # اگر کاربر لاگین کرده باشد
        if request.user.is_authenticated:
            user = request.user
            liked_comments = Comment_Like.objects.filter(user=user).values_list('comment_id', flat=True)  # اطمینان از استفاده صحیح از نام فیلد
            return JsonResponse({'likedComments': list(liked_comments)})
        else:
            return JsonResponse({'likedComments': []})
        
class LikeComments(View):
    def post(self, request):
        if request.method == 'POST':
            user = User.objects.get(id=request.POST['user'])
            comment = Comments.objects.get(id=request.POST['comment'])

            # بررسی اینکه آیا این کامنت قبلاً لایک شده است یا خیر
            like, created = Comment_Like.objects.get_or_create(user=user, comment=comment)

            if created:  # اگر لایک جدید ایجاد شد
                return JsonResponse({'isLiked': True})
            else:  # اگر لایک قبلاً وجود داشت و حذف شد
                like.delete()
                return JsonResponse({'isLiked': False})
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)

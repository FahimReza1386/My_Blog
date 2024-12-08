from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse , HttpResponse
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import CreateView,UpdateView,DeleteView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .models import Post, Category
from accounts.models import Profile
from .forms import *
from comment.models import Comment_Like, Comments
from django.contrib.auth import get_user_model
import jdatetime # type: ignore

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
        for post in context["posts"]:
            g_date = post.published_date  # تاریخ میلادی از نمونه
            j_date = jdatetime.datetime.fromgregorian(datetime=g_date)
        formatted_date = f"{j_date.year}/{j_date.month}/{j_date.day}"
        context['post_published_date']=formatted_date
        return context
    
class MyBlogs(TemplateView):
    template_name='Blog/My_Blogs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prf=get_object_or_404(Profile , user=self.request.user)
        post=Post.objects.filter(owner=prf)
        context['posts']=post
        for post in context["posts"]:
            if post:
                g_date = post.published_date
                j_date = jdatetime.datetime.fromgregorian(datetime=g_date)
            else:
                pass
            formatted_date = f"{j_date.year}/{j_date.month}/{j_date.day}"
            context['post_published_date']=formatted_date
        category=Category.objects.all()
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

class DeletePost(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        post=Post.objects.get(id=kwargs['pk'])
        post.delete()
        return redirect('/my_blogs/')
    
class EditPost(LoginRequiredMixin,UpdateView):
    model=Post
    template_name="Blog/EditView.html"
    success_url='/my_blogs/'
    form_class=EditView



class DetailsPost(DetailView):
    template_name = 'Blog/post_detail.html'
    model = Post

    def get(self, request, *args, **kwargs):
        self.object=self.get_object()
        context = self.get_context_data(object=self.object)
        context['posts']=Post.objects.filter(id=self.object.id)
        context['comments']=Comments.objects.filter(post=self.object.id)
        for post in context["posts"]:
            if post:
                g_date = post.published_date
                j_date = jdatetime.datetime.fromgregorian(datetime=g_date)
            else:
                pass
            formatted_date = f"{j_date.year}/{j_date.month}/{j_date.day}"
            context['post_published_date']=formatted_date

        for comment in context['comments']:
            if comment:
                k_date = comment.created_date
                l_date = jdatetime.datetime.fromgregorian(datetime=k_date)
            else:
                pass
            formatted_date2 = f"{l_date.year}/{l_date.month}/{l_date.day}"
            context['comment_created_date']=formatted_date2
        context['prf']=get_object_or_404(Profile ,user=request.user)
        return self.render_to_response(context)
    
    
class CheckLikePost(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            liked_comments = Comment_Like.objects.filter(user=user).values_list('comment_id', flat=True)  # اطمینان از استفاده صحیح از نام فیلد
            return JsonResponse({'likedComments': list(liked_comments)})
        else:
            return JsonResponse({'likedComments': []})
 
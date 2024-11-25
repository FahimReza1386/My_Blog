from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView,UpdateView,DeleteView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .models import Post, Category
from accounts.models import Profile
from .forms import CreatePostForm
from comment.models import Comment_Like, Comments

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

    
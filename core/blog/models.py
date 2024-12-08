from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.

user = get_user_model()

class Post(models.Model):
    
    owner = models.ForeignKey("accounts.Profile" , on_delete=models.CASCADE)
    image= models.ImageField(upload_to='post_image/' , null=True , blank=True)
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=200)
    status= models.BooleanField(default=False)
    category = models.ForeignKey("Category" , on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.title}"

    def get_snipped(self):
        return self.content[0:5]
    
    def get_absolute_api_url(self):
        return reverse("Blog:api-v1:Blogs-detail" , kwargs={"pk":self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Comments(models.Model):
    user = models.ForeignKey("accounts.Profile" , on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    post = models.ForeignKey('blog.Post' , on_delete=models.CASCADE , null=True)
    star = models.IntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True , null=True)
    updated_date = models.DateTimeField(auto_now=True , null=True)
    
    def like_count(self):
        return self.comment_liked.count()


class Comment_Like(models.Model):
    comment = models.ForeignKey(Comments, related_name='comment_liked', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comment', 'user')

    def __str__(self):
        return f'{self.comment} {self.user}'

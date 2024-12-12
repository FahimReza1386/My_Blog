from django.test import TestCase
from django.urls import reverse, resolve
from accounts.models import User, Profile
from blog.models import Post,Category
from ..models import Comments, Comment_Like
from ..views import *
from datetime import datetime


class TestCommentUrl(TestCase):

    def test_add_comment_url(self):
        url = reverse("AddComment" , kwargs={"pk":1})
        self.assertEquals(resolve(url).func.view_class , AddComment)

    def test_delete_comment_url(self):
        url = reverse("DeleteComment" , kwargs={"pk":1})
        self.assertEquals(resolve(url).func.view_class , DeleteComment)
    def test_like_comment_url(self):
        url = reverse("LikeComment")
        self.assertEquals(resolve(url).func.view_class , LikeComments)
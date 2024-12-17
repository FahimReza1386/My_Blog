from django.test import TestCase, Client
from accounts.models import User, Profile
from blog.models import Post, Category
from ..models import Comment_Like, Comments
from datetime import datetime


class TestCommentModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="Ali@gmail.com", password="a@/1234567"
        )
        self.profile = Profile.objects.get(user=self.user)
        self.category = Category.objects.create(name="Test.")
        self.post = Post.objects.create(
            owner=self.profile,
            title="Test Post.",
            content="This is a Post for Tests.",
            status=True,
            category=self.category,
            published_date=datetime.now(),
        )
        self.comment = Comments.objects.create(
            user=self.profile, text="Test Comment.", post=self.post, star=3
        )

    def test_create_comment(self):
        self.client.force_login(self.user)

        comment = self.comment

        self.assertTrue(Comments.objects.filter(text=comment.text).exists())

    def test_delete_comment(self):
        self.client.force_login(self.user)

        comment = self.comment
        comment.delete()

        self.assertFalse(Comments.objects.filter(text=comment.text).exists())

    def test_Create_like_Comment(self):
        self.client.force_login(self.user)

        comment = self.comment
        Comment_Like.objects.create(comment=self.comment, user=self.user)

        self.assertTrue(Comment_Like.objects.filter(comment=comment).exists())

    def test_delete_like_Comment(self):
        self.client.force_login(self.user)

        comment_liked = Comment_Like.objects.filter(
            comment=self.comment, user=self.user
        )
        comment_liked.delete()

        self.assertFalse(Comment_Like.objects.filter(comment=self.comment).exists())

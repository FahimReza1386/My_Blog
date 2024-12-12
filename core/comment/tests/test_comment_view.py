from django.test import TestCase , Client
from django.urls import reverse
from accounts.models import User, Profile
from blog.models import Post, Category
from ..models import Comments, Comment_Like
from datetime import datetime


class TestCommentView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user=User.objects.create_user(email="Ali@gmail.com" , password="a@/1234567")
        self.profile=Profile.objects.get(user=self.user)
        self.category=Category.objects.create(name="Test.")
        self.post = Post.objects.create(
            owner=self.profile,
            title="Test Post.",
            content = "This is a Post for Tests.",
            status=True,
            category=self.category,
            published_date=datetime.now()
        )
        self.comment=Comments.objects.create(
            user=self.profile,
            text="Test Comment.",
            post=self.post,
            star=3
        )
    
    def test_comment_like_view(self):
        self.client.force_login(self.user)
        url = reverse("LikeComment")
        
        data = {
            'user': self.user.id,
            'comment': self.comment.id,
        }

        response = self.client.post(url, data)

        like = Comment_Like.objects.filter(user=self.user, comment=self.comment).first()
        self.assertIsNotNone(like)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, data)

        like = Comment_Like.objects.filter(user=self.user, comment=self.comment).first()
        self.assertIsNone(like)

        self.assertEqual(response.status_code, 200)

    def test_comment_addComment_view(self):
        self.client.force_login(self.user)
        url = reverse("AddComment" , kwargs={"pk":self.post.id})

        data={
            "user":self.profile.id,
            "comment":"This is a Test Comment.",
            "post":self.post.id,
            "star":2,
        }
        response=self.client.post(url , data)
        self.assertEquals(response.status_code , 302)
        self.assertTrue(Comments.objects.filter(post=data["post"] , text=data["comment"]).exists())



    def test_comment_delete_view(self):
        self.client.force_login(self.user)

        url = reverse("DeleteComment" , kwargs={"pk" : self.comment.id})

        response=self.client.delete(url)
        self.assertEquals(response.status_code , 302)
        self.assertFalse(Comments.objects.filter(id=self.comment.id).exists())
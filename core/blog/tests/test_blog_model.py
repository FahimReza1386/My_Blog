from django.test import TestCase
from blog.models import Post, Category
from accounts.models import User, Profile
from datetime import datetime
class TestBlogModel(TestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(email="fahim123@gmail.com",password="Hosseini123")
        self.profile=Profile.objects.create(user=self.user)


    def test_create_post_and_category(self):
        category=Category.objects.create(name="Test Cat")
        post=Post.objects.create(
            owner=self.profile,
            title="Test 1",
            content="This is a Test Post.",
            image=None,
            status=True,
            category=category,
            published_date=datetime.now()
        )

        self.assertTrue(Post.objects.filter(id=post.id).exists())
        self.assertTrue(Category.objects.filter(id=category.id).exists())
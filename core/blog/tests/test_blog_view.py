from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Profile
from ..models import Post, Category
from datetime import datetime


class TestBlogView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="fahim123@gmail.com", password="Hosseini123"
        )
        self.profile = Profile.objects.create(user=self.user)
        self.category = Category.objects.create(name="TestCat")
        self.post = Post.objects.create(
            owner=self.profile,
            title="Test1",
            content="This is a Test Post.",
            image="111",
            category=self.category,
            status=True,
            published_date=datetime.now(),
        )

    def test_blog_index_response_200(self):
        url = reverse("IndexPage")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(str(response.content).find("IndexPage"))
        self.assertTemplateUsed(response, template_name="Blog/index.html")

    # def test_blog_my_blogs_response_200(self):
    #     self.client.force_login(self.user)
    #     url= reverse("MyBlogs")

    #     response= self.client.get(url)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTrue(str(response.content).find("MyBlogs"))
    #     self.assertTemplateUsed(response, template_name="My_Blogs.html")

    def test_blog_post_create_post(self):
        self.client.force_login(self.user)
        url = reverse("CreatePost")
        response = self.client.get(url)
        post = self.post
        post.save()
        self.assertEquals(response.status_code, 200)
        self.assertTrue(Post.objects.filter(id=post.id).exists())

    def test_blog_delete_post(self):
        self.client.force_login(self.user)
        url = reverse("DeletePost", kwargs={"pk": self.post.pk})

        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=self.post.pk).exists())

    def test_blog_edit_post(self):
        self.client.force_login(self.user)
        url = reverse("EditPost", kwargs={"pk": self.post.pk})

        post = self.post
        post.title = "EditedPost"
        post.content = "The Post Successfully Changed."
        post.save()

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.post.title == "EditedPost")
        self.assertTrue(self.post.content == "The Post Successfully Changed.")

    def test_blog_details_post(self):
        url = reverse("DetailsPost", kwargs={"pk": self.post.pk})
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "Blog/post_detail.html")

    def test_check_like_post(self):
        url = reverse("CheckLikePost")
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

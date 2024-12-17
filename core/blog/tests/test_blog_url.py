from django.test import TestCase
from django.urls import reverse, resolve
from ..views import (
    IndexPage,
    MyBlogs,
    CreatePost,
    DeletePost,
    EditPost,
    DetailsPost,
    CheckLikePost,
)


class TestBlogUrl(TestCase):

    def test_blog_index_url(self):
        url = reverse("IndexPage")
        self.assertEquals(resolve(url).func.view_class, IndexPage)

    def test_blog_my_blogs(self):
        url = reverse("MyBlogs")
        self.assertEquals(resolve(url).func.view_class, MyBlogs)

    def test_blog_create_post(self):
        url = reverse("CreatePost")
        self.assertEquals(resolve(url).func.view_class, CreatePost)

    def test_blog_delete_post(self):
        url = reverse("DeletePost", kwargs={"pk": 1})
        self.assertEquals(resolve(url).func.view_class, DeletePost)

    def test_blog_edit_post(self):
        url = reverse("EditPost", kwargs={"pk": 1})
        self.assertEquals(resolve(url).func.view_class, EditPost)

    def test_blog_details_post(self):
        url = reverse("DetailsPost", kwargs={"pk": 1})
        self.assertEquals(resolve(url).func.view_class, DetailsPost)

    def test_blog_checkLike_post(self):
        url = reverse("CheckLikePost")
        self.assertEquals(resolve(url).func.view_class, CheckLikePost)

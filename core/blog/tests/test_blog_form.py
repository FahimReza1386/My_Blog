from django.test import TestCase
from ..models import Post, Category
from ..forms import CreatePostForm, EditView
from datetime import datetime


class TestPostForm(TestCase):

    def test_post_from_valid_data(self):
        category = Category.objects.create(name="Test")
        form = CreatePostForm(data={
            "title":"Test 1",
            "image":None,
            "content":"Hi This is a Test Post. ",
            "category":category,
            "published_date":datetime.now()
        })

        self.assertTrue(form.is_valid())

    def test_post_no_data(self):
        form=CreatePostForm(data={})
        self.assertFalse(form.is_valid())

    def test_blog_form_edit_post(self):
        category = Category.objects.create(name="Test2")
        
        form=EditView(data={
            "title":"Test 2",
            "image":None,
            "content":"Test Changed .",
            "category":category,
            "published_date":datetime.now()
        })


        self.assertTrue(form.is_valid())
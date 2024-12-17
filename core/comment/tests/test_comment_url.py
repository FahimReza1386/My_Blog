from django.test import TestCase
from django.urls import reverse, resolve
from comment.views import AddComment, DeleteComment, LikeComments


class TestCommentUrl(TestCase):

    def test_add_comment_url(self):
        url = reverse("AddComment", kwargs={"pk": 1})
        self.assertEquals(resolve(url).func.view_class, AddComment)

    def test_delete_comment_url(self):
        url = reverse("DeleteComment", kwargs={"pk": 1})
        self.assertEquals(resolve(url).func.view_class, DeleteComment)

    def test_like_comment_url(self):
        url = reverse("LikeComment")
        self.assertEquals(resolve(url).func.view_class, LikeComments)

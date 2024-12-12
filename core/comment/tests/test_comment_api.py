from django.urls import reverse
from accounts.models import User, Profile
from blog.models import Post, Category
from comment.models import Comments, Comment_Like
from rest_framework.test import APIClient
from datetime import datetime
import pytest



@pytest.fixture
def api_client():
    client= APIClient()
    return client

@pytest.fixture
def get_user():
    user= User.objects.create_user(email="admin@gmail.com" , password="a/@123456")
    return user

@pytest.fixture
def get_category():
    cat = Category.objects.create(name='Test')
    return cat

@pytest.fixture
def get_profile(get_user):
    prf = Profile.objects.get(user=get_user)
    return prf

@pytest.fixture
def get_post(get_profile):
    category=Category.objects.create(name="Test")
    prf = get_profile
    post=Post.objects.create(
        owner=prf,
        title="TestAPi",
        content="This is a Post Test.",
        status=True,
        category= category,
        published_date=datetime.now()
    )
    return post


@pytest.fixture
def get_comment(get_profile , get_post):
    profile=get_profile
    post=get_post
    comment= Comments.objects.create(
        user=profile,
        text="Test Comment.",
        post=post,
        star=3
    )
    return comment


@pytest.mark.django_db
class TestCommentApi:

    def test_get_allComment_response_200(self , api_client, get_user):
        user=get_user   
        api_client.force_login(user=user)

        url = reverse("comment-api-v1:Comments-list")

        response= api_client.get(url)
        assert response.status_code == 200

    def test_create_comment_response_201(self , api_client, get_user, get_post , get_comment):
        user=get_user   
        api_client.force_login(user=user)
        url = reverse("comment-api-v1:Comments-list")

        data = {
            "text":"This is a Test Comment.",
            "post":get_post,
            "star":3,
        }

        response= api_client.post(url , data)
        assert response.status_code == 201
        assert get_comment.__class__.objects.filter(text=data["text"],post=data["post"]).exists()

    def test_get_comment_response_200(self , get_user , get_comment , api_client):
        user=get_user   
        api_client.force_login(user=user)

        comment=get_comment
        url = reverse("comment-api-v1:Comments-detail" , kwargs={"pk":  comment.id})

        response= api_client.get(url)
        assert response.status_code == 200


    def test_delete_comment_response_204(self , get_user , get_comment , api_client):
        user=get_user   
        api_client.force_login(user=user)

        comment=get_comment
        url = reverse("comment-api-v1:Comments-detail" , kwargs={"pk":  comment.id})

        response= api_client.delete(url)
        assert response.status_code == 204
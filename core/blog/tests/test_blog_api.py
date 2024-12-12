from accounts.models import User, Profile
from blog.models import Post, Category
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
import pytest

@pytest.fixture
def api_client():
    client= APIClient()
    return client

@pytest.fixture
def get_user():
    user= User.objects.create_user(email="Fahim@gmail.com" , password="Fahim2684")
    return user

@pytest.fixture
def get_category():
    category=Category.objects.create(name="Test")
    return category

@pytest.fixture
def get_post(get_category, get_user):
    user=get_user
    prf=Profile.objects.get(user=user)
    post=Post.objects.create(
        owner=prf,
        title="TestAPi",
        content="This is a Post Test.",
        status=True,
        category= get_category,
        published_date=datetime.now()
    )
    return post

@pytest.mark.django_db
class TestBlogApi:

    def test_api_get_post_response_200(self , api_client , get_user):
        user=get_user
        api_client.force_login(user=user)
        url= reverse("api-v1:Blogs-list")

        response= api_client.get(url)
        assert response.status_code == 200

    def test_api_create_post_response_200(self, api_client , get_category, get_user) :
        api_client.force_login(get_user)
        url = reverse("api-v1:Blogs-list")

        data={
            
            "title": "TestAPi",
            "content": "This is a Post Test.",
            "status": True,
            "category": get_category,
            "published_date": datetime.now()

        }
        response= api_client.post(url , data)
        assert response.status_code == 201


    def test_api_get_post_response_200(self , api_client, get_user , get_post):
        user= get_user
        api_client.force_login(user=user)

        post_id=get_post.id
        url = reverse("api-v1:Blogs-detail" , kwargs={"pk":post_id})

        response = api_client.get(url)
        assert response.status_code == 200 



    def test_api_delete_post_response_204(self , api_client, get_user , get_post):
        user= get_user
        api_client.force_login(user=user)

        post_id=get_post.id
        url = reverse("api-v1:Blogs-detail" , kwargs={"pk":post_id})
        
        response= api_client.get(url)
        assert response.status_code == 200

        response = api_client.delete(url)
        assert response.status_code == 204  


    def test_api_edit_post_response_200(self , api_client, get_user , get_post , get_category):
        user= get_user
        api_client.force_login(user=user)

        post_id=get_post.id
        url = reverse("api-v1:Blogs-detail" , kwargs={"pk":post_id})

        data={
            "title": "Test Changed .",
            "content": "This is a Post Changed .",
            "status": True,
            "category": get_category.name,
            "published_date": datetime.now()
        }
          
        response= api_client.get(url)
        assert response.status_code == 200

        response= api_client.put(url , data , format="json")
        assert response.status_code == 200

        post_changed = get_post.__class__.objects.get(id=post_id)

        assert post_changed.title == data["title"]
        assert post_changed.content == data["content"]
        assert post_changed.status == data["status"]


    def test_api_get_all_categories_response_200(self , api_client , get_user):
        user= get_user
        api_client.force_login(user=user)

        url = reverse("api-v1:Categories-list")
        response = api_client.get(url)

        assert response.status_code == 200

    def test_api_get_category_detail_response_200(self , api_client , get_user, get_category):
        user= get_user
        api_client.force_login(user=user)

        category=get_category

        url = reverse("api-v1:Categories-detail" , kwargs={"pk":category.id})
        response = api_client.get(url)

        assert response.status_code == 200

    def test_api_create_category_response_201(self , api_client , get_user , get_category):
        user = get_user
        api_client.force_login(user=user)

        url = reverse("api-v1:Categories-list")

        data = {
            "name" : "Test_Cat"
        }
        response = api_client.post(url , data)
        assert response.status_code == 201
        assert get_category.__class__.objects.filter(name=data["name"]).exists()

    def test_api_delete_category_response_204(self , get_user , get_category , api_client):
        user = get_user
        api_client.force_login(user=user)
        
        category=get_category
        url = reverse("api-v1:Categories-detail" , kwargs={"pk":category.id})

        response = api_client.delete(url)
        
        assert response.status_code == 204
        assert get_category.__class__.objects.filter(id=category.id).exists() == False


    def test_api_edit_category_response_200(self , api_client , get_user , get_category):
        user = get_user 
        api_client.force_login(user=user)
        category=get_category
        url = reverse("api-v1:Categories-detail" , kwargs={"pk":category.id})

        data={
            "name" : "Changed."
        }

        response = api_client.put(url , data)
        assert response.status_code == 200

        changed_category=get_category.__class__.objects.get(id=category.id)
        assert changed_category.name == data["name"]

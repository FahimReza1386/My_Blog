from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Category
from comment.models import Comments, Comment_Like
from datetime import datetime
import random
import requests

class Command(BaseCommand):
    def __init__(self,*args , **kwargs):
        super().__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        user=User.objects.create_user(email=self.faker.email() , password=self.faker.password())
        user.is_verified = True
        user.save()

        image_url = f'https://picsum.photos/200/200?random={random.randint(1, 1000)}'

        response = requests.get(image_url)
        image_name = f'{self.faker.uuid4()}.jpg'

        prf = Profile.objects.get(user=user)
        prf.first_name=self.faker.first_name()
        prf.last_name=self.faker.last_name()
        prf.image=ContentFile(response.content, image_name)
        prf.description=self.faker.paragraph(nb_sentences=3)
        prf.save()

        ss=list(Post.objects.all())


        for _ in range(5):
            Comments.objects.create(
                user=prf,
                text=self.faker.paragraph(nb_sentences=1),
                post=random.choice(ss),
                star=random.choice([1,2,3,4,5])
            )

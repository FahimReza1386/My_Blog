from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Category
from django.core.files.base import ContentFile
from datetime import datetime
import random
import requests

category_name = ["سیاسی", "محلی", "اخبار", "حوادث"]

class Command(BaseCommand):

    help = "inserting dummy data."


    def __init__(self, *args , **kwargs):
        super().__init__(*args, **kwargs)
        self.faker=Faker()


    def handle(self, *args, **options):
        user =User.objects.create_user(email=self.faker.email(), password=self.faker.password())

        user.is_verified=True
        user.save()

        image_url = f'https://picsum.photos/200/200?random={random.randint(1, 1000)}'

        response = requests.get(image_url)
        image_name = f'{self.faker.uuid4()}.jpg'
    
        prf=Profile.objects.create(user=user)
        prf.first_name=self.faker.first_name()
        prf.last_name=self.faker.last_name()
        prf.image=ContentFile(response.content, image_name)
        prf.description=self.faker.paragraph(nb_sentences=3)
     

        prf.save()

        

        for name in category_name:
            Category.objects.get_or_create(name=name)
        
        for _ in range(10):
            Post.objects.create(
                owner=prf,
                title=self.faker.paragraph(nb_sentences=1),
                content=self.faker.paragraph(nb_sentences=5),
                image=ContentFile(response.content, image_name),
                status=random.choice([True, False]),
                category=Category.objects.get(name=random.choice(category_name)),
                published_date=datetime.now(),
            )

            

        

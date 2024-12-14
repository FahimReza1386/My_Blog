from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Category
<<<<<<< HEAD
from django.core.files.base import ContentFile
from datetime import datetime
import random
import requests
=======
from datetime import datetime
import random
>>>>>>> 31fc3ef (Create The Faker Data For Post)

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

<<<<<<< HEAD
        image_url = f'https://picsum.photos/200/200?random={random.randint(1, 1000)}'

        response = requests.get(image_url)
        image_name = f'{self.faker.uuid4()}.jpg'
    
        prf=Profile.objects.create(user=user)
        prf.first_name=self.faker.first_name()
        prf.last_name=self.faker.last_name()
        prf.image=ContentFile(response.content, image_name)
        prf.description=self.faker.paragraph(nb_sentences=3)
     

=======
        prf=Profile.objects.create(user=user)
        prf.first_name=self.faker.first_name()
        prf.last_name=self.faker.last_name()
        prf.description=self.faker.paragraph(nb_sentences=3)
>>>>>>> 31fc3ef (Create The Faker Data For Post)
        prf.save()

        

        for name in category_name:
            Category.objects.get_or_create(name=name)
        
<<<<<<< HEAD
        for _ in range(10):
=======

        for _ in range(10):
            image_url = self.faker.image_url()  # یک URL تصادفی برای تصویر فیک
>>>>>>> 31fc3ef (Create The Faker Data For Post)
            Post.objects.create(
                owner=prf,
                title=self.faker.paragraph(nb_sentences=1),
                content=self.faker.paragraph(nb_sentences=5),
<<<<<<< HEAD
                image=ContentFile(response.content, image_name),
=======
>>>>>>> 31fc3ef (Create The Faker Data For Post)
                status=random.choice([True, False]),
                category=Category.objects.get(name=random.choice(category_name)),
                published_date=datetime.now(),
            )

            

        

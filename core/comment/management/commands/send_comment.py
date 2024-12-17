from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Category
from comment.models import Comments, Comment_Like
from datetime import datetime
from PIL import Image
from io import BytesIO
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

        image= Image.open(BytesIO(response.content))

        image_size = len(response.content)

        if image_size > 1048576:
            image = self.resize_image(image)
        
        image_file= self.save_image(image)

        prf = Profile.objects.get(user=user)
        prf.first_name=self.faker.first_name()
        prf.last_name=self.faker.last_name()
        prf.image=image_file
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


    def resize_image(self , image):
        image = image.resize((800,800) , Image.ANTIALIAS)
        return image

    def save_image(self , image):
        img_io = BytesIO()
        image.save(img_io, format="JPEG" , quality=85)
        img_io.seek(0)
        return ContentFile(img_io.read(), name="image.jpg")
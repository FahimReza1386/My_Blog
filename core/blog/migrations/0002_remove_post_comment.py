# Generated by Django 3.2.25 on 2024-11-21 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comment',
        ),
    ]

# Generated by Django 3.2.25 on 2024-11-25 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20241125_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='comments',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

# Generated by Django 3.2.25 on 2024-11-25 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0002_comments_comment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comments",
            old_name="comment",
            new_name="post",
        ),
        migrations.AddField(
            model_name="comments",
            name="star",
            field=models.IntegerField(default=0),
        ),
    ]

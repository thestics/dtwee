# Generated by Django 4.1.7 on 2023-03-22 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dtwee_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tweet", name="like_count", field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="tweet",
            name="reply_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="tweet",
            name="retweet_count",
            field=models.IntegerField(default=0),
        ),
    ]

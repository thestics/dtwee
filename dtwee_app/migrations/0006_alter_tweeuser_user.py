# Generated by Django 4.1.7 on 2023-03-27 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dtwee_app", "0005_alter_useraction_tweet_alter_useraction_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tweeuser",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="twee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
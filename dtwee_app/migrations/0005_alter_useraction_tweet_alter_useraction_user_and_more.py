# Generated by Django 4.1.7 on 2023-03-27 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("dtwee_app", "0004_useraction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraction",
            name="tweet",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user_actions",
                to="dtwee_app.tweet",
            ),
        ),
        migrations.AlterField(
            model_name="useraction",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user_actions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="TweeUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("avatar", models.FileField(upload_to="media/avatars")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ext",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 2.2.16 on 2022-04-14 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("reviews", "0001_initial"),
        ("titles", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="reviews",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="reviews",
            name="title",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="titles.Title",
            ),
        ),
        migrations.AddField(
            model_name="comments",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comments",
            name="review",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="reviews.Reviews",
            ),
        ),
    ]

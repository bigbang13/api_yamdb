# Generated by Django 2.2.16 on 2022-04-18 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0004_auto_20220418_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
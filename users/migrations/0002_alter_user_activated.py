# Generated by Django 4.2.7 on 2023-12-14 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
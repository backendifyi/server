# Generated by Django 4.1.7 on 2023-06-19 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailbox', '0006_emailmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmodel',
            name='total_request',
            field=models.IntegerField(default=0),
        ),
    ]
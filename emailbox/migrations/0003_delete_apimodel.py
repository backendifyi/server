# Generated by Django 4.1.7 on 2023-06-14 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailbox', '0002_alter_apimodel_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='APIModel',
        ),
    ]

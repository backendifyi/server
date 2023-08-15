# Generated by Django 4.1.7 on 2023-06-10 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0006_remove_accesstokenmodel_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenModel',
            fields=[
                ('token', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='AccessTokenModel',
        ),
    ]
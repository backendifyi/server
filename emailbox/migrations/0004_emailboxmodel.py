# Generated by Django 4.1.7 on 2023-06-14 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_projectmodel_product'),
        ('emailbox', '0003_delete_apimodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailBoxModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.projectmodel')),
            ],
        ),
    ]
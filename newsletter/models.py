from django.db import models

# Create your models here.
class EmailModel(models.Model):
    email = models.EmailField()

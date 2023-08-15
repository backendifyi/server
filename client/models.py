from django.db import models
from django.contrib.auth.models import User

class ClientProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    image_url = models.URLField(null=True)

    def __str__(self):
        return self.name

class AccessTokenModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email




# Create your models her

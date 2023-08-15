from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ProjectModel(models.Model):
    PRODUCT_CHOICES = [
        ('EMAILBOX', 'EMAILBOX'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    product = models.CharField(max_length=20, choices=PRODUCT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Other fields of your model

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"{self.name} {self.user.email}"

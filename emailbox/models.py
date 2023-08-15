from django.db import models
from django.contrib.auth.models import User

from project.models import ProjectModel

class EmailBoxModel(models.Model):
    project = models.OneToOneField(ProjectModel, on_delete=models.CASCADE)

    #
    def __str__(self):
        return self.project.name

class EmailModel(models.Model):
    emailbox = models.ForeignKey(EmailBoxModel, on_delete=models.CASCADE)
    email_address = models.EmailField()
    time_added = models.DateTimeField(auto_now_add=True)
    total_request = models.IntegerField(default=0)
    is_valid = models.BooleanField(null=True, default=None)
    syntax_error_status = models.BooleanField(null=True, default=None)
    role_status = models.BooleanField(null=True, default=None)
    disposable_status = models.BooleanField(null=True, default=None)
    free_status = models.BooleanField(null=True, default=None)
    dns_status = models.BooleanField(null=True, default=None)
    role = models.CharField(max_length=100, null=True, default=None)
    disposable_provider = models.CharField(max_length=100, null=True, default=None)
    domain = models.CharField(max_length=100, null=True, default=None)
    account = models.CharField(max_length=100, null=True, default=None)

    def __str__(self):
        return f"{self.email_address} in {self.emailbox.project.name}"

class InstantReplyModel(models.Model):
    email = models.ForeignKey(EmailModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


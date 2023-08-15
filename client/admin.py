from django.contrib import admin

# Register your models here.
from .models import ClientProfileModel, AccessTokenModel

admin.site.register(ClientProfileModel)
admin.site.register(AccessTokenModel)

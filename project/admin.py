from django.contrib import admin
from .models import ProjectModel

class ProjectModelAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'user', 'key', 'name', 'product')
admin.site.register(ProjectModel), ProjectModelAdmin

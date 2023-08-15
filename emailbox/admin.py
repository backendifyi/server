from django.contrib import admin
from .models import EmailModel, EmailBoxModel, InstantReplyModel

admin.site.register(EmailModel)
admin.site.register(EmailBoxModel)
admin.site.register(InstantReplyModel)
from django.urls import path
from .views import ProjectView, APIKeyView

urlpatterns = [
    path('apikey/', APIKeyView.as_view(), name="apikey"),
    path('name/', ProjectView.as_view(), name="project")
]

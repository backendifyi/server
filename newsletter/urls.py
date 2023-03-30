from django.urls import path

from .views import NewsEmailView

urlpatterns = [
    path("", NewsEmailView.as_view(), name="newletter")
]

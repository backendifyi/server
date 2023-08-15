from django.urls import path
from .views import EmailBoxView, EmailboxListView, EmailView, AllEmailView, InstantView, CSVView

urlpatterns = [
    path('', EmailBoxView.as_view(), name="emailbox"),
    path('list/', EmailboxListView.as_view(), name="emailboxlist"),
    path('addEmail/', EmailView.as_view(), name="addEmail"),
    path('allEmails/', AllEmailView.as_view(), name="allEmail"),
    path('instantReply/', InstantView.as_view(), name="instantReply"),
    path('csv/', CSVView.as_view(), name="csv")
]

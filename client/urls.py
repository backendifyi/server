from django.urls import path
from .views import GoogleAuthURLView, GoogleAuthCallbackView, ProfileView, LogoutView, PageAuthView

urlpatterns = [
    path('auth/google/url/', GoogleAuthURLView.as_view(), name='google_auth_url'),
    path('auth/google/callback/', GoogleAuthCallbackView.as_view(), name='google_auth_callback'),
    path('auth/page/', PageAuthView.as_view(), name='page_auth'),
    path('profile/', ProfileView.as_view(),name="profile"),
    path('logout/', LogoutView.as_view(), name="logout")
]

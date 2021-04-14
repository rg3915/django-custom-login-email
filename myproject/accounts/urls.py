from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

# Read https://github.com/rg3915/django-auth-tutorial

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

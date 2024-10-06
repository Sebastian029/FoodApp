# backend/api/urls.py

from django.urls import path
from .views import welcome

urlpatterns = [
    path('welcome/', welcome, name='welcome'),  # Ensure this pattern is correct
]

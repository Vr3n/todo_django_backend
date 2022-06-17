from django.urls import path

from users.views import register_user

urlpatterns = [
    path('register/', register_user, name="api_register_user"),
]

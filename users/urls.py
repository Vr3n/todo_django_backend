from django.urls import path, include

from users.views import RegisterUserAPIView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name="api_register_user"),
    path('', include('dj_rest_auth.urls')),
]

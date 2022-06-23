from django.urls import path, include

from users.views import RegisterUserAPIView, ProfileRetrieveUpdateView


urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name="api_register_user"),
    path('profile/<int:pk>/', ProfileRetrieveUpdateView.as_view(),
         name="api_profile"),
    path('', include('dj_rest_auth.urls')),
]

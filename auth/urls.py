from django.urls import path

from . import views


urlpatterns = [
    path('/token', views.AuthTokenPairAPIView.as_view(), name='auth_login'),
]

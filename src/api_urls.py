from django.urls import path, include


urlpatterns = [
    path('auth', include('auth.urls')),
    path('', include('user.urls')),
    path('', include('department.urls')),
]

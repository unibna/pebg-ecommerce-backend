from django.urls import path, include


urlpatterns = [
    path('auth', include('auth.urls')),
    path('', include('product.urls')),
    path('', include('department.urls')),
    path('', include('user.urls')),
]

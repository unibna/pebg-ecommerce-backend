from django.urls import path, include


urlpatterns = [
    path('auth', include('auth.urls')),
    path('', include('cart.urls')),
    path('', include('department.urls')),
    path('', include('product.urls')),
    path('', include('user.urls')),
]

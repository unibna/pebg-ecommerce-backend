from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'carts/items', views.CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('carts/items/add', views.CartItemCreateUpdateAPIView.as_view(), name='cart-item-add '),
    
    path('carts', views.CartAPIView.as_view(), name='cart-retrieve'),
]
